# Instructions

This project is responsible to split the clean data saved in the last step (preprocessing). The script will produce 2 artifacts: data_train.csv and data_test.csv.

## Run Steps

```bash
mlflow run . -P hydra_options="main.execute_steps='segregate'"
```

This command splits the dataset in train/test with the test accounting for 30% of the original dataset. The split is stratified according to the target, to keep the same label balance.
