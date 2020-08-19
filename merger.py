import pandas as pd


def merge_summaries(dataframes: list) -> pd.DataFrame:
    all_columns = set().union(*list(map(lambda x: x.columns, dataframes)))
    new_dataframes = []
    for df in dataframes:
        data = {}
        for column in all_columns:
            if column in df.columns:
                data[column] = [df[column].values[0]]
            else:
                data[column] = [""]
        new_dataframes.append(pd.DataFrame(data))

    return pd.concat(new_dataframes)
