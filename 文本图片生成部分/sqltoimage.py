
import pymysql

def getimage(id):

    conn = pymysql.connect(host='dltrade308.mysql.rds.aliyuncs.com', port=3306, user='report', password='x3m0u8X#M)U*',
                               database='reportdata', charset='utf8mb4')
    cursor = conn.cursor()
    sql1 = "select * from macro_report_graph_date where id = {}"
    sql = sql1.format(id)

    cursor.execute(sql)

    data = cursor.fetchall()
    conn.commit()
    path = "./"#图片地址为当前目录
    for i in range(len(data)):
        f = open(path+"%s.jpg" % data[i][0], 'wb')
        f.write(data[i][1])

if __name__ == '__main__':
    getimage(1)#test