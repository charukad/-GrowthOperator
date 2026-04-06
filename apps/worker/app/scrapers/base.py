from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ScrapedTrend(BaseModel):
    title: str
    url: Optional[str] = None
    summary: Optional[str] = None
    source: str
    raw_data: Dict[str, Any]
    external_id: str

class BaseScraper(ABC):
    @abstractmethod
    async def scrape(self, niche: str, **kwargs) -> List[ScrapedTrend]:
        pass
