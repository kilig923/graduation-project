import runSql as rs

#94954
#189037
for i in range(94954,100000):
    sql = "SELECT * FROM macro_child_report_module_indicator WHERE id = '%d'" % i
    try:
        result = rs.SuccessSql(sql, isSelect=True)[0]  # 返回查询得到的文本和其它内容 并保存为元组
    except:
        print("notfound: module indicatorId"+str(i))
        continue

    moduleId=result['moduleId']
    moduleName=result['moduleName']
    indicatorId=result['indicatorId']
    indicatorLevel=result['indicatorLevel']
    indicatorName=result['indicatorName']
    indexFreq=result['indexFreq']
    dataDuration=result['dataDuration']
    datanum=result['datanum']
    area=result['area']
    isnull=result['isnull']

    #为空的情况，即所有的数据都为空，直接不要该叶子结点，在生成文本时直接忽略
    if(isnull==1):
        continue
    if(area=='常住'):
        continue

    timeList = dataDuration.split('-')
    firsttime = timeList[0] + '-' + timeList[1] + '-' + timeList[2]
    lasttime = timeList[3] + '-' + timeList[4] + '-' + timeList[5]
    if (firsttime == lasttime):
        sql = "SELECT * FROM macro_economic_child_data_raw WHERE indicatorId = '%s' and dataDate='%s' and area='%s'" \
              % (indicatorId, firsttime, area)
    else:
        sql = "SELECT * FROM macro_economic_child_data_raw WHERE indicatorId = '%s' and dataDate>='%s' " \
              "and dataDate<='%s' and area='%s' order by dataDate asc" \
              % (indicatorId, firsttime, lasttime, area)
    try:
        indicatorData = rs.SuccessSql(sql, isSelect=True)  # 返回查询得到的文本和其它内容 并保存为元组
    except:
        print("notfounddata: indicatorId = " + str(indicatorId))
        continue
    else:
        ind_firsttime = firsttime
        ind_lasttime = ''
        datarange = 0
        reslen = len(indicatorData)
        for i in range(reslen):
            datarange = datarange + 1
            ind_lasttime = indicatorData[i]['dataDate']
            subindicatorList = '[' + str(indicatorId) + ':' + ind_firsttime + '-' + ind_lasttime + ']'
            sql = "insert into macro_child_report_module_indicator_date (moduleId,moduleName,indicatorId,datarange,subindicatorList," \
                  "date,isDelete,indexFreq,area) values (%s,'%s',%s,%s,'%s','%s',0,'%s','%s')" \
                  % (moduleId, moduleName, indicatorId, datarange, subindicatorList, ind_lasttime, indexFreq, area)
            print(sql)
            resFile = "./macro_child_report_module_indicator_date_insertSql11.txt"
            resultFile = open(resFile, 'a', encoding='utf-8', errors='ignore')
            resultFile.write(sql + ';' + "\n")





