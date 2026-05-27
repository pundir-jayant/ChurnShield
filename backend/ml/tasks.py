from celery import shared_task
from .training import train_and_select

@shared_task
def retrain_churn_model(dataset_path):
    return train_and_select(dataset_path)

