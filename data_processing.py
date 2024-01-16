#Handles all the data reading and manipulation tasks. Uses Pandas to categorize transactions and calculate financial metrics.
import os
import pandas as panda
from datetime import datetime
from transactionDictionary import transactionDict
from utils import *


def readBankData():
    USAAFilePath = os.path.join(f"C:\\Users\\Nick\\Documents\\Finances\\Main\\Data\\{datetime.now().strftime('%B')}", "bk_download.csv")
    
    #filePath = os.path.join(f"C:\\Users\\Nick\\Documents\\Finances\\Main\\Data\\December", fileName)
    #filePath = os.path.join(f"C:\\Users\\joebe\\Downloads", fileName)

    USAADataFrame = panda.read_csv(USAAFilePath)
    SimmonsDataFrame = processSimmonsData()

    all_columns = USAADataFrame.columns.union(SimmonsDataFrame.columns)

    # Reindex both DataFrames to have the same column structure, filling missing ones with NaN or another placeholder
    USAADataFrame = USAADataFrame.reindex(columns=all_columns)
    SimmonsDataFrame = SimmonsDataFrame.reindex(columns=all_columns)

    mergedDataFrame = panda.concat([USAADataFrame, SimmonsDataFrame], ignore_index=True)

    mergedDataFrame = dropUnusedColumns(mergedDataFrame)

    return mergedDataFrame

def dropUnusedColumns(bankDataframe):
    columns_to_drop = ['Posted Date', 'Reference Number', 'Activity Status', 'Activity Type', 'Card Number', 'Category', 'Merchant Category Description', 'Merchant City', 'Merchant Country Code', 'Merchant Postal Code', 'Merchant State or Province', 'Name on Card']
    bankDataframe = bankDataframe.drop(columns_to_drop, axis=1)
    return bankDataframe

def processSimmonsData():
    SimmonsFilePath = os.path.join(f"C:\\Users\\Nick\\Documents\\Finances\\Main\\Data\\{datetime.now().strftime('%B')}", "Transaction History_Current.csv")

    SimmonsDataFrame = panda.read_csv(SimmonsFilePath)

    SimmonsDataFrame.rename(columns={'Merchant Name': 'Description'}, inplace=True)
    SimmonsDataFrame['Description'] = SimmonsDataFrame['Description'].apply(simplify_transaction_name)
    SimmonsDataFrame['Amount'] = SimmonsDataFrame['Amount'].str.replace('$', '', regex=False).astype(float) * -1

    return SimmonsDataFrame


def categorizeTransactions(bankDataframe):
    bankDataframe = bankDataframe[~bankDataframe['Description'].apply(regexSearch_Simmons)] #Exclude simmons statements from transactions
    bankDataframe = bankDataframe[bankDataframe['Status'] != "Pending"]
    bankDataframe['Category'] = bankDataframe['Description'].apply(lambda x: transactionDict.get(x, "Unknown"))
    bankDataframe.to_csv('merged_data.csv', index=False)
    return bankDataframe

def calculatePositiveCashFlow(bankDataframe):
    positiveCashFlow = bankDataframe[bankDataframe['Amount'] > 0]['Amount'].sum()
    return round(positiveCashFlow, 2)

def calculateNegativeCashFlow(bankDataframe):
    negativeCashFlow = bankDataframe[bankDataframe['Amount'] < 0]['Amount'].sum()
    return round(negativeCashFlow, 2)

def calculateNetCashFlow(bankDataframe):
    positiveCashFlow = calculatePositiveCashFlow(bankDataframe)
    negativeCashFlow = calculateNegativeCashFlow(bankDataframe)
    netCashFlow = positiveCashFlow + negativeCashFlow
    return round(netCashFlow, 2)

def calculateIncomeToExpenseRatio(bankDataframe):
    positiveCashFlow = calculatePositiveCashFlow(bankDataframe)
    negativeCashFlow = calculateNegativeCashFlow(bankDataframe)
    incomeToExpenseRatio = abs(negativeCashFlow / positiveCashFlow)
    return round(incomeToExpenseRatio, 2)

def processData():
    bankDataframe = readBankData()
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions_dataframe = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    unknownTransactions_dataframe = categorizedTransactions[categorizedTransactions['Category'] == "Unknown"]

    knownTransactionsDictionaryionary = {}
    unknownTransactionsDictionary = {}

    for index, row in knownTransactions_dataframe.iterrows():
        description = row['Description']
        amount = row['Amount']
        category = transactionDict.get(description)

        if category in knownTransactionsDictionaryionary:
            knownTransactionsDictionaryionary[category] += amount
        else:
            knownTransactionsDictionaryionary[category] = amount

    for index, row in unknownTransactions_dataframe.iterrows():
        description = row['Description']
        amount = row['Amount']

        if description in unknownTransactionsDictionary:
            unknownTransactionsDictionary[description] += amount
        else:
            unknownTransactionsDictionary[description] = amount       

    # Sort the known dictionary by value in descending order
    knownTransactionsDictionaryionary = {k: v for k, v in sorted(knownTransactionsDictionaryionary.items(), key=lambda item: item[1], reverse=True)}

    for category, amount in knownTransactionsDictionaryionary.items():
        # Round to 2 decimal places
        knownTransactionsDictionaryionary[category] = round(amount, 2)
    
    return knownTransactionsDictionaryionary, unknownTransactionsDictionary

def createCategoryDataTable():
    bankDataframe = readBankData()
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]

    positiveCashFlow = calculatePositiveCashFlow(knownTransactions)

    categoriesSum = knownTransactions.groupby('Category')['Amount'].sum().reset_index()
    categoriesSum['Percentage'] = (categoriesSum['Amount'] / positiveCashFlow * 100)
    categoriesSum['Percentage'] = categoriesSum['Percentage'].map('{:,.2f} %'.format)
    categoriesSum = categoriesSum.sort_values(by='Amount', ascending=False)
    categoriesSum['Amount'] = categoriesSum['Amount'].map('{:,.2f} $'.format)

    categoriesColumns = [{"name": col, "id": col} for col in categoriesSum.columns]

    categoriesData = categoriesSum.to_dict('records')

    return categoriesColumns, categoriesData

def createPositiveCashFlowDictionary():

    bankDataframe = readBankData()
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    positiveCashFlow = calculatePositiveCashFlow(knownTransactions)

    return {'positiveCashFlow': positiveCashFlow}

def createNegativeCashFlowDictionary():

    bankDataframe = readBankData()
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    negativeCashFlow = calculateNegativeCashFlow(knownTransactions)

    return {'negativeCashFlow': negativeCashFlow}

def createNetCashFlowDictionary():

    bankDataframe = readBankData()
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    netCashFlow = calculateNetCashFlow(knownTransactions)

    return {'netCashFlow': netCashFlow}

def createIncomeToExpenseRatioDictionary():

    bankDataframe = readBankData()
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    incomeToExpenseRatio = calculateIncomeToExpenseRatio(knownTransactions)

    return {'incomeToExpenseRatio': incomeToExpenseRatio}


unique_transactions = readBankData()['Description'].unique()
print(unique_transactions)