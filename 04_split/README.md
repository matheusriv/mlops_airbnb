# Instructions

This project is responsible to split the clean data saved in the last step (preprocessing). The script will produce 2 artifacts: data_train.csv and data_test.csv.

## Run Steps

```bash
mlflow run . -P input_artifact="mlops_airbnb_preprocessing/clean_data.csv:latest" \
             -P artifact_root="data" \
             -P artifact_type="trainvaltest_data" \
             -P test_size=0.3 \
             -P stratify="room_type" \
             -P random_state="13" \
             -P project_name="mlops_airbnb_split"
```

This command splits the dataset in train/test with the test accounting for 30% of the original dataset. The split is stratified according to the target, to keep the same label balance.
