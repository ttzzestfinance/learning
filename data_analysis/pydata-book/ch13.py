#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 14:45:12 2018

@author: Teresa
"""

import pandas as pd
import numpy as np
data = pd.DataFrame({
        'x0': [1, 2, 3, 4, 5],
        'x1': [0.01, -0.01, 0.25, -4.1, 0.],
        'y': [-1.5, 0., 3.6, 1.3, -2.]})
data
data.columns
data.values
df2 = pd.DataFrame(data.values, columns = ['one', 'two', 'three'])
df2
df3 = data.copy()
df3['strings'] = ['a', 'b', 'c', 'd', 'e']
df3
df3.values
df2.values
model_cols = ['x0', 'x1']
data.loc[:, model_cols].values
data[model_cols].values
data['category'] = pd.Categorical(['a', 'b', 'a', 'a', 'b'], categories=['a', 'b'])
data
dummies = pd.get_dummies(data.category, prefix='category')
data_with_dummies = data.drop('category', axis=1).join(dummies)
data_with_dummies
dummies
data = pd.DataFrame({
        'x0': [1, 2, 3, 4, 5],
        'x1': [0.01, -0.01, 0.25, -4.1, 0.],
        'y': [-1.5, 0., 3.6, 1.3, -2.]})
data
import patsy
y, X = patsy.dmatrices('y~x0+x1', data)        
y
X
np.asarray(y)
np.asarray(X)
patsy.dmatrices('y~x0+x1+0', data)[1]
coef, resid, _, _ = np.linalg.lstsq(X,y)
coef.T.values
coef.squeeze()
coef=pd.Series(coef.squeeze(), index=X.design_info.column_names)
coef
y, X = patsy.dmatrices('y~standardize(x0)+center(x1)', data)
X
new_data = pd.DataFrame({
        'x0': [6, 7, 8, 9],
        'x1': [3.1, -0.5, 0, 2.3],
        'y': [1, 2, 3, 4]})
new_X = patsy.build_design_matrices([X.design_info], new_data)
new_X
X.design_info
y, X = patsy.dmatrices('y~I(x0+x1)', data) # add columns from a dataset by name
X
data = pd.DataFrame({
        'key1': ['a', 'a', 'b', 'b', 'a', 'b', 'a', 'b'],
        'key2': [0, 1, 0, 1, 0, 1, 0, 0],
        'v1':[1,2,3,4,5,6,7,8],
        'v2': [-1, 0, 2.5, -0.5, 4.0, -1.2, 0.2, -1.7]})
y, X = patsy.dmatrices('v2~key1',data) # non-numeric terms n Patsy formula is converted to dummy variables by default
X
y, X = patsy.dmatrices('v2~key1+0', data)
X
y, X = patsy.dmatrices('v2~C(key2)', data) # numerical columns can be interpreted as categorical with C function
X
data['key2'] = data['key2'].map({0: 'zero', 1: 'one'})
data
y, X = patsy.dmatrices('v2~key1+key2+key1:key2', data) # key1:key2 is the interaction term
X

import statsmodels.api as sm
import statsmodels.formula.api as smf
def dnorm(mean, variance, size=1):
    if isinstance(size, int):
        size=size,
    return mean+np.sqrt(variance)*np.random.randn(*size)
np.random.seed(12345)
N=100
X=np.array([list(dnorm(0, 0.4, size=N)),
        list(dnorm(0, 0.6, size=N)),
        list(dnorm(0, 0.2, size=N))])
X = np.c_[dnorm(0, 0.4, size=N),
          dnorm(0, 0.6, size=N),
          dnorm(0, 0.2, size=N)]
X.shape
eps = dnorm(0, 0.1, size=N)
beta = [0.1, 0.3, 0.5]
y = np.dot(X, beta) +eps
X_model = sm.add_constant(X)
X_model[:5]
model = sm.OLS(y, X)
results = model.fit()
results.params
print(results.summary())
data = pd.DataFrame(X, columns = ['col0', 'col1', 'col2'])
data
data['y'] =y
data[:5]
results = smf.ols('y~col0+col1+col2', data=data).fit()
results.params
results.tvalues
results.pvalues
results.predict(data[:5])

init_x=4
import random
values = [init_x, init_x]
N=1000
b0=0.8
b1=-0.4
noise=dnorm(0, 0.1, N)
for i in range(N):
    new_x = values[-1]*b0+values[-2]*b1+noise[i]
    values.append(new_x)
values[:5]
MAXLAGS=5
model = sm.tsa.AR(values)
results = model.fit(MAXLAGS)
results.params

train = pd.read_csv('../datasets/titanic/train.csv')
test = pd.read_csv('../datasets/titanic/test.csv')
train[:4] # libraries like statsmodel and scikit-learn cannot be fed missing data
train.isnull().sum()
test.isnull().sum()
impute_value = train.Age.median()
train.Age.fillna(impute_value,inplace=True)
test.Age.fillna(impute_value,inplace=True)
train['IsFemale'] = (train.Sex=='female').astype(int)
test['IsFemale'] = (test.Sex=='female').astype(int)
predictors =['Pclass', 'IsFemale', 'Age']
X_train = train[predictors].values
X_test = test[predictors].values
y_train = train['Survived'].values
X_train[:5]
y_train[:5]
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
y_predict = model.predict(X_test)
y_predict[:10]
(y_predict==test['Survived'].values).mean()
from sklearn.linear_model import LogisticRegressionCV
model_cv = LogisticRegressionCV(10)
model_cv.fit(X_train, y_train)
y_predict = model_cv.predict(X_test)
y_predict.shape
test.shape
from sklearn.model_selection import cross_val_score
model = LogisticRegression(C=10)
scores = cross_val_score(model, X_train, y_train, cv=4)
scores
