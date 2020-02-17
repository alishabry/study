import pandas as pd
import numpy as np
import time

with open('config.txt') as conf:
    conf = conf.readlines()
dataFileName = conf[0].split("'")[1]
statisticsFileName = conf[1].split("'")[1]
tableFileName = conf[2].split("'")[1]


def read(name):
    with open(name) as f:
        f = f.readlines()
    data = []
    c = len(f[3].split('\t'))
    for line in f:
        a = line
        b = a.split('\t')
        if len(b)== c:
            data.append([b[1],int(b[15])])
    return pd.DataFrame(data)

def stat(df):
    d = df[1]
    return [df[0].unique()[0],'min = ' + str(d.min()),' 50% = ' + str(round(d.quantile(q=0.5),2)),' 90% = ' +
            str(round(d.quantile(q=0.9))),' 99% = ' + str(round(d.quantile(q=0.99))),' 99.9% = ' + str(round(d.quantile(q=0.999)))]

def bounds(df):
    t = df[1]
    if t.min()%5!=0:
        tmin = t.min()-t.min()%5+5
    else:
        tmin = t.min()
    if t.max()%5!=0:
        tmax = t.max()-t.max()%5+5
    else:
        tmax = t.max()
    return [tmin,tmax]

def createTable(df,bound):
    k = np.array(df)
    table = []
    for i in range(bound[0],bound[1]+5,5):
        x1 = k[k[:,1]>i-5]
        x2 = len(x1[x1[:,1]<=i])
        if x2 == 0:
            continue
        table.append([i,x2,round(x2/len(k),2)*100,round(x2/len(k[k[:,1]<=i]),2)*100])
    return pd.DataFrame(table,columns = ['ExecTime','TransNo','Weight,%','Percent'])



def main(dn = dataFileName,stn = statisticsFileName ,tn = tableFileName):
    a = time.time()
    try:
        v = read(dn)
        st, tb = [],[]
        for i in v[0].unique():
            v1 = v[v[0] == i]
            st.append(stat(v1))
            createTable(v1,bounds(v1)).to_html(tn.split('.')[0]+
                                               i+'.'+tn.split('.')[1],header=True)
        np.savetxt(stn, st, fmt = '%s')
        print('--STATISTICS SAVED--')
        print(str(round((time.time()-a)/60,2))+' min')
    except FileNotFoundError:
        print('error: Нет файла с таким названием')
    except IndexError:
        print('error: Неверное представление данных')

main(dataFileName,statisticsFileName,tableFileName)



