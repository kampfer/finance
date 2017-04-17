# coding: utf-8

import sys
import MySQLdb
import pandas as pd

print('MySQLdb: %s') % MySQLdb.__version__

def saveData(excelPath):
    conn = MySQLdb.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        passwd = 'root'
    )

    cursor = conn.cursor()

    # 如果数据库不存在就创建新的数据库，并切换到新数据库
    cursor.execute('create database if not exists finance')
    conn.select_db('finance')
    conn.commit()

    cursor.execute('drop table if exists gold_prices')
    cursor.execute('create table gold_prices(date date primary key, daily float)')
    conn.commit()

    goldDailyPrices = pd.read_excel(
        io = excelPath,
        sheetname = 'Daily',
        header = 7,
        index_col = 3
    )

    goldDailyUSDPrices = []
    for index, price in goldDailyPrices['US dollar'].iteritems():
        goldDailyUSDPrices.append((index, price))

    cursor.executemany('insert ignore into gold_prices(date, daily) values(%s, %s)', goldDailyUSDPrices)
    conn.commit()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) > 3:
        excelPath = sys.argv[2]
    else:
        excelPath = 'Prices.xlsx'

    saveData(excelPath)
