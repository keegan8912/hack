import pandas as pd
import numpy as np


meter_rows = ['600700',
    '100868100',
    '100868500',
    '103373903',
    '106250400',
    '113463300',
    '148143400',
    '163467601',
    '182602000']


def read_article_wise_amount_by_week(filepath: str, sep=';', thousands=',') -> np.ndarray:
    """
    Read table from the "Edgar"-formatted csv:

    "Edgar"-format:
                week_1  week_2  week_3  week_4 ...
    article_1      0      10      4       0
    article_2      2       1      0       3
    article_3    300     150     20       0
        .
        .
        .

    :param filepath: path to csv-file
    :param sep: separator used in csv-file
    :param thousands: thousands separator used in csv-file
    :return: numpy array one row per week (row: [amount_article_1, amount_article_2, ...])
    """

    data = pd.read_csv(filepath, sep=sep, thousands=thousands).fillna(0)
    data = data.set_index(data.columns[0]).drop(meter_rows, errors='ignore')
    data = data[data.columns[1:]].apply(pd.to_numeric)
    return data.to_numpy(dtype=np.float32).T


def read_article_wise_amount_by_month(filepath: str, sep=';', thousands=',') -> np.ndarray:
    """
    Read table from the "Edgar"-formatted csv:

    "Edgar"-format:
                week_1  week_2  week_3  week_4 ...
    article_1      0      10      4       0
    article_2      2       1      0       3
    article_3    300     150     20       0
        .
        .
        .

    :param filepath: path to csv-file
    :param sep: separator used in csv-file
    :param thousands: thousands separator used in csv-file
    :return: numpy array one row per month (row: [amount_article_1, amount_article_2, ...])
    """
    by_week = read_article_wise_amount_by_week(filepath, sep, thousands)
    by_month = np.zeros((int(np.ceil(by_week.shape[0] / 4)), by_week.shape[1]))
    for month in range(by_month.shape[0]):
        if by_week[month:, :].shape[0] >= 4:
            by_month[month, :] = np.sum(by_week[month:month + 4, :], axis=0)
        else:
            by_month[month, :] = np.sum(by_week[month:, :], axis=0)
    return by_month


def read_article_amount_by_week(filepath: str, sep=';', thousands=',') -> np.ndarray:
    """
    Read table from the "Edgar"-formatted csv:

    "Edgar"-format:
                week_1  week_2  week_3  week_4 ...
    article_1      0      10      4       0
    article_2      2       1      0       3
    article_3    300     150     20       0
        .
        .
        .

    :param filepath: path to csv-file
    :param sep: separator used in csv-file
    :param thousands: thousands separator used in csv-file
    :return: numpy array (row: [week, amount])
    """
    data = pd.read_csv(filepath, sep=sep, thousands=thousands).fillna(0)
    data = data.set_index(data.columns[0]).drop(meter_rows, errors='ignore')
    data = data[data.columns[1:]].apply(pd.to_numeric)
    data = data.agg(sum).to_numpy(dtype=np.float32)
    return np.column_stack((np.arange(data.shape[0])+1, data))


def read_article_amount_by_month(filepath: str, sep=';', thousands=',') -> np.ndarray:
    """
    Read table from the "Edgar"-formatted csv:

    "Edgar"-format:
                week_1  week_2  week_3  week_4 ...
    article_1      0      10      4       0
    article_2      2       1      0       3
    article_3    300     150     20       0
        .
        .
        .

    :param filepath: path to csv-file
    :param sep: separator used in csv-file
    :param thousands: thousands separator used in csv-file
    :return: numpy array (row: [month, amount])
    """

    by_week = read_article_amount_by_week(filepath, sep, thousands)
    by_month = np.zeros((int(np.ceil(by_week.shape[0]/4)), 2))
    for month in range(by_month.shape[0]):
        if by_week[month:, :].shape[0] >= 4:
            by_month[month, 0] = month
            by_month[month, 1] = np.sum(by_week[month:month+4, 1])
        else:
            by_month[month, 0] = month
            by_month[month, 1] = np.sum(by_week[month:, 1])
    return by_month
