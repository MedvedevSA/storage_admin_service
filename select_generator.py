import logging
from typing import Any, Callable, TypeVar

from sqlalchemy import BinaryExpression, Select, String, cast, select
from sqlalchemy.orm import InstrumentedAttribute

from database import Base
from schemas import PagingModel, SortingModel

logger = logging.getLogger("uvicorn")
Dump = TypeVar('Dump', bound=dict[str, Any])
suffixes = dict()


def reg_suffix(fn: Callable) -> Callable:
    suffixes['_' + fn.__name__] = fn

    def _wrapper(
            col: InstrumentedAttribute,
            fld_val: Any
    ) -> BinaryExpression | None:
        return fn(col, fld_val)

    return _wrapper


@reg_suffix
def _ilike(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return cast(col, String).ilike(f'%{str(fld_val)}%')


@reg_suffix
def _in(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return col.in_(fld_val)


@reg_suffix
def _eq(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return col == fld_val


@reg_suffix
def _neq(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return col != fld_val


@reg_suffix
def _ge(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return col >= fld_val


@reg_suffix
def _le(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return col <= fld_val


@reg_suffix
def _gt(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return col > fld_val


@reg_suffix
def _lt(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return col < fld_val


@reg_suffix
def _is_none(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    if fld_val:
        return col.is_(None)
    return col.is_not(None)


def get_model_col(model: Base, fld: str) -> InstrumentedAttribute | None:
    try:
        column = getattr(model, fld)
        assert isinstance(column, InstrumentedAttribute)
        return column

    except AttributeError:
        logger.warning(
            "\n".join([
                f"{__name__}.{get_model_col.__name__}:",
                f"{model} has no attr \"{fld}\""
            ])
        )
    except AssertionError:
        logger.warning(
            "\n".join([
                f"{__name__}.{get_model_col.__name__}:",
                f"{model}.\"{fld}\" is not {InstrumentedAttribute}"
            ])
        )


class SelectGenerator:
    def __init__(
            self,
            model: Base,
            params: Dump = None,
            relations: dict[str, Base] = None
    ):
        self.model = model
        self.params = params or {}
        self.relations = relations or {}
        self.stmt = select(self.model)

    def get_stmt(self) -> Select:
        self.join_relations()
        self.stmt = self.stmt.where(*self.where_from_params())
        self.adjust_paging_sorting()
        self.adjust_order_by()
        return self.stmt

    def join_relations(self):
        for model in self.relations.values():
            self.stmt = self.stmt.outerjoin(model)

    def where_from_params(self) -> list[BinaryExpression]:
        where = [self.parse(_fld, val) for _fld, val in self.params.items()]
        return [el for el in where if isinstance(el, BinaryExpression)]

    def parse_prefix(self, fld: str) -> tuple[Base, str]:
        for prefix, model in self.relations.items():
            prefix = prefix + '__'
            if fld.startswith(prefix):
                return model, fld.removeprefix(prefix)
        return self.model, fld

    def parse(self, fld: str, val: Any) -> BinaryExpression | None:
        model, fld = self.parse_prefix(fld)

        for suffix, fn in suffixes.items():
            if fld.endswith(suffix):
                if col := get_model_col(model, fld.removesuffix(suffix)):
                    return fn(col, val)

        if fld not in [*PagingModel.model_fields, *SortingModel.model_fields]:
            if col := get_model_col(model, fld):
                return _eq(col, val)

    def adjust_order_by(self) -> None:
        sorting = SortingModel.model_validate(self.params)
        if sorting.sort_col and (
            col := get_model_col(self.model, sorting.sort_col)
        ):
            order_by = {'asc': col.asc(), 'desc': col.desc()}
            self.stmt = self.stmt.order_by(order_by[sorting.sort_order])

    def adjust_paging_sorting(self) -> None:
        pg = PagingModel.model_validate(self.params)
        if pg.offset and pg.page_limit:
            self.stmt = self.stmt.offset(pg.offset).limit(pg.page_limit)