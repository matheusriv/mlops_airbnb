"""
Author: Matheus Silva
Date: July 2022
This project is responsible to fetch data
and create a wandb artifact.
"""
import argparse
import logging
import os
import gdown
import wandb

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(message)s",
                    datefmt='%d-%m-%Y %H:%M:%S')

LOGGER = logging.getLogger()


def process_args(args):
    """Process args passed by cmdline and fetch raw data
    Args:
        args - command line arguments
        args.input_url: Google Drive URL to download dataset
        args.artifact_name:  Name for the artifact
        args.artifact_type: Type for the artifact
        args.project_name: Name of WandB project you want to access/create
        args.artifact_description: Description for the artifact
    """
    run = wandb.init(project=args.project_name,
                     job_type="fetch_data")

    LOGGER.info("Dowloading file")
    url = args.input_url.replace("'","")
    LOGGER.info(url)
    raw_data = gdown.download(url, quiet=False)

    LOGGER.info("Creating W&B artifact")
    artifact = wandb.Artifact(
        name=args.artifact_name,
        type=args.artifact_type,
        description=args.artifact_description
    )
    artifact.add_file(raw_data)

    LOGGER.info("Logging artifact to wandb project")
    run.log_artifact(artifact)

    # Remote temporary files
    os.remove(raw_data)

    run.finish()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description="Fetch csv data from google drive",
        fromfile_prefix_chars="@"
    )

    PARSER.add_argument(
        "--input_url",
        type=str,
        help="Google Drive URL to download dataset",
        required=True
    )

    PARSER.add_argument(
        "--artifact_name",
        type=str,
        help="Name for the artifact",
        required=True
    )

    PARSER.add_argument(
        "--artifact_type",
        type=str,
        help="Type for the artifact",
        required=True
    )

    PARSER.add_argument(
        "--project_name",
        type=str,
        help="Name of WandB project you want to access/create",
        required=True
    )

    PARSER.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        default="",
        required=False
    )
    ARGS = PARSER.parse_args()
    process_args(ARGS)
