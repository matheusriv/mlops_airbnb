"""
Author: Matheus Silva
Date: July 2022
"""
import pandas as pd


def test_dataset_size(full_data):
    """Check if dataset has more than 3000 rows"""
    assert len(full_data) > 3000, "The choosen Dataset is smaller than 3000 rows."


def test_column_presence_and_type(full_data):
    """Check if dataset has all needed columns with the correct type"""

    required_columns = {
        "room_type": pd.api.types.is_object_dtype,
        "accommodates": pd.api.types.is_int64_dtype,
        "bathrooms": pd.api.types.is_float_dtype,
        "bedrooms": pd.api.types.is_int64_dtype,
        "beds": pd.api.types.is_int64_dtype,
        "price": pd.api.types.is_float_dtype,
        "host_listings_count": pd.api.types.is_int64_dtype,
        "availability_30": pd.api.types.is_int64_dtype,
        "availability_60": pd.api.types.is_int64_dtype,
        "availability_90": pd.api.types.is_int64_dtype,
        "availability_365": pd.api.types.is_int64_dtype,
        "number_of_reviews": pd.api.types.is_int64_dtype,
        "minimum_nights": pd.api.types.is_int64_dtype,
        "maximum_nights": pd.api.types.is_int64_dtype,
        "neighbourhood_cleansed": pd.api.types.is_object_dtype,
        "host_is_superhost": pd.api.types.is_object_dtype,
        "host_response_time": pd.api.types.is_object_dtype,
        "host_response_rate": pd.api.types.is_float_dtype,
        "instant_bookable": pd.api.types.is_object_dtype,
        "host_identity_verified": pd.api.types.is_object_dtype,
        "host_verifications": pd.api.types.is_object_dtype,
        "amenities": pd.api.types.is_object_dtype
    }

    # Check column presence
    assert set(full_data.columns.values).issuperset(
        set(required_columns.keys()))

    for col_name, format_verification_funct in required_columns.items():

        assert format_verification_funct(full_data[col_name]), \
            f"Column {col_name} failed test {format_verification_funct}"


def test_class_names(full_data):
    """Check that only the known classes are present"""
    known_classes = [
        'Entire home/apt',
        'Private room',
        'Shared room',
        'Hotel room'
    ]

    assert full_data["room_type"].isin(known_classes).all()


def test_column_ranges(full_data):
    """Check if all columns have meaningful data ranges"""
    ranges = {
        "accommodates": (1, 999),
        "bathrooms": (0.0, 99.0),
        "bedrooms": (1.0, 99.0),
        "beds": (1.0, 99.0),
        "price": (0.0, 999999.0),
        "host_listings_count": (0, 999),
        "availability_30": (0, 30),
        "availability_60": (0, 60),
        "availability_90": (0, 90),
        "availability_365": (0, 365),
        "number_of_reviews": (0, 9999),
        "minimum_nights": (1, 9999),
        "maximum_nights": (1, 99999),
    }

    for col_name, (minimum, maximum) in ranges.items():

        assert full_data[col_name].dropna().between(minimum, maximum).all(), (
            f"Column {col_name} failed the test. Should be between {minimum} and {maximum}, "
            f"instead min={full_data[col_name].min()} and max={full_data[col_name].max()}"
        )
