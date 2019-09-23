import pandas as pd


def accumulate_weekly(data: pd.DataFrame):
    """
    Accumulates the amount and revenue off equal items per week.

    :param data: input table
    :return: table where items are accumulated
    """
    accumulated = pd.DataFrame()
    for Calendar_week_value, calendar_week in data.groupby('Calendar_week', as_index=False):
        inter = calendar_week.groupby('Article_Number').agg({"Revenue": "sum", "Amount": "sum"})
        inter['Calendar_week'] = Calendar_week_value
        accumulated = accumulated.append(inter)
    return accumulated


data = pd.read_csv("../Data/CSV/Customer_A.csv", sep=';')
data = accumulate_weekly(data)
print(data)
