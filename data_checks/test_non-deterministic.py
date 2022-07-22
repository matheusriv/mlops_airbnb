"""
Author: Matheus Silva
Date: July 2022
"""
import scipy.stats

def test_kolmogorov_smirnov(splitted_data, ks_alpha):
    """Check if train/test datasets are correct"""
    sample1, sample2 = splitted_data

    numerical_columns = ['accommodates', 'bedrooms', 'beds', 'price',
                         'number_of_reviews', 'review_scores_rating',
                         'review_scores_accuracy', 'review_scores_cleanliness',
                         'review_scores_checkin', 'review_scores_communication',
                         'review_scores_location', 'review_scores_value', 'bathrooms']

    # Bonferroni correction for multiple hypothesis testing
    alpha_prime = 1 - (1 - ks_alpha)**(1 / len(numerical_columns))

    for col in numerical_columns:
        # two-sided: The null hypothesis is that the two distributions are identical
        # the alternative is that they are not identical.
        _, p_value = scipy.stats.ks_2samp(
            sample1[col],
            sample2[col],
            alternative='two-sided'
        )
        # NOTE: as always, the p-value should be interpreted as the probability of
        # obtaining a test statistic (TS) equal or more extreme that the one we got
        # by chance, when the null hypothesis is true. If this probability is not
        # large enough, this dataset should be looked at carefully, hence we fail
        assert p_value > alpha_prime
