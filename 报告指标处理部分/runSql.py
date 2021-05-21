import pymysql


# 连接配置信息
config = {
        #本地服务器
        'host':'localhost',
        'port':3306,
        'user':'root',
        'passwd':'123456',
        'db':'macrodata',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
}



config_data = {
        #本地服务器
        'host':'localhost',
        'port':3306,
        'user':'root',
        'passwd':'123456',
        'db':'macrodata',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
}



# 处理可能丢失链接
def SuccessSql(sql, isSelect = True):
    print("SQL: ", sql)
    try:
        return RunSql(sql, isSelect)
    except Exception:
        return SuccessSql(sql, isSelect)


# 执行sql语句
def RunSql(sql, isSelect = True):
    # print("SQL: ", sql)
    # 创建连接
    con = pymysql.connect(**config)
    con.ping(reconnect=True)
    cursor = con.cursor()
    cursor.execute(sql)
    if isSelect is True:  #select 查询数据
        result = cursor.fetchall()
        # print("selectCount: " + str(cursor.rowcount))
        cursor.close()
        con.close()
        return result
    else:                   #insert插入数据
        # print("affectCount: " + str(cursor.rowcount))
        con.commit()
        cursor.close()
        con.close()


# 执行sql语句
def RunSql_data(sql, isSelect = True):
    print("SQL: ", sql)
    # 创建连接
    con = pymysql.connect(**config_data)
    con.ping(reconnect=True)
    cursor = con.cursor()
    cursor.execute(sql)
    if isSelect is True:
        result = cursor.fetchall()
        print("selectCount: " + str(cursor.rowcount))
        cursor.close()
        con.close()
        return result
    else:
        print("affectCount: " + str(cursor.rowcount))
        con.commit()
        cursor.close()
        con.close()


# 执行sql语句
def RunManySql(sql, data, isSelect = True):
    # print("SQL: ", sql)
    # print("DATA: ", data)
    # 创建连接
    con = pymysql.connect(**config)
    con.ping(reconnect=True)
    cursor = con.cursor()
    cursor.executemany(sql, data)
    if isSelect is True:
        result = cursor.fetchall()
        # print("selectCount: " + str(cursor.rowcount))
        cursor.close()
        con.close()
        return result
    else:
        # print("affectCount: " + str(cursor.rowcount))
        con.commit()
        cursor.close()
        con.close()
