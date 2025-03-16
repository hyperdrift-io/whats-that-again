"""
Pydantic models for request and response validation
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str
    sessionId: Optional[str] = None
    tryNextModel: bool = False


class MemoryTag(BaseModel):
    tag: str


class SearchResponse(BaseModel):
    answer: str
    confidence: float
    usage_info: str
    memoryTags: List[str] = []
    sessionId: str
    model: str
    modelLevel: int
