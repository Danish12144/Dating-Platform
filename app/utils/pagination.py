# app/utils/pagination.py
from fastapi import Query

def pagination_params():
    async def _inner(
        page: int = Query(1, ge=1, description="Page number, starts at 1"),
        limit: int = Query(20, ge=1, le=100, description="Items per page"),
    ):
        skip = (page - 1) * limit
        return {"skip": skip, "limit": limit, "page": page}
    return _inner
