from importlib import import_module
from pathlib import Path

from fastapi import FastAPI


def create_routes(app: FastAPI, *modules):
    for m in modules:
        app.include_router(
            getattr(m, 'r'),
            tags=[short_module_name(m.__name__)],
        )


def short_module_name(name: str):
    return name.split('.')[-1]


def module_url(name: str):
    return f'/{short_module_name(name)}'


def include_module_route(app: FastAPI, module_path: Path):
    def path_to_import_str(path: Path) -> str:
        return str(path).rstrip('.py').replace('/', '.')

    router_module = import_module(
        path_to_import_str(module_path)
    )
    if hasattr(router_module, 'r'):
        app.include_router(
            router_module.r,
            prefix='',
            tags=[short_module_name(router_module.__name__)],
        )


def include_routes(app: FastAPI):
    src_path = Path('./routes')
    src_modules = [module for module in src_path.iterdir() if module.is_file()]
    for module in src_modules:
        include_module_route(app, module)
