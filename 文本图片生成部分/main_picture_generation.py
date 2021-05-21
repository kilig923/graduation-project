# noinspection PyUnresolvedReferences
import pymysql
import create_charts
import imagetosql

# noinspection PyUnresolvedReferences
from tkinter import _flatten
import runSql as rs

def graph_choose(dataUnit,x_list,data_dic,title):

    # 基本柱状图
    base_bar_chart = ("个",  "元", "千公顷")
    # x-y轴置换 柱状图
    reversal_bar_chart = ("人", "户", "人/户", "万辆","%","万人", "亿元")
    # 基本折线图
    base_line_chart = ("公斤/人", "公斤/公顷", "万吨", "万头", "元/公斤",
                       "比重", "同比环比变化率", "同比环比(上期=100)",)
    # 基本折线图+标记
    line_with_mark_chart = ("同比环比(上期=100)", "比重", "人", "户", "人/户",
                            "万辆", "项", "所",'None')
    # 基本饼状图
    base_pie_chart = ("公里", "艘", "吨", "万美元", "亿美元")
    # 基本表格
    base_table_chart = ()

    for key in data_dic.keys():
        if (len(data_dic[key]) < 4):
            create_charts.create_base_table(title, x_list, data_dic)
        else:
            if dataUnit in reversal_bar_chart:
                create_charts.create_reversal_bar(title, x_list, data_dic, dataUnit)
            elif dataUnit in base_bar_chart:
                create_charts.create_base_bar(title, x_list, data_dic, dataUnit)
            elif dataUnit in base_line_chart:
                create_charts.create_base_line(title, x_list, data_dic, dataUnit)
            elif dataUnit in line_with_mark_chart:
                create_charts.create_base_line_with_marks(title, x_list, data_dic, dataUnit)
            elif dataUnit in base_pie_chart:
                create_charts.create_base_pie(title, data_dic)
            else:
                create_charts.create_base_table(title, x_list, data_dic)


if __name__ == '__main__':
    #293585
    #7291√
    for i in range(1,116):
        data_list=[]
        x_list=[]
        data_dic={}
        sql = "SELECT * FROM macro_child_report_module_indicator_date WHERE id =%s" % (i)
        try:
            result = rs.SuccessSql(sql, isSelect=True)[0]  # 返回查询得到的文本和其它内容 并保存为元组
        except:
            print("notfound: module indicatorId" + str(i))
            continue
        if(result['result']==""):
            continue
        # if(result['area']!='230281'):
        #     continue

        subIndicatorList=result['subIndicatorList']
        enddate=result['date']
        datarange=result['datarange']
        area=result['area']


        subIndicatorList=subIndicatorList.strip('[]')
        ind_id = subIndicatorList.split(":")[0]
        ind_Duration = subIndicatorList.split(":")[1]
        firsttime = ind_Duration[:10].replace('.', '-')
        lasttime = ind_Duration[11:].replace('.', '-')

        sql = "select indexName,dataUnit from macro_economic_child_indicator where id = " + ind_id
        try:
            data = rs.SuccessSql(sql, isSelect=True)[0]
        except:
            print("ERROR when finding indexName!")

        indexName = data['indexName']
        dataUnit=data['dataUnit']
        print(indexName)

        if (area == None):
            if (firsttime == lasttime):
                sql = "SELECT * FROM macro_economic_child_data_raw WHERE indicatorId = '%s' and " \
                      "dataDate='%s'" % (ind_id, firsttime)
            else:
                sql = "SELECT * FROM macro_economic_child_data_raw WHERE indicatorId = '%s' and " \
                      "dataDate>='%s' and dataDate<='%s' order by dataDate desc" % \
                      (ind_id, firsttime, lasttime)
        else:
            if (firsttime == lasttime):
                sql = "SELECT * FROM macro_economic_child_data_raw WHERE indicatorId = '%s' and" \
                      " dataDate='%s' and area='%s'" % (ind_id, firsttime, area)
            else:
                sql = "SELECT * FROM macro_economic_child_data_raw WHERE indicatorId = '%s' and " \
                      "dataDate>='%s' and dataDate<='%s' and area='%s' order by dataDate desc" % \
                      (ind_id, firsttime, lasttime, area)

        try:
            indicatorData = rs.SuccessSql(sql, isSelect=True)
        except:
            print("ERROR when finding datas!")

#        print(indicatorData)
        j=0
        for ind_data in indicatorData:
            j=j+1
            if (j > 5):
                break
            x_list.append(ind_data['dataDate'])   #横坐标
            data_list.append(ind_data['data'])   #指标数据

        x_list.reverse()
        data_list.reverse()
        data_dic.update({indexName: data_list})
        title=indexName+'('+str(enddate)+')'
        if('/' in title):
            title=title.replace('/','每')
        print(x_list,data_dic,dataUnit,title)

        graph_choose(dataUnit,x_list,data_dic,title)
        imagetosql.image_to_sql(i, title)   #i为对应的文本的id




