from fastapi import APIRouter, Depends
from typing import List

from app.models.analytics import (
    AnalyticsCreate,
    AnalyticsResponse
)

from app.services.analytics_service import AnalyticsService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# ==============================
# TRACK VISIT (PUBLIC)
# ==============================

@router.post("/track", response_model=AnalyticsResponse)
async def track_visit(data: AnalyticsCreate):

    return await AnalyticsService.track_visit(data)


# ==============================
# ADMIN STATS
# ==============================

@router.get("/stats", dependencies=[Depends(admin_required)])
async def analytics_stats():

    total = await AnalyticsService.total_visitors()
    today = await AnalyticsService.today_visitors()
    pages = await AnalyticsService.page_views()
    avg_time = await AnalyticsService.average_session_time()

    return {
        "total_visitors": total,
        "today_visitors": today,
        "page_views": pages,
        "average_session_time_seconds": avg_time
    }