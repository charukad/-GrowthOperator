from typing import List
from openai import AsyncOpenAI
from app.core.config import settings
from loguru import logger

class EmbeddingService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"

    async def get_embedding(self, text: str) -> List[float]:
        try:
            response = await self.client.embeddings.create(
                input=[text.replace("\n", " ")],
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise e

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            # Basic batching could be implemented here if needed
            response = await self.client.embeddings.create(
                input=[text.replace("\n", " ") for text in texts],
                model=self.model
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise e

embedding_service = EmbeddingService()
