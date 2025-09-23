import pandas as pd


def print_df(df: pd.DataFrame, max_rows: int = 10):
    with pd.option_context("display.max_rows", max_rows, "display.max_columns", None):
        print(df)



