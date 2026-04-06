import asyncio
from app.core.celery_app import celery_app
from app.scrapers.reddit_scraper import RedditScraper
from app.db.session import AsyncSessionLocal
from app.models.trend import Trend
from loguru import logger
import uuid

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
                if result.scalars().first():
                    continue
                
                new_trend = Trend(
                    workspace_id=uuid.UUID(workspace_id),
                    title=trend_data.title,
                    summary=trend_data.summary,
                    source=trend_data.source,
                    url=trend_data.url,
                    external_id=trend_data.external_id,
                    raw_data=trend_data.raw_data
                )
                db.add(new_trend)
            await db.commit()
            logger.info(f"Successfully scraped {len(scraped_trends)} trends for {niche}")

    asyncio.run(run_scrape())
    return f"Scraping complete for {niche}"
