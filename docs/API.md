# API Documentation

Authentication uses JWT for API clients and Django sessions for the template UI.

## Register
`POST /api/auth/register/`
```json
{"username":"analyst","email":"a@example.com","password":"StrongPass123","role":"analyst"}
```

## Token
`POST /api/auth/token/`
```json
{"username":"analyst","password":"StrongPass123"}
```

## Manual Prediction
`POST /api/predictions/predict/`
```json
{
  "gender":"Female","senior_citizen":false,"partner":"Yes","dependents":"No",
  "tenure":8,"phone_service":"Yes","multiple_lines":"No","internet_service":"Fiber optic",
  "online_security":"No","tech_support":"No","contract":"Month-to-month",
  "paperless_billing":"Yes","payment_method":"Electronic check",
  "monthly_charges":88.5,"total_charges":701.2
}
```

## Dataset Upload
`POST /api/datasets/` with multipart field `file`.

## Batch Prediction
`POST /api/datasets/{id}/batch_predict/`

## Dashboard Summary
`GET /api/dashboard/summary/`

## Reports
`POST /api/reports/prediction/{prediction_id}/`

