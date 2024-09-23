import pandas as pd


def basicStats(df, column):
    aggr = (
        df
        .groupby(column)
        .agg(
            n=('id', 'nunique'),
        )
        .assign(
            perc=lambda x: x['n'] / x['n'].sum()
        )
        .reset_index()
    )

    return aggr;


def sortByColumn(df, column):
    if column == None:
        return df;
    return df.sort_values(by=column, ascending=False)
