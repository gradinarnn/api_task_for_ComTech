from datetime import date

from .models import Catalog


def get_actual_catalog(full_title):
    return Catalog.objects.filter(full_title=full_title, start_date__lte=date.today()).order_by(
        '-start_date')
