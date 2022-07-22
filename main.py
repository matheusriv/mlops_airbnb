"""
Creator: Matheus Silva
Date: Jul. 2022
"""
import mlflow
import os
import hydra
from omegaconf import DictConfig, OmegaConf

# This automatically reads in the configuration
@hydra.main(config_name='config')
def process_args(config: DictConfig):

    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # You can get the path at the root of the MLflow project with this:
    root_path = hydra.utils.get_original_cwd()

    # Check which steps we need to execute
    if isinstance(config["main"]["execute_steps"], str):
        # This was passed on the command line as a comma-separated list of steps
        steps_to_execute = config["main"]["execute_steps"].split(",")
    else:
        steps_to_execute = list(config["main"]["execute_steps"])

    # Download step
    if "download" in steps_to_execute:
        _ = mlflow.run(
            os.path.join(root_path, "download"),
            "main",
            parameters={
                "input_url": config["data"]["input_url"],
                "artifact_name": "raw_data.csv",
                "artifact_type": "raw_data",
                "artifact_description": "Raw data from airbnb house prices in Rio de Janeiro"
            }
        )

    if "preprocess" in steps_to_execute:
        _ = mlflow.run(
            os.path.join(root_path, "preprocessing"),
            "main",
            parameters={
                "input_artifact": "raw_data.csv:latest",
                "artifact_name": "clean_data.csv",
                "artifact_type": "clean_data",
                "artifact_description": "Clean data from airbnb house prices in Rio de Janeiro"
            }
        )

    if "segregate" in steps_to_execute:
        _ = mlflow.run(
            os.path.join(root_path, "segregation"),
            "main",
            parameters={
                "input_artifact": "clean_data.csv:latest",
                "artifact_root": "data",
                "artifact_type": "segregated_data",
                "test_size": config["data"]["test_size"],
                "stratify": config["data"]["stratify"],
                "random_state": config["main"]["random_seed"]
            }
        )

    if "check_data" in steps_to_execute:
        _ = mlflow.run(
            os.path.join(root_path, "data_checks"),
            "main",
            parameters={
                "clean_data_artifact": "clean_data.csv:latest",
                "reference_artifact": config["data"]["reference_dataset"],
                "sample_artifact": config["data"]["sample_dataset"],
                "ks_alpha": config["data"]["ks_alpha"]
            }
        )


if __name__ == "__main__":
    process_args()