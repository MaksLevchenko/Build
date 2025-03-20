from pydantic import BaseModel

class PaginationSchema(BaseModel):
    offset: int = 0
    limit: int = 0
    count: int = 0
