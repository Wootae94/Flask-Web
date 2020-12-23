import sqlite3

def get_covid_daily(date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    stdDay = (date,)
    sql_select = 'select * from daily where stdDay= ?;'
    cur.execute(sql_select, stdDay)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_agender_daily(date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    createDt = (date,)
    sql_select = 'select * from agender where createDt= ?;'
    cur.execute(sql_select, createDt)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def write_covid_daily(params):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    sql_insert = '''insert into daily (stdDay, deathCnt, defCnt, gubun, incDec, isolClearCnt,
isolIngCnt, localOccCnt, overFlowCnt, qurRate) values(?,?,?,?,?,?,?,?,?,?);
'''
    cur.execute(sql_insert, params)
    conn.commit()
    cur.close()
    conn.close()

def write_covid_agender(params):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    sql_insert = 'insert into agender(createDt,gubun,confCase,confCaseRate,death,deathRate,criticalRate) values(?,?,?,?,?,?,?)'
    cur.execute(sql_insert, params)
    conn.commit()
    cur.close()
    conn.close()

def get_region_offset(region):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    gubun = (region,)
    sql_select = 'select count(*) from daily where gubun=?'
    cur.execute(sql_select, gubun)
    row = cur.fetchone()
    offset = row[0]
    return offset

def get_covid_region(region,offset):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    params = (region,offset)
    sql_select = 'select * from daily where gubun= ? order by stdDay limit 10 offset ?'
    cur.execute(sql_select, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_region_list():
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    sql_select = 'select DISTINCT gubun from daily'
    cur.execute(sql_select)
    rows = cur.fetchall()
    region_list = []
    for row in rows:
        region_list.append(row[0])
    
    return region_list