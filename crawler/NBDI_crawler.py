# coding: utf-8

import time
import requests
import MySQLdb
from pyquery import PyQuery

class NBDICrawler:

    url='https://www.federalreserve.gov/releases/h10/summary/indexb_b.htm'

    def __init__(self):
        self.connectDb()

        self.cursor.execute('drop table if exists us_dollar_index')
        self.cursor.execute('create table us_dollar_index(date date primary key, daily float)')
        self.conn.commit()

        self.add(self.getData())

    def connectDb(self):
        self.conn = MySQLdb.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'root'
        )
        self.cursor = self.conn.cursor()

        # 如果数据库不存在就创建新的数据库，并切换到新数据库
        self.cursor.execute('create database if not exists finance')
        self.conn.select_db('finance')
        self.conn.commit()

    def add(self, dailyIndex):
        try:
            sql = 'insert ignore into us_dollar_index(date, daily) values(%s, %s)'
            if (isinstance(dailyIndex[0], tuple)):
                self.cursor.executemany(sql, dailyIndex)
            else:
                self.cursor.execute(sql, dailyIndex)
        except:
            import traceback
            traceback.print_exc()
            self.conn.rollback()
        finally:
            self.conn.commit()

    def getData(self):
        data = []
        def extraRow(index, elem):
            pqElem = PyQuery(elem)
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(pqElem.find('th').text(), '%d-%b-%y'))
            if pqElem.find('td').text() == 'ND':
                value = None
            else:
                value = float(pqElem.find('td').text())
            data.append((date, value))
        r = requests.get(self.url)
        doc = PyQuery(r.content)
        print r.content
        doc('.pubtables tr').each(extraRow)
        return data

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    NBDICrawler()
