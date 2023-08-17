from datetime import date
from django.db.models.query import QuerySet
from django.db.models import Max
from django.utils import timezone
from refbook.models import RefbookElement


def convert_date(date_str: str) -> date | None:
    '''Check if date has YYYY-MM-DD format.'''
    try:
        return date.fromisoformat(date_str)
    except (TypeError, ValueError):
        return None


def filter_elements(refbook_id: int, version: str = None) -> QuerySet:
    '''Filter elements with pointed or current version.'''

    queryset = RefbookElement.objects.prefetch_related('refbook_version')\
        .filter(refbook_version__refbook=refbook_id)

    if version:
        queryset = queryset.filter(refbook_version__version=version)
    else:
        now = timezone.now().date()
        queryset = queryset.filter(refbook_version__active_from__lte=now)
        cur_ver_date = queryset.aggregate(
            date=Max('refbook_version__active_from')
        )['date']
        queryset = queryset.filter(refbook_version__active_from=cur_ver_date)

    return queryset
