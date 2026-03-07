from typing import List
from datetime import datetime, timedelta

from app.models.analytics import (
    Analytics,
    AnalyticsCreate
)


class AnalyticsService:


    # ==============================
    # TRACK VISIT
    # ==============================

    @staticmethod
    async def track_visit(data: AnalyticsCreate):

        analytics = Analytics(**data.model_dump())

        await analytics.insert()

        return analytics


    # ==============================
    # TOTAL VISITORS
    # ==============================

    @staticmethod
    async def total_visitors():

        return await Analytics.count()


    # ==============================
    # TODAY VISITORS
    # ==============================

    @staticmethod
    async def today_visitors():

        today = datetime.utcnow().date()

        return await Analytics.find(
            {"created_at": {"$gte": datetime(today.year, today.month, today.day)}}
        ).count()


    # ==============================
    # PAGE VIEWS
    # ==============================

    @staticmethod
    async def page_views():

        pipeline = [
            {
                "$group": {
                    "_id": "$page",
                    "views": {"$sum": 1}
                }
            }
        ]

        return await Analytics.aggregate(pipeline).to_list()


    # ==============================
    # AVG SESSION TIME
    # ==============================

    @staticmethod
    async def average_session_time():

        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "avg_time": {"$avg": "$session_duration"}
                }
            }
        ]

        result = await Analytics.aggregate(pipeline).to_list()

        if result:
            return result[0]["avg_time"]

        return 0