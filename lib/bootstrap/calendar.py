__version__ = "1.0.0"

from datetime import datetime, timedelta
from typing import Optional, Dict


class Calendar:
    """
    Date and period helper utilities.

    Provides:
        - current date/time
        - current month information
        - previous month information
        - next month information
        - period boundaries
    """

    alias = "calendar"

    @staticmethod
    def get_current_date(pattern: Optional[str] = None) -> str:
        if pattern is None:
            pattern = "%Y-%m-%d"
        return datetime.now().strftime(pattern)

    @staticmethod
    def get_current_datetime() -> datetime:
        return datetime.now()

    @staticmethod
    def get_current_time(pattern: Optional[str] = None) -> str:
        if pattern is None:
            pattern = "%H:%M:%S"
        return datetime.now().strftime(pattern)

    @staticmethod
    def get_current_period_info(
        reference_date: Optional[datetime] = None
    ) -> Dict[str, str]:

        bounds = Calendar._current_month_bounds(reference_date)

        return {
            "first_day_current_month": bounds["first_day"].strftime("%Y-%m-%d"),
            "last_day_current_month": bounds["last_day"].strftime("%Y-%m-%d"),
            "current_month": bounds["first_day"].strftime("%m"),
            "current_year": bounds["first_day"].strftime("%Y"),
        }

    @staticmethod
    def get_previous_month_first_day(
        pattern: Optional[str] = None,
        reference_date: Optional[datetime] = None
    ) -> str:

        if pattern is None:
            pattern = "%Y-%m-%d"

        bounds = Calendar._previous_month_bounds(reference_date)

        return bounds["first_day"].strftime(pattern)

    @staticmethod
    def get_previous_month_last_day(
        pattern: Optional[str] = None,
        reference_date: Optional[datetime] = None
    ) -> str:

        if pattern is None:
            pattern = "%Y-%m-%d"

        bounds = Calendar._previous_month_bounds(reference_date)

        return bounds["last_day"].strftime(pattern)

    @staticmethod
    def get_previous_month(
        pattern: Optional[str] = None,
        reference_date: Optional[datetime] = None
    ) -> str:

        if pattern is None:
            pattern = "%m"

        bounds = Calendar._previous_month_bounds(reference_date)

        return bounds["first_day"].strftime(pattern)

    @staticmethod
    def get_previous_year(
        pattern: Optional[str] = None,
        reference_date: Optional[datetime] = None
    ) -> str:

        if pattern is None:
            pattern = "%Y"

        ref = reference_date or datetime.now()

        return datetime(ref.year - 1, 1, 1).strftime(pattern)

    @staticmethod
    def get_previous_period_info(
        reference_date: Optional[datetime] = None
    ) -> Dict[str, str]:

        bounds = Calendar._previous_month_bounds(reference_date)

        return {
            "first_day_previous_month": bounds["first_day"].strftime("%Y-%m-%d"),
            "last_day_previous_month": bounds["last_day"].strftime("%Y-%m-%d"),
            "previous_month": bounds["first_day"].strftime("%m"),
            "previous_year": bounds["first_day"].strftime("%Y"),
        }

    @staticmethod
    def get_next_month_first_day(
        pattern: Optional[str] = None,
        reference_date: Optional[datetime] = None
    ) -> str:

        if pattern is None:
            pattern = "%Y-%m-%d"

        bounds = Calendar._next_month_bounds(reference_date)

        return bounds["first_day"].strftime(pattern)

    @staticmethod
    def get_next_month_last_day(
        pattern: Optional[str] = None,
        reference_date: Optional[datetime] = None
    ) -> str:

        if pattern is None:
            pattern = "%Y-%m-%d"

        bounds = Calendar._next_month_bounds(reference_date)

        return bounds["last_day"].strftime(pattern)

    @staticmethod
    def get_next_month(
        pattern: Optional[str] = None,
        reference_date: Optional[datetime] = None
    ) -> str:

        if pattern is None:
            pattern = "%m"

        bounds = Calendar._next_month_bounds(reference_date)

        return bounds["first_day"].strftime(pattern)

    @staticmethod
    def get_next_period_info(
        reference_date: Optional[datetime] = None
    ) -> Dict[str, str]:

        bounds = Calendar._next_month_bounds(reference_date)

        return {
            "first_day_next_month": bounds["first_day"].strftime("%Y-%m-%d"),
            "last_day_next_month": bounds["last_day"].strftime("%Y-%m-%d"),
            "next_month": bounds["first_day"].strftime("%m"),
            "next_year": bounds["first_day"].strftime("%Y"),
        }

    @staticmethod
    def _current_month_bounds(
        reference_date: Optional[datetime] = None
    ) -> Dict[str, datetime]:

        ref = reference_date or datetime.now()

        first_day = ref.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        if first_day.month == 12:
            next_month_first = first_day.replace(
                year=first_day.year + 1,
                month=1,
            )
        else:
            next_month_first = first_day.replace(
                month=first_day.month + 1
            )

        last_day = next_month_first - timedelta(days=1)

        return {
            "first_day": first_day,
            "last_day": last_day,
        }

    @staticmethod
    def _previous_month_bounds(
        reference_date: Optional[datetime] = None
    ) -> Dict[str, datetime]:

        ref = reference_date or datetime.now()

        first_day_current_month = ref.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        last_day_previous_month = (
            first_day_current_month - timedelta(days=1)
        )

        first_day_previous_month = (
            last_day_previous_month.replace(day=1)
        )

        return {
            "first_day": first_day_previous_month,
            "last_day": last_day_previous_month,
        }

    @staticmethod
    def _next_month_bounds(
        reference_date: Optional[datetime] = None
    ) -> Dict[str, datetime]:

        ref = reference_date or datetime.now()

        ref = ref.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        if ref.month == 12:
            first_day_next_month = ref.replace(
                year=ref.year + 1,
                month=1,
                day=1,
            )
        else:
            first_day_next_month = ref.replace(
                month=ref.month + 1,
                day=1,
            )

        if first_day_next_month.month == 12:
            first_day_month_after = first_day_next_month.replace(
                year=first_day_next_month.year + 1,
                month=1,
                day=1,
            )
        else:
            first_day_month_after = first_day_next_month.replace(
                month=first_day_next_month.month + 1,
                day=1,
            )

        last_day_next_month = (
            first_day_month_after - timedelta(days=1)
        )

        return {
            "first_day": first_day_next_month,
            "last_day": last_day_next_month,
        }