"""Helper class"""
import numpy as np


def add_counts(df):
    """The next helper function is the add_counts function.

    This function accepts a DataFrame which is then broken down based on cards.
    Then for each card, a lambda functions is applied to each line that counts
    each occurrence of that card. This is done for each card within the hand.
    A new column is then added to the original DataFrame for the count of each card.
    The same is done for the relationships of the suit.

    Note the reason we break them up this way is to not accidentally count a
    "2" in the suits column when we are looking at the cards in hand.
    """
    tmp_card = df[["C1", "C2", "C3", "C4", "C5"]]
    tmp_suit = df[["S1", "S2", "S3", "S4", "S5"]]
    # counts how many like cards are in the row, exposes the relationship required for pairs, sets, and quads.
    df["cnt_c1"] = tmp_card.apply(lambda c: sum(c == c.iloc[0]), axis=1)
    df["cnt_c2"] = tmp_card.apply(lambda c: sum(c == c.iloc[1]), axis=1)
    df["cnt_c3"] = tmp_card.apply(lambda c: sum(c == c.iloc[2]), axis=1)
    df["cnt_c4"] = tmp_card.apply(lambda c: sum(c == c.iloc[3]), axis=1)
    df["cnt_c5"] = tmp_card.apply(lambda c: sum(c == c.iloc[4]), axis=1)
    # counts how many like suits are in the row, allows for easy tracking of flushes
    df["cnt_s1"] = tmp_suit.apply(lambda s: sum(s == s.iloc[0]), axis=1)
    df["cnt_s2"] = tmp_suit.apply(lambda s: sum(s == s.iloc[1]), axis=1)
    df["cnt_s3"] = tmp_suit.apply(lambda s: sum(s == s.iloc[2]), axis=1)
    df["cnt_s4"] = tmp_suit.apply(lambda s: sum(s == s.iloc[3]), axis=1)
    df["cnt_s5"] = tmp_suit.apply(lambda s: sum(s == s.iloc[4]), axis=1)
    return df


def add_diffs(df):
    """The next helper function is the add_diffs function.

    This function accepts a DataFrame which then has 4 new columns added to it.
    Each column represents the difference of the card next to it.
    Therefore when the model is rf, if all values in the columns are
    equal to "1" then it must be a type of straight.
    The second half of the function is similar to the add_counts function
    in the sense that it adds up the differences.
    So if there is a straight the cnt_diff columns should all equal "4"
    except in the case of an ace during a royal straight.
    """
    tmp = df
    # Calculates the difference between cards to determine if a straight is
    # possible
    df["diff_1"] = tmp["C2"] - tmp["C1"]
    df["diff_2"] = tmp["C3"] - tmp["C2"]
    df["diff_3"] = tmp["C4"] - tmp["C3"]
    df["diff_4"] = tmp["C5"] - tmp["C4"]
    # Counts how many similar differences there are. Should improve straight
    # detection, and pair detection
    tmp_diff = df[["diff_1", "diff_2", "diff_3", "diff_4"]]
    df["cnt_diff1"] = tmp_diff.apply(lambda c: sum(c == c.iloc[0]), axis=1)
    df["cnt_diff2"] = tmp_diff.apply(lambda c: sum(c == c.iloc[1]), axis=1)
    df["cnt_diff3"] = tmp_diff.apply(lambda c: sum(c == c.iloc[2]), axis=1)
    df["cnt_diff4"] = tmp_diff.apply(lambda c: sum(c == c.iloc[3]), axis=1)
    return df


def add_unique_count(df):
    """The next helper function is the add_unique_count function.
    This function accepts a DataFrame which is then broken into the suits.
    Then a lambda function is applied to each of the rows to check and see
    how many unique suits are in the hand.
    This helps for checking a flush condition or not. A flush will always have
    a unique count of "1" because all cards must be of the same suit.
    """
    tmp_suit = df[["S1", "S2", "S3", "S4", "S5"]]
    df["unique_suit"] = tmp_suit.apply(lambda s: len(np.unique(s)), axis=1)
    return df


def pre_process_data(data):
    """First, we have to clean up the data to prepare to calculate the
    relationships mentioned above. Here we are taking the data splitting
    it up based on card and suit. We will then sort the values before
    combining it back into one DataFrame and passing onto the next helper
    function that will add relationships to the data frame.
    """
    df = data.copy()
    cards = df[["C1", "C2", "C3", "C4", "C5"]]
    suits = df[["S1", "S2", "S3", "S4", "S5"]]
    cards.values.sort()
    suits.values.sort()
    df[["C1", "C2", "C3", "C4", "C5"]] = cards
    df[["S1", "S2", "S3", "S4", "S5"]] = suits
    df = df[["S1", "C1", "S2", "C2", "S3", "C3", "S4", "C4", "S5", "C5"]]
    # df = add_counts(df)
    # df = add_diffs(df)
    df = add_unique_count(df)
    return df
