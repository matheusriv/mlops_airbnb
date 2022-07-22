# Instructions

This project is responsible to do both deterministics and non-deterministics tests on clean dataset and train/test data, checking if everything is strictly correct in the clean and train/test data.

On non-deterministic test, we did a [kolmogorov smirnov test](https://pt.wikipedia.org/wiki/Teste_Kolmogorov-Smirnov). 

## Run Steps

```bash
mlflow run . -P hydra_options="main.execute_steps='check_data'"
```
