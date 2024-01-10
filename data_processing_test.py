import pytest
import pandas as pd
from data_processing import *

def initialize_test_data():
    file_path = r"C:\\Users\\joebe\\Documents\\Finance\\LiquiLens\\Data\\TestData\\bk_download.csv"

    dataframe = pd.read_csv(file_path)
    return dataframe


def test_calculate_positive_cash_flow():
    dataframe = initialize_test_data()
    result = calculatePositiveCashFlow(dataframe)
    expected_result = 1178.88
    assert result == expected_result


def test_calculate_negative_cash_flow():
    dataframe = initialize_test_data()
    result = calculateNegativeCashFlow(dataframe)
    expected_result = -1892.76
    assert result == expected_result

def test_calculate_net_cash_flow():
    dataframe = initialize_test_data()
    result = calculateNetCashFlow(dataframe)
    expected_result = -713.88
    assert result == expected_result

def test_calculate_income_to_expense_ratio():
    dataframe = initialize_test_data()
    result = calculateIncomeToExpenseRatio(dataframe)
    expected_result = round(abs(1892.76 / 1178.88),2)
    assert result == expected_result
