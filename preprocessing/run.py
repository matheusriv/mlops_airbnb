"""
Author: Matheus Silva
Date: July 2022
This project is responsible for fetching the raw data
and clean the data, generating a new artifact in wandb project.
"""
import argparse
import logging
import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import wandb

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(message)s",
                    datefmt='%d-%m-%Y %H:%M:%S')

LOGGER = logging.getLogger()


def preprocess_data(raw_data):
    """Return the processed DataFrame
    Args:
        raw_data(pd.DataFrame): DataFrame to clean data
    Returns:
        (pd.DataFrame): Processed dataFrame
    """
    LOGGER.info("Selecting columns")
    columns = ['room_type', 'accommodates', 'bathrooms_text', 'bedrooms',
               'beds', 'price', 'number_of_reviews', 'review_scores_rating',
               'review_scores_accuracy', 'review_scores_cleanliness',
               'review_scores_checkin', 'review_scores_communication',
               'review_scores_location', 'review_scores_value']
    raw_data = raw_data[columns]

    LOGGER.info("Dropping duplicates")
    raw_data = raw_data.drop_duplicates(ignore_index=True)

    LOGGER.info("Treating missing values")
    columns_drop = ['room_type', 'accommodates', 'bathrooms_text', 'bedrooms',
                    'beds', 'price', 'number_of_reviews']
    columns_imputer = ['review_scores_rating', 'review_scores_accuracy',
                       'review_scores_cleanliness', 'review_scores_checkin',
                       'review_scores_communication', 'review_scores_location',
                       'review_scores_value']

    clean_data = raw_data.dropna(subset=columns_drop).reset_index(drop=True)

    inputer = SimpleImputer(strategy='mean', missing_values=np.nan)
    arr = clean_data[columns_imputer].values
    arr = inputer.fit_transform(arr)
    imputer_df = pd.DataFrame(arr, columns=columns_imputer)
    clean_data = pd.concat([clean_data[columns_drop], imputer_df], axis=1)

    LOGGER.info("Treating price columns from str to float")
    clean_data['price'] = clean_data['price'].apply(
        lambda x: float(x[1:].replace(',', '')) if isinstance(x, str) else x)

    LOGGER.info("Treating bathrooms_text column")
    clean_data['bathrooms'] = clean_data['bathrooms_text'].apply(treat_bathroom_text)
    clean_data = clean_data.drop(axis=1, labels=['bathrooms_text'])

    return clean_data

def treat_bathroom_text(value):
    """Treat bathroom_text column
    Args:
        value(Any): Value from bathroom_text column
    Returns:
        (float): the float treated value for bathroom_text item
    """
    if not isinstance(value, str):
        return value

    try:
        return float(value.split(' ')[0])
    except ValueError as excep:
        LOGGER.debug(excep)
        return 0.5

def process_args(args):
    """Process args passed by command line
    Args:
        args - command line arguments
        args.input_artifact: Fully qualified name for the input artifact
        args.artifact_name:  Name for the artifact
        args.artifact_type: Type for the artifact
        args.project_name: Name of WandB project you want to access/create
        args.artifact_description: Description for the artifact
    """
    run = wandb.init(project=args.project_name,
                     job_type="preproccess_data")

    LOGGER.info("Dowloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()

    raw_data = pd.read_csv(artifact_path)

    LOGGER.info("Preprocessing dataset")
    clean_data = preprocess_data(raw_data)

    clean_data.to_csv("preprocessed_data.csv", index=False)

    LOGGER.info("Creating W&B artifact")
    artifact = wandb.Artifact(
        name=args.artifact_name,
        type=args.artifact_type,
        description=args.artifact_description
    )
    artifact.add_file("preprocessed_data.csv")

    LOGGER.info("Logging artifact to wandb project")
    run.log_artifact(artifact)

    os.remove("preprocessed_data.csv")

    run.finish()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description="Preproccessing raw data from W&B artifact",
        fromfile_prefix_chars="@"
    )

    PARSER.add_argument(
        "--input_artifact",
        type=str,
        help="Fully qualified name for the input artifact",
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
        required=False,
        default='clean_data'
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
