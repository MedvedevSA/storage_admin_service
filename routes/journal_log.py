from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import JournaLogRepository
from schemas import JournalLog
from services import BaseService
from utils import module_url

r = APIRouter()
BASE = module_url(__name__)


def service_depends():
    return BaseService(JournaLogRepository)


ServiceDepends = Annotated[BaseService, Depends(service_depends)]


@r.get(BASE)
async def get_journal_log(
    journal_log_srvc: ServiceDepends
) -> list[JournalLog]:
    return await journal_log_srvc.get_all(response_model=JournalLog)
