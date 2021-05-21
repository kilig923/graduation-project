import openpyxl
import os
import pymysql
from module_choose import ModuleType   #自定义模板类函数
from report_sentence_generation2 import remakeSentence
import runSql as rs


# for i in range(229,100000):
for i in range(293584,297463):  #分省份数据设计报告部分 reportId为152
#for i in range(1576079,1700772):
    sql = "SELECT * FROM macro_child_report_module_indicator_date WHERE id = '%d'" % i
    try:
         # 返回查询得到的文本和其它内容 并保存为元组
        result = rs.SuccessSql(sql, isSelect=True)[0]
    except:
        print("notfound: module indicatorId"+str(i))
        continue
    print(result)
    matchId=i
    moduleId=result['moduleId']
    reportName=result['moduleName']
    indicatorId=result['indicatorId']
    datarange=result['datarange']
    subIndicatorList=result['subIndicatorList']
    enddate=result['date']
    indexFreq=result['indexFreq']
    area=result['area']
    # if(area!='230281'):
    #     continue

    subIndicatorList = subIndicatorList[1:len(subIndicatorList) - 1]
    ind_id=subIndicatorList.split(':')[0]
    ind_Duration = subIndicatorList.split(':')[1]
    firsttime = ind_Duration[:10].replace('.', '-')
    lasttime = ind_Duration[11:].replace('.', '-')

    sql = "SELECT * FROM macro_economic_child_indicator WHERE id = "+str(ind_id)
    try:
        result = rs.SuccessSql(sql, isSelect=True)[0]  # 返回查询得到的文本和其它内容 并保存为元组
    except:
        print("notfounddata: indicatorId = " + str(ind_id))
        continue

    word = []
    number = []
    #print(result)


    if(datarange<3):
        m = ModuleType(word, number, result,datarange,area)  # 初始化模板类
        text,word,number=m.module1()
    elif(datarange==3 or datarange==4):
        m = ModuleType(word, number, result, datarange,area)  # 初始化模板类
        if(i%2==0):text, word, number = m.module2()
        else:text, word, number = m.module3()
    else:
        m = ModuleType(word, number, result, datarange,area)  # 初始化模板类
        if(i%12==0):text, word, number = m.module4()
        elif (i % 12 == 1):text, word, number = m.module5()
        elif (i % 12 == 2):text, word, number = m.module6()
        elif (i % 12 == 3):text, word, number = m.module7()
        elif (i % 12 == 4):text, word, number = m.module8()
        elif (i % 12 == 5):text, word, number = m.module9()
        elif (i % 12 == 6):text, word, number = m.module10()
        elif (i % 12 == 7):text, word, number = m.module11()
        elif (i % 12 == 8):text, word, number = m.module12()
        elif (i % 12 == 9):text, word, number = m.module13()
        elif (i % 12 == 10):text, word, number = m.module14()
        elif (i % 12 == 11):text, word, number = m.module15()
    print(text, word, number)


    sql0="update macro_child_report_module_indicator_date set analysisText='%s' where id = '%s'"\
        %(text,matchId)
    print(sql0)
    rs.SuccessSql(sql0, isSelect=False)
    # resFile = "./macro_child_report_module_indicator_date_updateSqlreport.txt"
    # resultFile = open(resFile, 'a', encoding='utf-8', errors='ignore')
    # resultFile.write(sql0 + ';' + "\n")

    lennumber = len(number)
    for j in range(lennumber):
        name = 'number' + str(j + 1)
        expression = number[j].strip(' ').strip('\'')
        type = 1
        sql = "insert into macro_child_report_calculate_exp_date " \
              "(matchId,seq,type,name,expression) values ('%s','%s','%s','%s','%s')" % (
                  matchId, str(j + 1), type, name, expression)
        print(sql)
        rs.RunSql_data(sql, isSelect=False)

    lenword = len(word)
    for j in range(lenword):
        name = 'word' + str(j + 1)
        expression = word[j].strip(' ').strip('\'')
        type = 2
        sql = "insert into macro_child_report_calculate_exp_date " \
              "(matchId,seq,type,name,expression) values ('%s','%s','%s','%s','%s')" % (
                  matchId, str(j + 1), type, name, expression)
        print(sql)
        rs.RunSql_data(sql, isSelect=False)

    remakeSentence(i)


