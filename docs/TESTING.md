# Testing Guide

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
pytest
python manage.py train_churn_model --dataset datasets/sample_churn.csv
```

Manual QA:
- Login and open dashboard.
- Upload `datasets/sample_churn.csv`.
- Run batch prediction.
- Submit real-time prediction form.
- Generate a PDF report from a created prediction through the API.

