# -*- coding: utf-8 -*-

import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import stats
import MySQLdb

conn = MySQLdb.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'root',
    db = 'finance'
)
data = pd.read_sql('select * from gold_prices', conn, index_col='date')

goldPrices = data.daily
goldRtn = goldPrices.pct_change()

# print goldPrices

# print goldPrices.describe()
# print goldRtn.describe()
print 'max: %s'%goldRtn.max()
print 'min: %s'%goldRtn.min()
print 'mean: %s'%goldRtn.mean()
print 'median: %s'%goldRtn.median()
print 'std: %s'%goldRtn.std()
print 'skew: %s'%goldRtn.skew()
print 'kurt: %s'%goldRtn.kurt()

# print 't-test:'
# print stats.ttest_1samp(goldRtn, 0, nan_policy='omit')

print 'whether the skew is different from the normal distribution'
print stats.skewtest(goldRtn, nan_policy='omit')

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文

plt.subplot(221)
plt.title('Gold daily prices')
goldPrices.plot()

plt.subplot(222)
plt.title('Gold daily simple rate of return')
goldRtn.plot()

plt.subplot(223)
plt.title('Gold daily simple rate of return')
# plt.hist(goldRtn, bins=100, range=(goldRtn.min(), goldRtn.max()))
x = np.arange(goldRtn.min(), goldRtn.max(), 0.01)
y = stats.norm.pdf(x, goldRtn.mean(), goldRtn.std())
plt.plot(x, y)
goldRtn.hist(bins=100)

plt.subplot(224)
plt.title('Gold autocorrelation')
plt.acorr(goldRtn, maxlags=150)

plt.show()
