# Instructions

This project is responsible to fetch data and create a artifact in Weights and Biases. With artifacts, you can upload the full raw dataset and automatically track and version all the different ways you may subsequently decide to generate my train/val/test splits.

## Run Steps

```bash
mlflow run . -P hydra_options="main.execute_steps='download'"
```
