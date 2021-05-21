import runSql as rs


for i in range(94968,351043):
    # 最开始从map中找出所有的叶子指标==我们所需的所有叶子指标
    # 1.2.3.4-指标源的指标需要indicatorId和area两个变量才能获得所有指标的数据
    sql = "SELECT * FROM macro_economic_child_map WHERE id = '%d'" % i
    try:
        result = rs.SuccessSql(sql, isSelect=True)[0]  # 返回查询得到的文本和其它内容 并保存为元组
    except:
        print("notfound: childindicatorId = '%d'", i)
        continue

    indicatorId=result['childindicatorId']
    childindexName=result['childindexName']
    childlevel=result['childlevel']
    dataSource=result['dataSource']
    area=result['area']
    dataduration=result['dataduration']

    if(dataduration == None):
        continue
    #从macro_economic_child_indicator中获得叶子指标的指标时间频率和父节点（最后的文本大标题）
    sql = "SELECT parentId,indexFreq FROM macro_economic_child_indicator WHERE id = " + str(indicatorId)
    try:
        result = rs.SuccessSql(sql, isSelect=True)[0] # 返回查询得到的文本和其它内容 并保存为元组
    except:
        print("not found parentid: indicatorId = "+str(indicatorId))
        continue
    else:
        indexFreq=result['indexFreq']
        parentId=result['parentId']
        sql = "SELECT indexName FROM macro_economic_child_indicator WHERE id = " + str(parentId)
        try:
            result = rs.SuccessSql(sql, isSelect=True)[0] # 返回查询得到的文本和其它内容 并保存为元组
        except:
            print("not found parentIndex: indicatorId = "+str(indicatorId))
            continue
    parentindex=result['indexName']
    #print(parentId,parentindex,indexFreq)

    # 由于更新数据后 所有area为Null的指标都被标记上-1 所以直接查询更方便
    # 此处对dataDuration和datanum进行计算
    sql = "SELECT * FROM macro_economic_child_data_raw WHERE indicatorId = " + str(
        indicatorId) + " and area='" + area + "' order by dataDate desc"
    try:
        result = rs.SuccessSql(sql, isSelect=True)  # 返回查询得到的文本和其它内容 并保存为元组
    except:
        print("notfounddata: indicatorId = %d,area = %s", indicatorId, area)
        continue
    else:
        if (len(result) == 0):
            # 没有数据的情况
            sql = "insert into macro_child_report_module_indicator (moduleId,moduleName,indicatorId,indicatorLevel," \
                  "indicatorName,indexFreq,datanum,isDelete,isnull,area) values (%s,'%s',%s,'%s','%s','%s',0,0,1,'%s')" \
                  % (parentId, parentindex, indicatorId, childlevel, childindexName, indexFreq, area)
        else:
            datanum = 0
            reslen = len(result)
            firsttime = ''  # 最开始把区间两端数据firsttime/lasttime设置为空
            lasttime = ''
            for i in range(reslen):
                if (result[i]['data'] != None):  # 记录第一个非空数据的时间
                    lasttime = result[i]['dataDate']
                    j = 0
                    for j in range(i, reslen):
                        if (result[j]['data'] != None):  # 记录第二个非空数据的时间
                            firsttime = result[j]['dataDate']
                            datanum = datanum + 1
                        else:
                            break
                    break
            # print(datanum, firsttime, lasttime)
            if (datanum == 0):
                # 数据全部为Null（为空）的情况
                sql = "insert into macro_child_report_module_indicator (moduleId,moduleName,indicatorId,indicatorLevel," \
                      "indicatorName,indexFreq,datanum,isDelete,isnull,area) values (%s,'%s',%s,'%s','%s','%s',0,0,1,'%s')" \
                      % (parentId, parentindex, indicatorId, childlevel, childindexName, indexFreq, area)
            else:
                dataDuration = firsttime + '-' + lasttime
                sql = "insert into macro_child_report_module_indicator (moduleId,moduleName,indicatorId,indicatorLevel," \
                      "indicatorName,indexFreq,datanum,dataDuration,isDelete,isnull,area) values (%s,'%s',%s,'%s','%s','%s',%s,'%s',0,0,'%s')" \
                      % (
                      parentId, parentindex, indicatorId, childlevel, childindexName, indexFreq, datanum, dataDuration,
                      area)
    print(sql)



    resFile = "./macro_child_report_module_indicator_insertSql2.txt"
    resultFile = open(resFile, 'a', encoding='utf-8', errors='ignore')
    resultFile.write(sql + ';' + "\n")


