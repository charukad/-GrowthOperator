import asyncio
from app.core.celery_app import celery_app
from app.scrapers.reddit_scraper import RedditScraper
from app.db.session import AsyncSessionLocal
from app.models.trend import Trend, TrendEmbedding
from app.core.config import settings
from loguru import logger
import uuid
from openai import AsyncOpenAI

@celery_app.task(name="scrape_reddit_trends")
def scrape_reddit_trends_task(workspace_id: str, niche: str):
    async def run_scrape():
        scraper = RedditScraper()
        scraped_trends = await scraper.scrape(niche)
        
        async with AsyncSessionLocal() as db:
            for trend_data in scraped_trends:
                # Check if trend already exists for this workspace
                from sqlalchemy import select
                stmt = select(Trend).filter(
                    Trend.workspace_id == uuid.UUID(workspace_id),
                    Trend.external_id == trend_data.external_id
                )
                result = await db.execute(stmt)
                db_trend = result.scalars().first()
                
                if not db_trend:
                    db_trend = Trend(
                        workspace_id=uuid.UUID(workspace_id),
                        title=trend_data.title,
                        summary=trend_data.summary,
                        source=trend_data.source,
                        url=trend_data.url,
                        external_id=trend_data.external_id,
                        raw_data=trend_data.raw_data
                    )
                    db.add(db_trend)
                    await db.commit()
                    await db.refresh(db_trend)
                
                # Trigger embedding task
                generate_trend_embedding_task.delay(str(db_trend.id))
                
            logger.info(f"Successfully processed {len(scraped_trends)} trends for {niche}")

    asyncio.run(run_scrape())
    return f"Scraping complete for {niche}"

@celery_app.task(name="generate_trend_embedding")
def generate_trend_embedding_task(trend_id: str):
    async def run_embedding():
        async with AsyncSessionLocal() as db:
            from sqlalchemy import select
            stmt = select(Trend).filter(Trend.id == uuid.UUID(trend_id))
            result = await db.execute(stmt)
            trend = result.scalars().first()
            
            if not trend:
                logger.error(f"Trend {trend_id} not found for embedding generation")
                return

            # Check if embedding already exists
            stmt_embed = select(TrendEmbedding).filter(TrendEmbedding.trend_id == trend.id)
            result_embed = await db.execute(stmt_embed)
            if result_embed.scalars().first():
                logger.info(f"Embedding already exists for trend {trend_id}")
                return

            # Combine title and summary for embedding
            text_to_embed = f"{trend.title}. {trend.summary or ''}"
            
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            try:
                response = await client.embeddings.create(
                    input=[text_to_embed.replace("\n", " ")],
                    model="text-embedding-3-small"
                )
                embedding_vector = response.data[0].embedding
                
                new_embedding = TrendEmbedding(
                    trend_id=trend.id,
                    embedding=embedding_vector
                )
                db.add(new_embedding)
                await db.commit()
                logger.info(f"Successfully generated embedding for trend {trend_id}")
            except Exception as e:
                logger.error(f"Error generating embedding for trend {trend_id}: {e}")

    asyncio.run(run_embedding())
    return f"Embedding task complete for {trend_id}"
