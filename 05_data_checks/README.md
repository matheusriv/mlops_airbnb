# Instructions

This project is responsible to do both deterministics and non-deterministics tests on clean dataset and train/test data, checking if everything is strictly correct in the clean and train/test data.

On non-deterministic test, we did a [kolmogorov smirnov test](https://pt.wikipedia.org/wiki/Teste_Kolmogorov-Smirnov). 

## Run Steps

```bash
mlflow run . -P reference_artifact="mlops_airbnb_split/train_data.csv:latest" \
             -P sample_artifact="mlops_airbnb_split/test_data.csv:latest" \
             -P ks_alpha=0.05 \
             -P clean_data_artifact="mlops_airbnb_preprocessing/clean_data.csv:latest"
```
