# Instructions

In this project we create a MLflow component that preprocess the data from last step (fetch).

## Run Steps

```bash
mlflow run . -P input_artifact="mlops_airbnb_fetch/raw_data.csv:latest" \
             -P artifact_name="clean_data.csv" \
             -P artifact_type="clean_data" \
             -P artifact_description="Clean data from airbnb house prices in Rio de Janeiro" \
             -P project_name="mlops_airbnb_preprocessing"
```
