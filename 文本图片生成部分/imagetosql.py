import sys
import pymysql
from PIL import Image
import os


def image_to_sql(id, filename):
    path = "./指标-年度-图片生成/" + filename + ".png"
    print(path)
    # 读取图片文件
    fp = open(path, 'rb')
    img = fp.read()
    fp.close()


    # 建立一个MySQL连接

    database = pymysql.connect(host='dltrade308.mysql.rds.aliyuncs.com', port=3306, user='report', passwd='x3m0u8X#M)U*', db='reportdata', charset='utf8mb4')
    # 存入图片
    # 创建游标
    cursor = database.cursor()
    # 注意使用Binary()函数来指定存储的是二进制
    sql = "INSERT INTO macro_child_report_graph_date (image,moduleId) VALUES  (%s,%s);"
    args=(img,id)
    try:
        cursor.execute(sql,args)
        print("============")
        print(id, "insert sql done")
    except Exception as e:
        print(e)
        os._exit()
    database.commit()
    # 关闭游标
    cursor.close()
    # 关闭数据库连接
    database.close()

