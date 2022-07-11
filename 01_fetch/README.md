# Instructions

This project is responsible to fetch data and create a artifact in Weights and Biases. With artifacts, you can upload the full raw dataset and automatically track and version all the different ways you may subsequently decide to generate my train/val/test splits.

## Run Steps

```bash
mlflow run . -P project_name="mlops_airbnb_fetch" \
             -P artifact_name="raw_data.csv" \
             -P artifact_type="raw_data" \
             -P artifact_description="Raw data from airbnb house prices in Rio de Janeiro" \
             -P input_url="https://drive.google.com/uc?id=1sqkdXwEdN8EQYVkVIKJdVVenKl4BPmHq"
```
