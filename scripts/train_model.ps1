param([string]$Dataset = "datasets/sample_churn.csv")
python manage.py train_churn_model --dataset $Dataset

