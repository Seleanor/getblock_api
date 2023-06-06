from pydantic import BaseModel, StrictStr
from typing import Optional


class LastEthBlockModel (BaseModel):
    result: object
    error: StrictStr = None
    id: StrictStr


class ResultListModel (BaseModel):
    blocks: int
    difficulty: int
    networkhashps: float
    pooledtx: int
    chain: StrictStr
    warnings: StrictStr