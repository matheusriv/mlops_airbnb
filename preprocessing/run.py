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
    columns = ['room_type', 'accommodates', 'bathrooms_text',
               'bedrooms', 'beds', 'price', 'host_listings_count',
               'availability_30', 'availability_60', 'availability_90',
               'availability_365', 'number_of_reviews', 'minimum_nights',
               'maximum_nights', 'neighbourhood_cleansed', 'host_is_superhost',
               'host_response_time', 'host_response_rate', 'instant_bookable',
               'host_identity_verified', 'host_verifications', 'amenities']
    raw_data = raw_data[columns]

    LOGGER.info("Dropping duplicates")
    raw_data = raw_data.drop_duplicates(ignore_index=True)

    LOGGER.info("Treating missing values")
    columns_drop = ['room_type', 'bathrooms_text', 'price']
    columns_imputer_numerical = [
            'accommodates', 'bedrooms', 'beds', 'host_listings_count',
            'availability_30', 'availability_60', 'availability_90',
            'availability_365', 'number_of_reviews', 'minimum_nights',
            'maximum_nights']
    columns_imputer_categorical = [
            'neighbourhood_cleansed', 'host_is_superhost', 'host_response_time',
            'host_response_rate', 'instant_bookable', 'host_identity_verified',
            'host_verifications', 'amenities']

    clean_data = raw_data.dropna(subset=columns_drop).reset_index(drop=True)

    numerical_inputer = SimpleImputer(strategy='median', missing_values=np.nan)
    array = clean_data[columns_imputer_numerical].values
    array = numerical_inputer.fit_transform(array)
    imputer_numerical_df = pd.DataFrame(
        array, columns=columns_imputer_numerical)

    numerical_inputer = SimpleImputer(
        strategy='most_frequent', missing_values=np.nan)
    array = clean_data[columns_imputer_categorical].values
    array = numerical_inputer.fit_transform(array)
    imputer_categorical_df = pd.DataFrame(
        array, columns=columns_imputer_categorical)

    clean_data = pd.concat(
        [clean_data[columns_drop], imputer_categorical_df, imputer_numerical_df],
        axis=1
    )
    
    LOGGER.info("Treating bathrooms_text column")
    clean_data['bathrooms'] = clean_data['bathrooms_text'].apply(
        treat_bathroom_text)
    clean_data = clean_data.drop(axis=1, labels=['bathrooms_text'])

    LOGGER.info("Treating price column")
    clean_data['price'] = clean_data['price'].apply(
        lambda x: float(x[1:].replace(',', '')) if isinstance(x, str) else x)

    LOGGER.info("Treating host_response_rate column")
    clean_data["host_response_rate"] = clean_data["host_response_rate"].apply(
        lambda x: float(x.replace('%', ''))/100
    )

    LOGGER.info("Treating integer column")
    integer_columns = [
            'accommodates', 'bedrooms', 'beds', 'host_listings_count',
            'availability_30', 'availability_60', 'availability_90',
            'availability_365', 'number_of_reviews', 'minimum_nights',
            'maximum_nights']
    clean_data[integer_columns] = clean_data[integer_columns].round(
        0).astype(int)

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
        args.artifact_description: Description for the artifact
    """
    run = wandb.init(job_type="preproccess_data")

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
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        default="",
        required=False
    )
    ARGS = PARSER.parse_args()
    process_args(ARGS)
