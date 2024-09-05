from celery import shared_task
from django.core.management import call_command

@shared_task
def run_daily_kpi_task():
    call_command('calculate_daily_kpis')