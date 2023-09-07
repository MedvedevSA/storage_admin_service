import logging

from fastapi import Request
from sqlalchemy import insert
from starlette.requests import ClientDisconnect


from database import async_session
from models import JournalLog

logger = logging.getLogger("uvicorn")


async def journal_depends(
    request: Request,
):
    try:
        yield
    finally:
        if request.method != 'GET':
            await add_to_journal(request)


def trim_dict(_dict: dict, keys: list) -> dict:
    return {
        k: _dict[k]
        for k
        in keys
        if k in _dict
    }


async def add_to_journal(request: Request):
    data = trim_dict(
        request.scope,
        [   
            'method',
            'path',
            'path_params',
            'headers',
            'client',
        ],
    )

    data['client_ip'] = ':'.join(
        map(str, data.pop('client'))
    )
    headers = []
    for header in data['headers']:
        if b'authorization' not in header:
            headers.append([bytes(el).decode() for el in header])
    data['headers'] = headers

    body = None
    if request.method != 'DELETE':
        try:
            body = await request.json()
        except ClientDisconnect:
            ...
        except Exception as e:
            logger.warning(
                f"{type(e)}, {e}"
            )

    data['body'] = body
    stmt = insert(JournalLog).values(
        dict(client_ip=data.pop('client_ip'), data=data),
    )
    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()
