import runSql as rs


if __name__ == "__main__":
    #16663
    #45222
    for i in range(16663,20000):
        sql = "SELECT * FROM macro_child_report_category WHERE id = '%d'" % i
        try:
            result = rs.SuccessSql(sql, isSelect=True)[0]  # 返回查询得到的文本和其它内容 并保存为元组
        except:
            print("notfound: report category" + str(i))
            continue

        reportName = result['reportName']
        reportId = result['reportId']
        indexFreq = result['indexFreq']
        area = result['area']

        sql = "SELECT * FROM macro_child_report_module_indicator WHERE moduleId = '%s' and area='%s' and isnull=0 " \
              "order by dataDuration asc" % (reportId, area)
        try:
            indicatorData = rs.SuccessSql(sql, isSelect=True)  # 返回查询得到的文本和其它内容 并保存为元组
        except:
            print("notfounddata: indicatorId = " + str(reportId))
            continue
        else:
            if (len(indicatorData) == 0):
                continue
            dataDuration = indicatorData[0]['dataDuration']
            print(dataDuration)
            timeList = dataDuration.split('-')
            firsttime = timeList[0] + '-' + timeList[1] + '-' + timeList[2]
            lasttime = timeList[3] + '-' + timeList[4] + '-' + timeList[5]
            print(firsttime,lasttime)
            print(indexFreq)
            longyear = firsttime[:4]     #取最久的时间的年份

            # 时间频率为年
            if (indexFreq == '1'):
                for yearrange1 in range(int(longyear), 2021):
                    sql = "insert into macro_child_report_category_date (reportName,reportId,date," \
                          "indexFreq,area) values ('%s',%s,'%s','%s','%s')" \
                          % (reportName, reportId, yearrange1, indexFreq, area)
                    print(sql)

                    resFile = "./macro_child_report_category_date_insertSql4.txt"
                    resultFile = open(resFile, 'a', encoding='utf-8', errors='ignore')
                    resultFile.write(sql + ';' + "\n")

            # 时间频率为季度
            elif (indexFreq == '3'):
                for yearrange3 in range(int(longyear) + 1, 2021):
                    if (len(firsttime) < 10 or len(lasttime) < 10):
                        monthList3 = ['3', '6', '9', '12']
                    else:
                        monthList3 = ['03', '06', '09', '12']
                    for month3 in monthList3:
                        data3 = str(yearrange3) + '-' + str(month3)
                        print(data3)
                        sql = "insert into macro_child_report_category_date (reportName,reportId,date," \
                              "indexFreq,area) values ('%s',%s,'%s','%s','%s')" \
                              % (reportName, reportId, data3, indexFreq, area)
                        print(sql)

                        resFile = "./macro_child_report_category_date_insertSql4.txt"
                        resultFile = open(resFile, 'a', encoding='utf-8', errors='ignore')
                        resultFile.write(sql + ';' + "\n")

            # 时间频率为月度
            elif (indexFreq == '4'):
                lastyear = lasttime[:4]
                for yearrange4 in range(int(longyear) + 1, 2021):
                    if (len(firsttime) < 10 or len(lasttime) < 10):
                        monthList4 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                    else:
                        monthList4 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                    for month4 in monthList4:
                        data4 = str(yearrange4) + '-' + str(month4)
                        sql = "insert into macro_child_report_category_date (reportName,reportId,date," \
                              "indexFreq,area) values ('%s',%s,'%s','%s','%s')" \
                              % (reportName, reportId, data4, indexFreq, area)
                        print(sql)

                        resFile = "./macro_child_report_category_date_insertSql4.txt"
                        resultFile = open(resFile, 'a', encoding='utf-8', errors='ignore')
                        resultFile.write(sql + ';' + "\n")




