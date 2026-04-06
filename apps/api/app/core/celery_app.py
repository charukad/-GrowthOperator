from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "growthoperator",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.task_routes = {
    "scrape_reddit_trends": "trend-queue"
}
