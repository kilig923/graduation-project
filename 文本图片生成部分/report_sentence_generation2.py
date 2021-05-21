#! /usr/bin/env python
# -*-coding:utf-8-*-
import re
import traceback
import runSql as rs


# ============================================ 获取原始数据材料 ====================================================


# # 得到条目对应期数
# def getIndexTime(subIndicatorList):
#     """
#     得到条目对应期数
#     :param subIndicatorList: 包括的叶子指标ID列表. 指标ID : time的形式存放
#     :return: 对应期数
#     """
#     sub_indicator_list = subIndicatorList[1:len(subIndicatorList)-1].split(",")
#     return sub_indicator_list[0].split(":")[1]


# 获取两个时间之间的 对应频度 期数  date1为{'y':, 'm':, 'd':}
def getCountDuration(date1, date2, indexFreq):
    y1 = int(date1['y'])
    m1 = int(date1['m'])
    y2 = int(date2['y'])
    m2 = int(date2['m'])
    if y1 == y2 and m1 == m2:  # 同年月
        return 0  # 0期
    if int(indexFreq) == 1:  # 年
        return y2-y1
    if int(indexFreq) == 3:  # 季
        if y1 == y2:
            return (m2-m1)/3  # 月份3为一季
        count = m2/3  # 本年季度数
        count += (y2-y1-1)*4  # 跨过的整年 4季
        count += (12-m1)/3  # 第一年后面的季度数
        return count
    if int(indexFreq) == 4:  # 月
        if y1 == y2:
            return m2-m1  # 本年 月份数
        count = m2  # 本年月度数
        count += (y2-y1-1)*12  # 跨过的整年 12月
        count += 12-m1  # 第一年后面的月度数
        return count


# 传入指定跨度、总跨度，返回截取的期数、末尾不要的期数
#用来计算截取的时间和数据 目前无用 保留
def getListBydateDuration(dateList, dataDurationList, indexFreq):
    # print("时间跨度:", dateList)
    splitTxt = '&&'  # 初始设置一个不可能分割的，如果下面不匹配则一定出错终止文本替换
    if dateList[0].find('.') != -1:
        splitTxt = '.'
    elif dateList[0].find('-') != -1:
        splitTxt = '-'
    # 指定时间跨度
    dateList0 = dateList[0].split(splitTxt)
    date0 = {'y': dateList0[0], 'm': dateList0[1], 'd': dateList0[2]}
    dateList1 = dateList[1].split(splitTxt)
    date1 = {'y': dateList1[0], 'm': dateList1[1], 'd': dateList1[2]}
    dateDuration1 = [date0, date1]
    # 总跨度
    dateList0 = dataDurationList[0].split('-')
    date0 = {'y': dateList0[0], 'm': dateList0[1], 'd': dateList0[2]}
    dateList1 = dataDurationList[1].split('-')
    date1 = {'y': dateList1[0], 'm': dateList1[1], 'd': dateList1[2]}
    dateDuration2 = [date0, date1]
    # print("句中时间跨度:", dateDuration1, "总跨度:", dateDuration2)
    # 是否超出总跨度
    if dateDuration1[0]['y'] < dateDuration2[0]['y']:
        dateDuration1[0] = dateDuration2[0]  # 设为与总跨度开始时间一致
    elif dateDuration1[0]['y'] == dateDuration2[0]['y'] and dateDuration1[0]['m'] < dateDuration2[0]['m']:
        dateDuration1[0] = dateDuration2[0]  # 设为与总跨度开始时间一致
    elif dateDuration1[0]['y'] == dateDuration2[0]['y'] and dateDuration1[0]['m'] == dateDuration2[0]['m'] and dateDuration1[0]['d'] < dateDuration2[0]['d']:
        dateDuration1[0] = dateDuration2[0]  # 设为与总跨度开始时间一致

    if dateDuration1[1]['y'] > dateDuration2[1]['y']:
        dateDuration1[1] = dateDuration2[1]  # 设为与总跨度结束时间一致
    elif dateDuration1[1]['y'] == dateDuration2[1]['y'] and dateDuration1[1]['m'] > dateDuration2[1]['m']:
        dateDuration1[1] = dateDuration2[1]  # 设为与总跨度结束时间一致
    elif dateDuration1[1]['y'] == dateDuration2[1]['y'] and dateDuration1[1]['m'] == dateDuration2[1]['m'] and dateDuration1[1]['d'] > dateDuration2[1]['d']:
        dateDuration1[1] = dateDuration2[1]  # 设为与总跨度结束时间一致
    # print("待取跨度:", dateDuration1[0], "~", dateDuration1[1])

    issueNeedCount = getCountDuration(dateDuration1[0], dateDuration1[1], indexFreq)+1  # 需取出的期数 加上本身时间点也算一期
    issueEndCount = getCountDuration(dateDuration1[1], dateDuration2[1], indexFreq)  # 尾部无需的期数 不用加上结尾时间点
    # print("需取出的期数:", issueNeedCount, "尾部无需的期数", issueEndCount)

    return issueNeedCount, issueEndCount

def getList(indicatorData):
    dateList=[]
    dataList=[]
    gapList=[]
    changeRateList=[]
    #avg 为str
    sum=0
    datalen=len(indicatorData)
    for i in range(datalen):
     #   print(indicatorData[i])
        datestr0 = str(indicatorData[i]['dataDate'])
        datastr0 = str(indicatorData[i]['data'])
        dateList.append(datestr0)
        dataList.append(datastr0)
        sum = sum + float(indicatorData[i]['data'])
        if(i>0):
            data2 = float(indicatorData[i]['data'])
            data1 = float(indicatorData[i - 1]['data'])
 #           print(data2, data1)
            gap = round(data2 - data1, 4)
            if(data1==0.0):
                changeRate=0
            else:
                changeRate = round((gap / data1)*100,4)

            gapstr0=str(gap)
            changeRatestr0=str(changeRate)+'%'

            gapList.append(gapstr0)
            changeRateList.append(changeRatestr0)
    avg=0
    if(datalen!=0):
        avg=sum/datalen
    return dateList,dataList,gapList,changeRateList,avg



# 待改，目前不同数据数据标记日期可能不一致
def getIndicatorData(matchId, subIndicatorList,area):  # , indexCount:param indexCount: 期数
    """
    获取末端指标信息
    :param subIndicatorList: subIndicatorList字段内容
    :return: 指标信息
    """
    #对该处代码进行修改,主要目的位重新提取indicatorName所需用到的指标名列表和指标数据
    indexList = []      #indicatorName 所有用到的指标名列表
    dataList = []
    gapList = []
    changeRateList = []
    avgList = []
    dateList = []
    indexFreqList = []
    indicatorData = []
    subIndicatorList = subIndicatorList[1:len(subIndicatorList)-1].split(",")   #将所有时间区间分为一个id对应一个时间区间 保存为列表
    #ind所保存的列表的数据的格式为 [1015:2000.12.31-2019.12.31] 形式
    for ind in subIndicatorList:
        # 获取该标签名、数值信息(针对每一个指标进行处理)
        ind_id = ind.split(":")[0].strip('[').strip(']').strip('-').strip('(').strip(')')\
            .strip('}').strip('{').strip(',').strip('.').strip(';')  # 处理可能出现的拼写错误如 [18177 移除头尾的指定字符
        ind_Duration=ind.split(":")[1]
        firsttime = ind_Duration[:10].replace('.', '-')
        lasttime = ind_Duration[11:].replace('.', '-')
        try:
            sql = "select indexName,indexFreq from macro_economic_child_indicator where id = " + ind_id
            indexList.append(rs.SuccessSql(sql, isSelect=True)[0]["indexName"])
            indexFreqList.append(rs.SuccessSql(sql, isSelect=True)[0]["indexFreq"])
        except Exception as e:
            sql0 = "update macro_child_report_module_indicator_date set " \
                   "note = '获取 macro_economic_indicator表 id=" + ind_id + " 指标名称失败，无该指标' where id = " + str(matchId)
            rs.SuccessSql(sql0, isSelect=False)
        else:  #没有获取指标名的异常则继续执行
            #如下函数主要目的为获取dateList、dataList、gapList、changeRateList、indexFreq、avgStr
            try:#时间区间为左闭右闭区间
                if (firsttime == lasttime):
                    sql = "SELECT * FROM macro_economic_child_data_raw WHERE indicatorId = '%s' and" \
                          " dataDate='%s' and area='%s'" % (ind_id, firsttime,area)
                else:
                    sql = "SELECT * FROM macro_economic_child_data_raw WHERE indicatorId = '%s' and " \
                        "dataDate>='%s' and dataDate<='%s' and area='%s' order by dataDate asc" % \
                        (ind_id, firsttime, lasttime, area)
                indicatorData = rs.SuccessSql(sql, isSelect=True)
            except Exception as e:  #错误异常并填入数据库中记录
                sql0 = "update macro_child_report_module_indicator_date set " \
                       "note = '获取 macro_economic_child_data_raw indicatorId="+ind_id+" 各项数据失败，数据缺失' where id = "+str(matchId)
                rs.SuccessSql(sql0, isSelect=False)
            # 时间列表、初值列表、差值列表、变化率列表、均值列表 返回的值都为列表
            dateList0, dataList0, gapList0, changeRateList0, avg0 = getList(indicatorData)

            dateList.append(dateList0)
            dataList.append(dataList0)
            gapList.append(gapList0)  # 差值、变化率少一期
            changeRateList.append(changeRateList0)
            avgList.append(avg0)
    return indexList, dataList, gapList, changeRateList, avgList, dateList, indexFreqList




# ============================================ 获取数值 ====================================================


# 获取对应数值字符串  原数值 / 绝对值
def getDataX(dataXstr, dataList):
    """
    返回对应数据标记的对应值
    :param dataXstr: 数值表达式 a_data7
    :param dataList: 初值列表
    :return:
    """
   # print("dataXstr2:"+dataXstr)
    x = dataXstr.split("_data")[0]
    x_time = int(dataXstr.split("_data")[1])
    # print(x, x_time)
    try:
        dataText = dataList[ord(x)-ord('a')][x_time-1]
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getAbsDataX(dataXstr, dataList):
    """
    返回对应数据标记的对应值 绝对值  如：-9在文中需写作“下降9”此处数值需要绝对值表示。
    :param dataXstr: 数值表达式 a_data7
    :param dataList: 初值列表
    :return:
    """
    x = dataXstr.split("_data")[0]
    x_time = int(dataXstr.split("_data")[1])
    # print("x_time:", x, x_time)
    try:
        dataText = dataList[ord(x)-ord('a')][x_time-1]
        dec = dataText.find("-")
        if dec != -1:
            dataText = dataText[0:dec]+dataText[dec+1:len(dataText)]
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getGapX(gapXstr, gapList):
    """
    返回对应数据标记的对应值
    :param gapXstr: 表达式 a_gap6
    :param gapList: 差值列表
    :return:
    """
    x = gapXstr.split("_gap")[0]
    x_time = int(gapXstr.split("_gap")[1])
    try:
        dataText = gapList[ord(x)-ord('a')][x_time-1]
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getAbsGapX(gapXstr, gapList):
    """
    返回对应数据标记的对应值  绝对值  如：-9在文中需写作“下降9”此处数值需要绝对值表示。
    :param gapXstr: 表达式 a_gap6
    :param gapList: 差值列表
    :return:
    """
    x = gapXstr.split("_gap")[0]
    x_time = int(gapXstr.split("_gap")[1])
    # print(x, x_time)
    try:
        dataText = gapList[ord(x)-ord('a')][x_time-1]
        dec = dataText.find("-")
        if dec != -1:
            dataText = dataText[0:dec]+dataText[dec+1:len(dataText)]
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getChangeRateX(changeRateXstr, changeRateList):
    """
    返回对应数据标记的对应值
    :param changeRateXstr:
    :param changeRateList:
    :return:
    """
    x = changeRateXstr.split("_changeRate")[0]
    x_time = int(changeRateXstr.split("_changeRate")[1])
    try:
        dataText = changeRateList[ord(x)-ord('a')][x_time-1]
        # print(x, x_time, dataText)
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getAbsChangeRateX(changeRateXstr, changeRateList):
    """
    返回对应数据标记的对应值  绝对值  如：-9在文中需写作“下降9”此处数值需要绝对值表示。
    :param changeRateXstr: 表达式 a_changeRate6
    :param changeRateList: 变化率
    :return:
    """
    x = changeRateXstr.split("_changeRate")[0]
    x_time = int(changeRateXstr.split("_changeRate")[1])
    try:
        dataText = changeRateList[ord(x)-ord('a')][x_time-1]
        dec = dataText.find("-")
        if dec != -1:
            dataText = dataText[0:dec]+dataText[dec+1:len(dataText)]
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getAvg(avgXstr, avgList):
    """
    返回对应数据标记的对应值
    :param dataXstr:
    :param avgList:
    :return:
    """
    x = avgXstr.split("_avg")[0]
    try:
        dataText = avgList[ord(x)-ord('a')]  # avg无期数后缀
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getAbsAvg(avgXstr, avgList):
    """
    返回对应数据标记的对应值  绝对值  如：-9在文中需写作“下降9”此处数值需要绝对值表示。
    :param avgXstr: 表达式 a_avg6
    :param avgList: 变化率
    :return:
    """
    x = avgXstr.split("_avg")[0]
    try:
        dataText = avgList[ord(x)-ord('a')]  # avg无期数后缀
        dec = dataText.find("-")
        if dec != -1:
            dataText = dataText[0:dec]+dataText[dec+1:len(dataText)]
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getMax(maxXstr, dataList):
    """
    返回对应数据标记的对应值
    :param maxXstr:
    :param dataList:
    :return:
    """
    x = maxXstr.split("_max")[0]
    try:
        dataList0 = dataList[ord(x)-ord('a')]  # 取该指标的期内数据
        dataList0 = sorted(dataList0, reverse=True)  # 倒序排序
        return str(dataList0[0])
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getAbsMax(maxXstr, dataList):
    """
    返回对应数据标记的对应值
    :param maxXstr:
    :param dataList:
    :return:
    """
    x = maxXstr.split("_max")[0]
    try:
        dataList0 = dataList[ord(x)-ord('a')]  # 取该指标的期内数据
        dataList0 = sorted(dataList0, reverse=True)  # 倒序排序
        dataText = dataList0[0]
        dec = dataText.find("-")
        if dec != -1:
            dataText = dataText[0:dec]+dataText[dec+1:len(dataText)]
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getMin(minXstr, dataList):
    """
    返回对应数据标记的对应值
    :param minXstr:
    :param dataList:
    :return:
    """
    x = minXstr.split("_min")[0]
    try:
        dataList0 = dataList[ord(x)-ord('a')]  # 取该指标的期内数据
        dataList0 = sorted(dataList0)  # 升序排序
        return dataList0[0]
    except Exception:
        return "$$"  # 代替某指标没有数据的情况
def getAbsMin(minXstr, dataList):
    """
    返回对应数据标记的对应值
    :param minXstr:
    :param dataList:
    :return:
    """
    x = minXstr.split("_min")[0]
    try:
        dataList0 = dataList[ord(x)-ord('a')]  # 取该指标的期内数据
        dataList0 = sorted(dataList0)  # 升序排序
        dataText = dataList0[0]
        dec = dataText.find("-")
        if dec != -1:
            dataText = dataText[0:dec]+dataText[dec+1:len(dataText)]
        return dataText
    except Exception:
        return "$$"  # 代替某指标没有数据的情况


# 针对如：x_dataX、x_gapX、a_changeRateX、a_avg、a_max、a_min、numberX 单个词与纯数字
def getDataText(matchId, data_text, indexList, dataList, gapList, changeRateList, avgList):
  #  print("data_text1:"+data_text)
    if data_text.find("_data") != -1:   #x_dataX
        return getDataX(data_text, dataList)
    elif data_text.find("_gap") != -1:  #x_gapX
        return getGapX(data_text, gapList)
    elif data_text.find("_changeRate") != -1:   #a_changeRateX
        return getChangeRateX(data_text, changeRateList)
    elif data_text.find("_avg") != -1:      #a_avg
        return getAvg(data_text, avgList)
    elif data_text.find("_max") != -1:      #a_max
        return getMax(data_text, dataList)
    elif data_text.find("_min") != -1:      #a_min
        return getMin(data_text, dataList)
    elif data_text.find("number") != -1:  # 套表达式number 获取真表达式 一般没有 反正我是还没发现
        number_exp = getNumberWordExp(matchId, data_text)
        return getNumberExpInfo(matchId, number_exp, indexList, dataList, gapList, changeRateList, avgList)
    return data_text  # 对于纯数字的字符串表达式

def getAbsDataText(data_text, dataList, gapList, changeRateList, avgList):
    if data_text.find("_data") != -1:
        return getAbsDataX(data_text, dataList)
    elif data_text.find("_gap") != -1:
        return getAbsGapX(data_text, gapList)
    elif data_text.find("_changeRate") != -1:
        return getAbsChangeRateX(data_text, changeRateList)
    elif data_text.find("_avg") != -1:
        return getAbsAvg(data_text, avgList)
    elif data_text.find("_max") != -1:
        return getMax(data_text, dataList)
    elif data_text.find("_min") != -1:
        return getMin(data_text, dataList)
    return "data(abs) not found"


# 处理数据小数位 返回数值字符串
# 根据数据类型 保留小数点后四位小数 或把小数点后多余的0去掉
def resetFloat4(dataStr):
    dataStr=str(dataStr)
    minus_str = "-" if dataStr.find("-") != -1 else ""
    hund_str = "%" if dataStr.find("%") != -1 else ""
    dataList = dataStr.strip("-").strip("%").split(".")
    if len(dataList) > 1:  # 有小数位
        if dataList[1].count("0") == len(dataList[1]):  # 全是0
            # print(dataStr, "count(0):", dataList[1].count("0"), "len:", len(dataList[1]))
            dataList[1] = ""
        else:
            dataList[1] = dataList[1].rstrip("0")  # 小数位去末尾0
    else:  # 整数
        return dataStr
    # 处理小数位 >4
    if len(dataList[1]) > 0:
        if len(dataList[1]) > 4:  # 去0后有小数位 小数位>4位
            return minus_str+format(float(dataList[0]+"."+dataList[1]), '.4f')+hund_str
        else:  # 去0后有小数位 小数位<=4位
            return minus_str+str(float(dataList[0]+"."+dataList[1]))+hund_str
    else:  # 去0后无小数
        return minus_str+dataList[0]+hund_str


# 将数字字符串（包括百分率、普通小数字符串）转为等值小数数值
def getPrueData(data):
    if data.find("%") == -1:
        return float(data)
    data = data[0:len(data)-1]
    return float(data)/100


# ============================================ 获取时间 ====================================================


# 处理单个时间字符串 对具体的年、季、月的数据进行处理
def getTimeXText(m_str, dateList, indexFreqList):
    #获取时间timeX中的X
    m_time = int(m_str[4:len(m_str)])
    # print(dateList[0], m_time)
    try:
        timeList = dateList[0][m_time-1].split("-")   #默认选取第一个指标时间区间的时间列表 选取第X个数据 保存在列表中的第X-1个
        #print(timeList)··
    except Exception as e:  # 无法处理期数
        return "null"
    indexFreq = int(indexFreqList[0])                 #默认选取第一个指标的单位
    # print("timeX:", indexFreq, timeList)
    if indexFreq == 1:  # 1-年度 2-半年度 3-季度 4-月度
        return timeList[0]+"年"  # 纯年份的文本里无“年”，需要替换词补入
    elif indexFreq == 3:  # 1-年度 2-半年度 3-季度 4-月度
        if int(timeList[1]) in range(1, 4):
            return timeList[0]+"年第一季度"
        elif int(timeList[1]) in range(4, 7):
            return timeList[0]+"年第二季度"
        elif int(timeList[1]) in range(7, 10):
            return timeList[0]+"年第三季度"
        elif int(timeList[1]) in range(10, 13):
            return timeList[0]+"年第四季度"
    elif indexFreq == 4:  # 1-年度 2-半年度 3-季度 4-月度
        return timeList[0]+"年"+str(int(timeList[1]))+"月"



# 处理时间表达式，返回修改记录列表changeList  此处默认时间列表相同，取第一列表时间、频度做代表
def remakeTimeXASC(analysisText, changeList, dateList, indexFreqList):
    """
    处理时间表达式，返回修改记录列表changeList
    :param analysisText: 待解析文本
    :param changeList: 变化记录列表
    :param dateList: 时间列表
    :param indexFreqList: 频率列表
    :return: 变化记录列表
    """
    #对于[timeX]格式的时间的时间表达式的匹配
    p_timeX = re.compile("\[time\d+\]")
    for m in p_timeX.finditer(analysisText):
        # m.group(): 左右有"["、"]"
        # 获取单个时间点
        timeText = getTimeXText(m.group()[1:len(m.group())-1], dateList, indexFreqList)
        # 记录替换 id:起始位置；length：所需替换的长度；text：替换后的文本内容
        changeItem = {"id": m.start(), "length": len(m.group()), "text": timeText}
        changeList.append(changeItem)  #先记录所需替换的[timeX]
        # print(m.start(), m.group(), "->", timeText)
    #对于[timeX-timeY]格式的时间表达式的匹配
    p_timeX = re.compile("\[time\d+-time\d+\]")
    for m in p_timeX.finditer(analysisText):
        timeList = m.group()[1:len(m.group())-1].split("-")  # 去掉外套[]、分割两个时间
        timeText0 = getTimeXText(timeList[0], dateList, indexFreqList)
        timeText1 = getTimeXText(timeList[1], dateList, indexFreqList)
        timeText = timeText0+"至"+timeText1
        # 记录替换
        changeItem = {"id": m.start(), "length": len(m.group()), "text": timeText}
        changeList.append(changeItem)    #再记录所需替换的[timeX-timeY]
        # print(m.start(), m.group(), "->", timeText)
    return changeList



# ============================================ 处理计算式 number ====================================================


# 返回数值表达式的尾部内容 用于计算abc/numberX类
def getExpAndX(expression):
    data_i = expression.find("_data")
    if data_i != -1:
        return expression[data_i:len(expression)]
    data_i = expression.find("_gap")
    if data_i != -1:
        return expression[data_i:len(expression)]
    data_i = expression.find("_changeRate")
    if data_i != -1:
        return expression[data_i:len(expression)]
    data_i = expression.find("_avg")
    if data_i != -1:
        return expression[data_i:len(expression)]


# 处理数据表达式，返回修改记录列表changeList
def remakeXDataX(matchId, analysisText, changeList, indexList, dataList, gapList, changeRateList, avgList):
    #print(analysisText)
    p_dataX = re.compile("\[[a-z](_data|_gap|_changeRate|_avg|_max|_min)\d*\]")  # 中文[\u4E00-\u9FA5\(\{\[。，：；‘“’”\'\".,]
    for m in p_dataX.finditer(analysisText):
     #   print(m.group())
        m_len = len(m.group())
        m_str = m.group().replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '')
        # 获取数据，自动识别所属类 初值、差值、变化率 调整小数
    #    print(getDataText(matchId, m_str, indexList, dataList, gapList, changeRateList, avgList))
        dataText = resetFloat4(getDataText(matchId, m_str, indexList, dataList, gapList, changeRateList, avgList))
        # 记录替换
        changeItem = {"id": m.start(), "length": m_len, "text": dataText}
        changeList.append(changeItem)
    #    print(m.start(), m.group(), "->", dataText)
    return changeList

#此处的代码是要开始处理number相关啦！
# 获取number对应实际表达式，检查一层套娃（对于多个轮换套娃无法检查）
def getNumberWordExp(matchId, expression):
    print(expression)
    sql = "select * from macro_child_report_calculate_exp_date where " \
          "name = '"+expression+"' and matchId = "+str(matchId)+" and isDelete = 0 order by id desc"
    number_exp = rs.SuccessSql(sql, isSelect=True)[0]["expression"]
    if number_exp.find(expression) != -1:  # 查看返回表达式内是否套着表达式名称
        sql0 = "update macro_child_report_module_indicator_test set " \
               "note = '"+str(matchId)+"式子"+expression+"套娃' where id = "+str(matchId)
        rs.SuccessSql(sql0, isSelect=False)
        return None  # 表达式套娃错误。返回空诱导程序报错，终止此句文本替换
    else:
        return number_exp


def getNumberExpInfo(matchId, expression, indexList, dataList, gapList, changeRateList, avgList, needIndexName=False):
    """
    处理number系列计算式结果
    :param matchId: 句子id
    :param expression: 完整表达式
    :param dataList: 初值列表
    :param gapList: 差值列表
    :param changeRateList: 变化率列表
    :return: 结果字符串
    """
    expression = expression.replace(' ', '').replace('　', '').replace('(', '').\
        replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '')
    exp_list = expression.split(":")
  #  print("expression:", expression)
    # 表达式类型
    exp_type = int(exp_list[0])
    # 处理表达式
    data_text = exp_list[1]
    # 数值类型 1-初值 2-绝对值
    if len(exp_list) == 3:  # 表达式有第三部分表示标志位
        data_type_id = str(exp_list[2])
    else:  # 没有第三部分，默认为1
        data_type_id = "1"
    # 数据单值 x_dataX/x_gapX/x_changeRateX/x_avg
    if exp_type == 3:
        if data_type_id == "1":
            return resetFloat4(getDataText(matchId, data_text, indexList, dataList, gapList, changeRateList, avgList))
        if data_type_id == "2":
            return resetFloat4(getAbsDataText(data_text, dataList, gapList, changeRateList, avgList))
        if data_type_id == "3":
            dataStr = resetFloat4(getDataText(matchId, data_text, indexList, dataList, gapList, changeRateList, avgList))
            if dataStr.find("%") == -1:
                return resetFloat4(str(dataStr)) + "%"  # 换算等值
            else:
                return dataStr
    # 差值计算 (a_dataX - b_dataY)/(a_changeRateX - b_changeRateY)
    if exp_type == 4:
        data_text_list = data_text.replace(' ', '').replace('　', '').split("-")
        # print("[exp_type == 4]", data_text_list)
        # 获取数值字符串  处理 number-x_dataX情况 getDataText 处理x_dataX、number等
        data0_text = getDataText(matchId, data_text_list[0], indexList, dataList, gapList, changeRateList, avgList)
        data1_text = getDataText(matchId, data_text_list[1], indexList, dataList, gapList, changeRateList, avgList)
        if data0_text != "$$" and data1_text != "$$":
            # 字符串转浮点数 特殊处理百分率
            rate_flag = True if data0_text.find("%") != -1 else False
            # print("[exp_type == 4]", data0_text, data1_text)
            data0 = float(data0_text.strip('%'))/100 if rate_flag else float(data0_text)
            data1 = float(data1_text.strip('%'))/100 if rate_flag else float(data1_text)
            # 浮点数转字符串 特殊处理百分率 不会超出4位小数，且多余末尾0会在float过程去掉
            if data_type_id == "1":
                return resetFloat4(str((data0 - data1)*100))+"%" if rate_flag else resetFloat4(str(data0 - data1))
            if data_type_id == "2":  # 绝对值
                return resetFloat4(str((data0 - data1)*100)).strip("-")+"%" if rate_flag else resetFloat4(str(data0 - data1)).strip("-")
            if data_type_id == "3":  # 绝对值后折算成百分点形式
                return resetFloat4(str((data0 - data1)*100).strip("-")) if rate_flag else resetFloat4(str(data0 - data1)).strip("-")
        else:
            return "$$"
    # 求和计算 (a_dataX + b_dataY)
    if exp_type == 5:
        data_text_list = data_text.replace(' ', '').replace('　', '').split("+")
        # 获取数值字符串
        data0_text = getDataText(matchId, data_text_list[0], indexList, dataList, gapList, changeRateList, avgList)
        data1_text = getDataText(matchId, data_text_list[1], indexList, dataList, gapList, changeRateList, avgList)
        if data0_text != "$$" and data1_text != "$$":
            # 字符串转浮点数 特殊处理百分率
            rate_flag = True if data0_text.find("%") != -1 else False
            data0 = float(data0_text.strip('%'))/100 if rate_flag else float(data0_text)
            data1 = float(data1_text.strip('%'))/100 if rate_flag else float(data1_text)
            # 浮点数转字符串 特殊处理百分率  小数情况同 -
            if data_type_id == "1":
                return str((data0 + data1)*100)+"%" if rate_flag else str(data0 + data1)
            if data_type_id == "2":  # 绝对值
                return str((data0 + data1)*100).strip("-")+"%" if rate_flag else str(data0 + data1).strip("-")
        else:
            return "$$"
    # 变化率/比例计算 (a_dataX / b_dataY)
    if exp_type == 6:
        data_text_list = data_text.replace(' ', '').replace('　', '').split("/")
        # 获取数值字符串
        data0_text = getDataText(matchId, data_text_list[0], indexList, dataList, gapList, changeRateList, avgList)
        data1_text = getDataText(matchId, data_text_list[1], indexList, dataList, gapList, changeRateList, avgList)
        if data0_text != "$$" and data1_text != "$$":
            # 字符串转浮点数 特殊处理百分率
            rate_flag = True if data0_text.find("%") != -1 else False
            data0 = float(data0_text.strip('%'))/100 if rate_flag else float(data0_text)
            data1 = float(data1_text.strip('%'))/100 if rate_flag else float(data1_text)
            # 浮点数转字符串 特殊处理百分率 需处理小数位
            if data_type_id == "1":  # 默认值
                return resetFloat4(str((data0/data1)*100))+"%" if rate_flag else str(data0/data1)
            if data_type_id == "2":  # 折算成百分率形式：xx%
                return resetFloat4(str((data0/data1)*100))+"%"
            if data_type_id == "3":  # 折算成百分点形式：例如23.7% -> 23.7
                return resetFloat4(str(data0/data1))*100
            if data_type_id == "4":  # 折算成比例形式：xx : 100 （例如表示男女比例时、同比环比时）
                return resetFloat4(str((data0/data1)*100))+" : 100"
            if data_type_id == "5":  # 折算成千分率形式：
                return resetFloat4(str((data0/data1)*1000))+"‰"
            if data_type_id == "6":  # 折算成千分点形式：
                return resetFloat4(str((data0/data1)*1000))
            if data_type_id == "7":  # 折算成万分率形式：
                return resetFloat4(str((data0/data1)*10000))+"‱"
            if data_type_id == "8":  # 折算成万分点形式：
                return resetFloat4(str((data0/data1)*10000))
        else:
            return "$$"
    # bcdef/a_dataX类
    if exp_type == 7:
        # 切割 bcdef / a_dataX  abcdef 代表指标
        data_text_divide = data_text.split("/")
        # print("data_text_divide:", data_text_divide)
        fin_text = ""
        # 切割后缀 补上期数 X
        if data_text.find("_data") != -1:
            fin_text = "_data"+data_text.split("_data")[1]
        elif data_text.find("_gap") != -1:
            fin_text = "_gap"+data_text.split("_gap")[1]
        elif data_text.find("_changeRate") != -1:
            fin_text = "_changeRate"+data_text.split("_changeRate")[1]
        elif data_text.find("_avg") != -1:
            fin_text = "_avg"  # avg无期数
        resultList = []  # 存放计算结果数值
        child_str = data_text_divide[0]  # 'bcdef'串
        # 获取a_dataX数值字符串
        a_data_text = getDataText(matchId, "a"+fin_text, indexList, dataList, gapList, changeRateList, avgList)
        if a_data_text == "$$":  # a无数值
            return None
        # print("indexList:", indexList)
        # 获取 bef_dataX 数值字符串 并计算/a结果 并处理百分率 存放resultList
        for i in range(0, len(child_str)):  # 'bdf' 可能不连续 需要每个都对'a'计算偏移量做下标
            pi = ord(child_str[i])-ord('a')  # 当前指标的下标
            bcdef_data_text = getDataText(matchId, child_str[i]+fin_text, indexList, dataList, gapList, changeRateList, avgList)
            if bcdef_data_text == "$$":  # 某一项没有数值，直接跳过
                continue
            else:
                if fin_text.find("_changeRate") != -1:  # 百分率 计算比率
                    bcdef_data = float(bcdef_data_text.strip('%'))/100
                    a_data = float(a_data_text.strip('%'))/100
                    result_item = {'indexId': pi, 'indexName': indexList[pi], 'result': bcdef_data/a_data}  # 相对于'a'的偏移量
                    resultList.append(result_item)
                else:  # 普通数 计算比率
                    result_item = {'indexId': pi, 'indexName': indexList[pi], 'result': float(bcdef_data_text)/float(a_data_text)}
                    resultList.append(result_item)
        # 从大到小排序
        resultList = sorted(resultList, key=lambda item: item["result"], reverse=True)
        return resultList  # 各子类型占比计算结果
    # radioMax 先获取内部number表达式结果列表 再取最大值
    if exp_type == 8:  # 子类型占比中，占比最大的类型比例
        # number获取到实际表达式为：[7:bcdef/a_dataX] 或 [10:abc/numberX:y] y表示期数
        number_exp = getNumberWordExp(matchId, data_text)
        resultList = getNumberExpInfo(matchId, number_exp, indexList, dataList, gapList, changeRateList, avgList)
        # print(resultList[0])
        if not needIndexName:
            return resetFloat4(str(resultList[0]['result']))
        else:
            return resetFloat4(str(resultList[0]['result']))+"&&"+resultList[0]['indexName']
    # radioMin 先获取内部number表达式结果列表 再取最小值
    if exp_type == 9:  # 子类型占比中，占比最小的类型比例
        number_exp = getNumberWordExp(matchId, data_text)  # number获取到实际表达式为：[7:bcdef/a_dataX]
        resultList = getNumberExpInfo(matchId, number_exp, indexList, dataList, gapList, changeRateList, avgList)
        # print(resultList[len(resultList)-1])
        if not needIndexName:
            return resetFloat4(str(resultList[len(resultList)-1]['result']))
        else:
            return resetFloat4(str(resultList[len(resultList)-1]['result']))+"&&"+resultList[len(resultList)-1]['indexName']
    # bcd_dataY/numberX类  只考虑data
    if exp_type == 10:
        # 切割 bcd_dataY/numberX  bcd 代表指标
        data_text_divide = data_text.split("/")
        resultList = []  # 存放计算结果数值
        child_dataList = data_text_divide[0].split("_")  # 'bcd_dataY'串
        child_str = child_dataList[0]  # bcd
        fin_text = '_data'+data_type_id  # _dataY  data_type_id为第三部分标志位
        exp2 = data_text_divide[1]
        # 获取 number 数值字符串
        number_text = getNumberExpInfo(matchId, getNumberWordExp(matchId, exp2), indexList, dataList, gapList, changeRateList, avgList)
        if number_text == "$$":  # a无数值
            return None
        # 获取 bef_dataX 数值字符串 并计算/a结果 并处理百分率 存放resultList
        for i in range(0, len(child_str)):  # 'bdf' 可能不连续 需要每个都对'a'计算偏移量做下标
            pi = ord(child_str[i]) - ord('a')  # 当前指标的下标
            bcdef_data_text = getDataText(matchId, child_str[i]+fin_text, indexList, dataList, gapList, changeRateList, avgList)
            if bcdef_data_text == "$$":  # 某一项没有数值，直接跳过
                continue
            else:
                # 只考虑data
                result_item = {'indexId': pi, 'indexName': indexList[pi],
                               'result': float(bcdef_data_text) / float(number_text)}
                resultList.append(result_item)
        # 从大到小排序
        resultList = sorted(resultList, key=lambda item: item["result"], reverse=True)
        return resultList  # 各子类型占比计算结果
    return "[ number表达式错误 ]"


# number系列 计算式 将替换为[3 : a_gap6 : 2]，返回修改记录列表changeList
def remakeNumberX(matchId, analysisText, changeList, indexList, dataList, gapList, changeRateList, avgList):
    p_dataX = re.compile("\[number[0-9]+\]")  # 匹配左右中文
    for m in p_dataX.finditer(analysisText):
        m_str = m.group()[1:len(m.group())-1]
        # 获取number表达式实际
        expression = getNumberWordExp(matchId, m_str)
        dataText = getNumberExpInfo(matchId, expression, indexList, dataList, gapList, changeRateList, avgList)
        # 记录替换
        changeItem = {"id": m.start(), "length": len(m.group()), "text": dataText}
        changeList.append(changeItem)
        # print(m.start()+1, m.group()[1:len(m.group())-1], "->", dataText)
    return changeList



# ============================================ 处理留空词 word ====================================================


def getGapDesc(text_id, data):
    """
    :param text_id: 选择词组参数 1-7
    :param data: 数值影响词性
    :return: gapDesc描述词
    """
    text_list = [
        ['增长', '下降'],
        ['增长', '减少'],
        ['盈余', '赤字'],
        ['拉大', '缩小'],
        ['高于', '低于'],
        ['升高', '降低'],
        ['盈利', '亏损']
    ]
    ex = 0 if data > 0 else 1
    return text_list[text_id-1][ex]
def getRateDesc(text_id, data):
    """
    :param text_id: 选择词组参数 1-4
    :param data: 数值影响词性
    :return: rateDesc描述词
    """
    text_list = [
        ['增速', '减速'],
        ['加快', '减慢']
    ]
    ex = 0 if data > 0 else 1
    return text_list[text_id-1][ex]
def getRateChangeDesc(data1, data2):
    """
    :param data1: rateDesc 增-0、减-1 选择词组参数
    :param data2: 数值影响词性
    :return: 描述词
    """
    text_list = [
        ['上升', '回落'],
        ['回升', '下降']
    ]
    index1 = 0 if data1 > 0 else 1
    index2 = 0 if data2 > 0 else 1
    return text_list[index1][index2]
def getGapLevelDesc(x, expretion):
    """
    根据表达式的值，确定程度描述词。PS：与之前的统计分析划分的分级区间相结合？还是简单写死？
建议可以分开写，一个是大局上定死一个标准描述其表现；另一方面对比自身成长过程描述此段时间表现如何（即查看加速度与往期加速度均值的比率，仍需阈值）。
比如：
大局上定死：10%、30%、50%对应全体成长慢-快
A往期：8%、3%、7%、12%，本期22%
“虽然成长不如其他企业迅猛，但相较自身有了一个较大的进步。”
    :param x: 选择词组参数
    :param expretion: 数值影响词性
    :return: 描述词
    """
    text_list = [
        ['显著', '一般', '细微'],
        ['较强', '一般', '较弱'],
    ]
    ex = 0 if expretion > 0 else 1
    return text_list[x][ex]

# 获取文本匹配式信息
def cutGapDescASCExp(expretion):
    """
    处理[gapDesc:1:(c_data7)]类模板
    :param expretion: 模板
    :return: 模板类型、选词词组、原数据值
    """
    expretion = expretion.replace(' ', '').replace('　', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '')
    exp_list = expretion.split(":")
    # 模板类型
    type_text = exp_list[0]
    # 选取形容词组号/rateChangeDesc中为表达式1
    text_exp = exp_list[1]
    if len(exp_list) > 2:
        # 处理表达式
        data_exp_text = exp_list[2]
        return type_text, text_exp, data_exp_text
    else:  # indexMax类 仅两部分
        return type_text, text_exp, ""


# 区分是哪类文本匹配式信息
def getWordExpInfo(matchId, expression, indexList, dataList, gapList, changeRateList, avgList):
    expression = expression.replace(' ', '').replace('　', '').replace('(', '').\
        replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '')
    # 获取模板表达式信息 仅分割三部分
    #print(expression)
    type_text, text_exp, data_exp = cutGapDescASCExp(expression)

    # 获取第三部分表达式数值，包括套着的number计算式
    if data_exp != "":
        # 获取数值 字符串 可能有百分率
        x_data = getDataText(matchId, data_exp, indexList, dataList, gapList, changeRateList, avgList)
        if x_data == "$$":
            return "$$"
        else:
            x_data = getPrueData(x_data)  # 获取纯小数
            if type_text == "gapDesc":
                return getGapDesc(int(text_exp), float(x_data))
            elif type_text == "rateDesc":
                return getRateDesc(int(text_exp), float(x_data))
            elif type_text == "rateChangeDesc":
                # 获取第二部分 即 表达式1的数值 可能式纯数字，如1：即永大于0
                text_data = getDataText(matchId, text_exp, indexList, dataList, gapList, changeRateList, avgList)
                # print(text_data, float(x_data))
                return getRateChangeDesc(float(text_data), float(x_data))
            elif type_text == "gapLevelDesc":
                return getGapLevelDesc(int(text_exp), float(x_data))
    # 仅两部分  [indexMax/indexMin:(表达式)] 已切割 type_text、text_exp
    else:
        if text_exp.find("number") != -1 and text_exp.find(":") == -1:  # 套单独number表达式
            text_exp1 = getNumberWordExp(matchId, text_exp)
            text_exp = text_exp1
        # indexMax/indexMin 会由后面表达式的8/9标记进行区分，此处需要返回名称 会返回 数值字符串&&名称 字符串
        result = getNumberExpInfo(matchId, text_exp, indexList, dataList, gapList, changeRateList, avgList, needIndexName=True)
        indexName = result.split("&&")[1]
        return indexName  # 要返回这个最大/最小的名称


# word系列 文本匹配式 将替换为[gapDesc:1:a_gap6]，返回修改记录列表changeList
def remakeWordX(matchId, analysisText, changeList, indexList, dataList, gapList, changeRateList, avgList):
    p_dataX = re.compile("\[word[0-9]+\]")  # 匹配左右中文
    for m in p_dataX.finditer(analysisText):
        m_str = m.group()[1:len(m.group())-1]
        expression = getNumberWordExp(matchId, m_str)   #先找表达式中是否有numberx 比如该形式[gapDesc:1:number6]只能替换一个number
        dataText = getWordExpInfo(matchId, expression, indexList, dataList, gapList, changeRateList, avgList)
        # 记录替换
        changeItem = {"id": m.start(), "length": len(m.group()), "text": dataText}
        changeList.append(changeItem)
    #    print(m.start()+1, m.group()[1:len(m.group())-1], "->", dataText)
    return changeList



def remakeText(module):
    matchId = module["id"]
    subIndicatorList = module["subIndicatorList"]  # 二级模块ID
    analysisText = module["analysisText"]  # 数据描述文本
    area=module["area"]
    # moduleId = module["moduleId"]  # 二级模块ID
    # moduleName = module["moduleName"]  # 宏观分析角度名称
    # indicatorId = module["indicatorId"]  # 对应末端分支指标ID
    # indicatorLevel = module["indicatorLevel"]  # 指标所在层级（2-二级 3-三级）
    # description = module["description"]  # 描述
    # isValid = module["isValid"]  # 0-生效 1-失效

    changeList = []  # 记录所有修改，最后由大到小排序，有后向前按标记修改
    # indexCount = getIndexTime(subIndicatorList)  # 期数
    # 待改，目前日期可能不一致
    indexList, dataList, gapList, changeRateList, avgList, dateList, indexFreqList = getIndicatorData(matchId, subIndicatorList,area)
    # print('dataList:',dataList)
    # print('gapList:',gapList)
    # print('changeRateList:',changeRateList)
    # print('dateList:',dateList)
    # print("remakeText ", indexList)
    # 匹配 [timeX]、[timeX-timeY]
    #print(analysisText)
    changeList = remakeTimeXASC(analysisText, changeList, dateList, indexFreqList)
    changeList = remakeXDataX(matchId, analysisText, changeList, indexList, dataList, gapList, changeRateList, avgList)
    #print("匹配data结束: ", changeList)
    # 匹配word系列 即原留空词 [gapDesc:1:(c_data7)]
    changeList = remakeWordX(matchId, analysisText, changeList, indexList, dataList, gapList, changeRateList, avgList)
    #print("匹配word结束: ", changeList)
    # 匹配number系列 即原计算式 [3 : c_data7 : 2]
    changeList = remakeNumberX(matchId, analysisText, changeList, indexList, dataList, gapList, changeRateList, avgList)
    #print("匹配number结束: ", changeList)

    # 按修改标记从大到小排序
    changeList = sorted(changeList, key=lambda change: change["id"], reverse=True)
    for change in changeList:
      #  print(change)
        # if change["text"] == "$$":  # 存在数据错误
        #     # return "[ 句子("+str(matchId)+")替换错误 ]"
        #     return ""
        ana_len = len(analysisText)
        analysisText = analysisText[0:change["id"]]+change["text"]+analysisText[(change["id"]+change["length"]):ana_len]
    return analysisText  # 整句顺利替换


# 替换对应id文本
def remakeSentence(senId):
    sql = "select * from macro_child_report_module_indicator_date where id = "+str(senId)  # moduleId >= 33 limit 0, 1
    module = rs.SuccessSql(sql, isSelect=True)[0]   #返回查询得到的文本和其它内容 并保存为元组
    # resultText = remakeText(module)
    # print(resultText)
    try:
        resultText = remakeText(module)
        print(resultText)
    except Exception as e:
        traceback.print_exc()
        # return "[ 句子("+str(senId)+")替换错误 ]"
        return ""
    else:
        if ("$$" in resultText):
            update_sql = "update macro_child_report_module_indicator_date set note =" + "'数据缺失'" + " where id = " + str(
                module["id"])
        # resultText = module['']
        else:
            update_sql = "update macro_child_report_module_indicator_date set result = '"+resultText+"' where id = "+str(module["id"])
        print(update_sql)
        rs.SuccessSql(update_sql, isSelect=False)
        # resFile = "D:/辛弋然/A实验室/4.23/文本自动生成/test/textdateUpdateSqlreport.txt"
        # resultFile = open(resFile, 'a', encoding='utf-8', errors='ignore')
        # resultFile.write(update_sql + ';' + "\n")

# if __name__ == "__main__":
#     for i in range(1,116):
#         remakeSentence(i)   #替换相应id的文本 主函数入口



