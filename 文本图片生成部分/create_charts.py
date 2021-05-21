# encoding: utf-8
import sys
from pyecharts import options as opts
from pyecharts.charts import Bar,Line,Pie,Grid
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.components import Table



#   以下导入是为了生成图片
from pyecharts.render import make_snapshot
from snapshot_pyppeteer import snapshot
import imgkit

# ---------------------------------------全局变量------------------------------------------- #
THEME_TYPE = ThemeType.MACARONS


# ----------------------------------------Utils--------------------------------------------- #
def getMinRate(data_list):
    minData = sys.maxsize
    for x in data_list:
        for y in x:
            if y == None:
                continue
            elif y<minData:
                minData = y
    return minData

def getMaxRate(data_list):
    maxData = -sys.maxsize
    for x in data_list:
        for y in x:
            if y == None:
                continue
            elif y > maxData:
                maxData = y
    return maxData

def getMinData(data_dic):
    minData = sys.maxsize
    for key in data_dic.keys():
        for y in data_dic[key]:
            if y == None:
                continue
            elif y<minData:
                minData = y
    return minData

def getMaxData(data_dic):
    maxData = -sys.maxsize
    for key in data_dic.keys():
        for x in data_dic[key]:
            if x == None:
                continue
            elif x > maxData:
                maxData = x
    return maxData


# -----------------------------------待解决的几个问题------------------------------------- #
#   1.图表标题如何自动+正确的拟定：由时间+地点+指标内容拼接而成


# -------------------------------------------柱状图图表生成---------------------------------------------- #
#  基本柱状图主要分两种类型：1.时间序列型，横坐标为时间
#                            2.时间截面型，横坐标为不同指标/地区
#  进阶问题：1.比较每个bar的title长度与bar的范围长度，设置倾斜
#            2.增加markLine表示平均线、markPoint表示最大最小值
def create_base_bar(title, x_list, data_list, data_unit):
    """
    :param title: 图表名称
    :param x_list: 横坐标内容，具有多种情况：1.时间序列   2.指标序列
    :param data_list: 字典{key1:value1,key2:value2...}，构成柱状图的多个不同类型的bar
    :param data_unit: 数值的单位
    :return:
    """
    c = Bar(init_opts=opts.InitOpts(theme=THEME_TYPE))
    c.add_xaxis(x_list)
    for key in data_list.keys():
        c.add_yaxis(key, data_list[key])
    c.set_global_opts(title_opts=opts.TitleOpts(title=title),
                      legend_opts=opts.LegendOpts(pos_left="25%", pos_top="5%"),
                      yaxis_opts=opts.AxisOpts(name="单位:" + data_unit,
                                               is_scale=True))

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+":生成完毕...")

#   对基本柱状图的x-y轴置换后的柱状图
def create_reversal_bar(title, x_list, data_list, data_unit):
    """
    :param title: 图表名称
    :param x_list: 横坐标内容，具有多种情况：1.时间序列   2.指标序列
    :param data_list: 字典{key1:value1,key2:value2...}，构成柱状图的多个不同类型的bar
    :param data_unit: 数值的单位
    :return:
    """
    unit = "单位:" + data_unit
    c = Bar(init_opts=opts.InitOpts(theme=THEME_TYPE))
    c.add_xaxis(x_list)
    for key in data_list.keys():
        c.add_yaxis(key, data_list[key])
    c.reversal_axis()
    c.set_series_opts(label_opts=opts.LabelOpts(position="right"))
    c.set_global_opts(title_opts=opts.TitleOpts(title=title),
                      legend_opts=opts.LegendOpts(pos_left="right"),
                      xaxis_opts=opts.AxisOpts(name=unit))
    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+":生成完毕...")

#   比例构成柱状图
def create_percent_stack_bar(title, x_list, data_list, data_unit):
    """
        :param title: 图表名称
        :param x_list: 横坐标内容为时间序列，纵坐标高度为多个(同级)指标的总和，具体各个指标的数值、比例以不同颜色标出
        :param data_list: 字典{key1:value1,key2:value2...}，构成柱状图的多个不同类型的bar
        :param data_unit: y轴的数值单位
        :return:
        """
    # 数据格式重构：
    count = len(x_list)   # 数据期数
    sumList = []            # 汇总
    for i in range(count):
        sumList.append(0)
    for key in data_list.keys():
        for i in range(count):
            if data_list[key][i] is not None:           #   空数据处理
                sumList[i] = sumList[i] + data_list[key][i]
    for key in data_list.keys():
        value_list = []
        for i in range(count):
            new_dic = {}
            new_dic["value"] = data_list[key][i]
            if data_list[key][i] is not None:           #   空数据处理,sumList[i]不会为None或为0，指标选择时已经做了规避
                new_dic["percent"] = data_list[key][i]/sumList[i]
            else:
                new_dic["percent"] = None
            value_list.append(new_dic)
        data_list[key] = value_list

    c = Bar(init_opts=opts.InitOpts(theme=THEME_TYPE))
    c.add_xaxis(x_list)
    for key in data_list.keys():
        c.add_yaxis(key, data_list[key],stack="stack1")         # stack参数设置层叠样式

    c.set_series_opts(label_opts=opts.LabelOpts(position="right",
                      formatter=JsCode(
                        "function(x){console.log(x);return Number(x.data.percent * 100).toFixed() + '%';}"
                      )))
    c.set_global_opts(title_opts=opts.TitleOpts(title=title),
                      legend_opts=opts.LegendOpts(pos_left="right"),
                      yaxis_opts=opts.AxisOpts(name="单位:" + data_unit))

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+":生成完毕...")


#   柱状 + 折线图组合
#   选用说明：1.折线用于表示变化率:单柱状图+单折线 or 多柱状图+多折线
#             2.折线用于表示占比：
#             3.折线用于描述另一维度指标
#
def create_mixed_line_and_bar(type, title, x_list, data_list, data_unit1, data_unit2 = None):
    """
        :param type: 1-折线用于表示变化率and单柱状图+单折线  2-折线用于表示变化率and多柱状图+多折线
                    3-折线表示占比and单柱状图+单折线         4-折线表示占比and多柱状图+多折线
                    5-折线用于描述另一维度指标（此时data_list中最后一个k-v为折线数据）
        :param title: 图表名称
        :param x_list: 横坐标内容为时间序列，纵坐标高度为多个(同级)指标的总和，具体各个指标的数值、比例以不同颜色标出
        :param data_list: 字典{key1:value1,key2:value2...}，构成柱状图的多个不同类型的bar
        :param data_unit1: 第一根y轴的数值单位
        :param data_unit2: 第二根y轴的数值单位
        :return:
        """
    c = Bar(init_opts=opts.InitOpts(height="600px",width="900px",theme=ThemeType.MACARONS))
    c.add_xaxis(x_list)
    if type == 1:                               # 因为有overlap，所以需要自适应调整刻度范围，是的bar和line都能显示出来
        all_rate_list = []
        for key in data_list.keys():            # 单柱状图只有一个bar
            change_rate_list = [0]
            c.add_yaxis(key, data_list[key], bar_width="20%",label_opts=opts.LabelOpts(is_show=True))
            for i in range(1,len(data_list[key])):
                if data_list[key][i-1] == 0 or data_list[key][i-1] is None or data_list[key][i] is None:                     # 注意分母不为0
                    change_rate_list.append(None)
                else:
                    change_rate_list.append(round((data_list[key][i]-data_list[key][i-1])/data_list[key][i-1]*100,2))
            all_rate_list.append(change_rate_list)

        c.extend_axis(yaxis=opts.AxisOpts(
            name="变化率",
            type_="value",
            min_=int(round((getMinRate(all_rate_list)-(getMaxRate(all_rate_list)-getMinRate(all_rate_list)))/10)*10),
            max_=int(round((getMaxRate(all_rate_list)/10)*10)),
            interval=10,
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
        ))
        line = (
            Line()
                .add_xaxis(xaxis_data=x_list)
                .add_yaxis(
                series_name="增长率",
                yaxis_index=1,
                y_axis=all_rate_list[0],
                label_opts=opts.LabelOpts(is_show=True, formatter=JsCode(
                        "function(x){console.log(x);return Number(x.data[1]).toFixed(2) + '%';}"
                      )),
            )
        )
        c.set_global_opts(title_opts=opts.TitleOpts(title=title,# subtitle="数据来源国家统计局",
                                                    # pos_left="center",pos_bottom="0px",
                                                    # item_gap=2,
                                                    # subtitle_textstyle_opts=opts.TextStyleOpts(color="black")
                                                    ),
                          legend_opts=opts.LegendOpts(pos_left="right"),
                          yaxis_opts=opts.AxisOpts(name="单位:" + data_unit1,
                                               # name_location="end",
                                               # name_gap=5,
                                               # # name_rotate=45,
                                               min_=0,                          # 基本上指标数据都是为正的
                                               max_=int(round(getMaxData(data_list)/10)*10)*2,
                                               interval=10,
                                             ))
        c.overlap(line)
    elif type == 2:
        count = len(data_list.keys())
        all_rate_list = []
        keys_list = []
        for key in data_list.keys():
            keys_list.append(key)
            change_rate_list = [0]
            c.add_yaxis(key, data_list[key], label_opts=opts.LabelOpts(is_show=True))
            for i in range(1,len(data_list[key])):
                if data_list[key][i-1] == 0 or data_list[key][i-1] is None or data_list[key][i] is None:                     # 注意分母不为0
                    change_rate_list.append(None)
                else:
                    change_rate_list.append(round((data_list[key][i]-data_list[key][i-1])/data_list[key][i-1]*100,2))
            all_rate_list.append(change_rate_list)
        c.extend_axis(yaxis=opts.AxisOpts(
            name="变化率",
            type_="value",
            min_=int(
                round((getMinRate(all_rate_list) - (getMaxRate(all_rate_list) - getMinRate(all_rate_list))) / 10) * 10),
            max_=int(round((getMaxRate(all_rate_list) / 10) * 10)),
            interval=10,
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
        ))
        all_line = []
        for i in range(count):
            line = (
                Line()
                    .add_xaxis(xaxis_data=x_list)
                    .add_yaxis(
                    series_name=keys_list[i] + "增长率",
                    yaxis_index=1,
                    y_axis=all_rate_list[i],
                    label_opts=opts.LabelOpts(is_show=True, formatter=JsCode(
                        "function(x){console.log(x);return Number(x.data[1]).toFixed(2) + '%';}"
                    )),
                )
            )
            all_line.append(line)
        c.set_global_opts(title_opts=opts.TitleOpts(title=title,  # subtitle="数据来源国家统计局",
                                                    pos_left="center",pos_bottom="0px",
                                                    # item_gap=2,
                                                    # subtitle_textstyle_opts=opts.TextStyleOpts(color="black")
                                                    ),
                          legend_opts=opts.LegendOpts(pos_left="right"),
                          yaxis_opts=opts.AxisOpts(name="单位:" + data_unit1,
                                                   # name_location="end",
                                                   # name_gap=5,
                                                   # # name_rotate=45,
                                                   min_=0,
                                                   max_=int(round(getMaxData(data_list)/10)*10)*2,
                                                   interval=10,
                                                   ))
        for line in all_line:
            c.overlap(line)

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+":生成完毕...")


# ----------------------------------------------折线图----------------------------------------------  #

#   基础折线图
def create_base_line(title, x_list, data_list, data_unit):
    """
        :param title: 图表名称
        :param x_list: 横坐标内容一般为时间序列
        :param data_list: 字典{key1:value1,key2:value2...}，构成多条不同的折线
        :param data_unit: y轴的数值单位
        :return:
        """
    c = (
        Line(init_opts=opts.InitOpts(theme=THEME_TYPE))
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            legend_opts=opts.LegendOpts(pos_left="right"),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="单位"+data_unit,
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True# 刻度标记线
            ),
        )
            .add_xaxis(xaxis_data=x_list)
    )
    for key in data_list.keys():
        c.add_yaxis(
            series_name=str(key),
            y_axis=data_list[key],
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+"生成完毕...")


#   基础折线图-含均值标记线和最值标记点
def create_base_line_with_marks(title, x_list, data_list, data_unit):
    """
        :param title: 图表名称
        :param x_list: 横坐标内容一般为时间序列
        :param data_list: 字典{key1:value1,key2:value2...}，构成多条不同的折线
        :param data_unit: y轴的数值单位
        :return:
        """
    c = (
        Line(init_opts=opts.InitOpts(theme=THEME_TYPE))
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            legend_opts=opts.LegendOpts(pos_left="right"),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="单位"+data_unit,
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True
                # 刻度标记线
            ),
        )
            .add_xaxis(xaxis_data=x_list)
    )
    for key in data_list.keys():
        c.add_yaxis(
            series_name=str(key),
            y_axis=data_list[key],
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
        )

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+"生成完毕...")


# ----------------------------------------------饼状图----------------------------------------------  #
# 使用饼状图的两个问题：
#                       1.是否存在summary指标，1)如果有，summary指标传入的格式约定  2)如果无，则加总数据作为总数
#                       2.

#   基础饼状图: 一般用于表示时间截面数据
def create_base_pie(title, data_list):
    """
        :param title: 图表名称
        :param dic: 字典{key1:[value1,value2...],key2:[value1,value2...]...}，构成多条不同的折线
        :return:    生成最新一期、各指标数据占比情况饼状图
        """
    #   1.数据格式转换
    key_list = []
    value_list = []
    for key in data_list.keys():
        key_list.append(key)
        value_list.append(data_list[key][len(data_list[key]) - 1])
    data_pair = [list(z) for z in zip(key_list, value_list)]
    #   2.计算各项指标的占比
    sum = 0
    for x in data_pair:
        if x[1] is not None:
            sum += x[1]
    for x in data_pair:
        if x[1] is not None:                        # sum不为0，这在指标选取时规避
            x[1] = round(x[1]/sum*100,2)
    #   3.开始生成饼状图
    c = (
        Pie(init_opts=opts.InitOpts(theme=THEME_TYPE,width="700px"))
            .add(series_name="占比情况", data_pair=data_pair,center=["40%", "50%"],radius=["0","60%"])
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             legend_opts=opts.LegendOpts(pos_left="80%",orient="vertical"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%" ))
    )

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+"生成完毕...")

#   多饼状图：将时间序列数据 转换为 多个时间截面的对应的饼状图
def create_base_multiple_pie(title, data_list):
    """
        :param title: 图表名称
        :param dic: 字典{key1:[value1,value2...],key2:[value1,value2...]...}，构成多条不同的折线
        :return:    生成最近四期、各指标数据占比情况饼状图
        """
    #   1.数据格式转换
    data_pair_list = []
    for i in range(0,4):
        value_list = []
        key_list = []
        for key in data_list.keys():
            key_list.append(key)
            value_list.append(data_list[key][len(data_list[key])-4+i])        #   避免数组越界，即期数需要大于4
        data_pair_list.append([list(z) for z in zip(key_list, value_list)])

    #   2.计算每个时间截面的占比情况
    for data_pair in data_pair_list:
        sum = 0
        for x in data_pair:
            if x[1] is not None:
                sum += x[1]
        for x in data_pair:
            if x[1] is not None:                    # sum不会为0，指标选取后
                x[1] = round(x[1]/sum*100, 2)

    c = (
        Pie(init_opts=opts.InitOpts(theme=THEME_TYPE,width="800px"))
            .add(series_name="第一季度占比情况", data_pair=data_pair_list[0],center=["20%", "30%"],radius=["0","30%"])
            .add(series_name="第二季度占比情况", data_pair=data_pair_list[1],center=["60%", "30%"],radius=["0","30%"])
            .add(series_name="第三季度占比情况", data_pair=data_pair_list[2],center=["20%", "70%"],radius=["0","30%"])
            .add(series_name="第四季度占比情况", data_pair=data_pair_list[3],center=["60%", "70%"],radius=["0","30%"])
            .set_global_opts(title_opts=opts.TitleOpts(title=title),legend_opts=opts.LegendOpts(pos_left="80%",orient="vertical"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%" ))
    )

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+"生成完毕...")

#   ----------------------------------------------------表格---------------------------------------------------    #
#   PS：以表格的形式展示数据


def create_base_table(title, x_list, data_list):
    headers = [" "] + x_list
    rows = []
    for key in data_list.keys():
        #print(key)
        row = []
        row.append(key)
        for x in data_list[key]:
            row.append(x)
        #print(row)
        rows.append(row)
    table = Table()
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=opts.ComponentTitleOpts(title=title)
    )
    src_path = "./test/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    table.render(html_file_name)
    path_wkimg = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'  # 工具路径
    cfg = imgkit.config(wkhtmltoimage=path_wkimg)
    imgkit.from_file(html_file_name, img_file_name, config=cfg)
    #make_snapshot(snapshot, table.render(html_file_name), img_file_name)
    print(img_file_name+"生成完毕...")

#   ------------------------------------------------------组合图表-------------------------------------------------    #
#   PS：饼状图默认不包含summary指标，而是由多指标的和作为summary
#   柱状图+饼状图：柱状图描绘时间序列数据、饼状图描绘最新1期or2期数据的占比情况
def create_grid_bar_and_pie(title, x_list, data_list, data_unit):
    #   1.先生成左边的柱状图
    bar = Bar()
    bar.add_xaxis(x_list)
    for key in data_list.keys():
        bar.add_yaxis(key, data_list[key])
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title),
                      legend_opts=opts.LegendOpts(pos_left="right"),
                      yaxis_opts=opts.AxisOpts(name="单位:" + data_unit))

    #   2.再生成右边的饼状图(使用最新一期数据)
    #   2.1 数据格式转换
    key_list = []
    value_list = []
    for key in data_list.keys():
        key_list.append(key)
        value_list.append(data_list[key][len(data_list[key]) - 1])
    data_pair = [list(z) for z in zip(key_list, value_list)]

    #   2.2 计算各项指标的占比
    sum = 0
    for x in data_pair:
        if x[1] is not None:
            sum += x[1]
    for x in data_pair:
        if x[1] is not None:
            x[1] = round(x[1] / sum * 100, 2)

    #   2.3 开始生成饼状图

    pie = Pie()
    pie.add(series_name="占比情况", data_pair=data_pair, radius=["0", "30%"],center=["40%", "75%"])
    pie.set_global_opts(title_opts=opts.TitleOpts(title=title+"-最新占比情况",pos_top="48%"),
                         legend_opts=opts.LegendOpts(pos_left="70%",pos_top="50%",orient="vertical"))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))

    # 3.生成最终的组合图
    c = (
        Grid(init_opts=opts.InitOpts(theme=THEME_TYPE,height="700px"))
            .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
            .add(pie, grid_opts=opts.GridOpts(pos_top="60%"))
    )

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+"生成完毕...")

#   折线图+饼状图 type1：折线图描绘各个指标的实际数据值，饼状图描绘最新2期数据的占比情况
#   折线图+饼状图 type2：折线图描绘各个指标所占比重随时间序列的变化情况、饼状图描绘最新数据的占比情况
def create_grid_pie_and_line(type,title, x_list, data_list, data_unit):
    if type == 1:                  #   类型1
        #   1.先生成折线图（含标记点和标记线）
        line = (
            Line(init_opts=opts.InitOpts(theme=THEME_TYPE))
                .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                legend_opts=opts.LegendOpts(pos_left="right"),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    name="单位：" + data_unit,
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    is_scale=True# 刻度标记线
                ),
            )
                .add_xaxis(xaxis_data=x_list)
        )
        for key in data_list.keys():
            line.add_yaxis(
                series_name=str(key),
                y_axis=data_list[key],
                symbol="emptyCircle",
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
                # markpoint_opts=opts.MarkPointOpts(
                #     data=[
                #         opts.MarkPointItem(type_="max", name="最大值"),
                #         opts.MarkPointItem(type_="min", name="最小值"),
                #     ]
                # ),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average", name="平均值")]
                ),
            )
        #   2.再生成饼状图（最新两期的饼状图）
        #   2.1 数据格式转换
        data_pair_list = []
        for i in range(0, 2):
            value_list = []
            key_list = []
            for key in data_list.keys():
                key_list.append(key)
                value_list.append(data_list[key][len(data_list[key]) - 2 + i])  # 避免数组越界，即期数需要大于2
            data_pair_list.append([list(z) for z in zip(key_list, value_list)])

        #   2.2 计算每个时间截面的占比情况
        for data_pair in data_pair_list:
            sum = 0
            for x in data_pair:
                if x[1] is not None:           #   数值缺空时的处理方式
                    sum += x[1]
            for x in data_pair:
                if  x[1] is not None:
                    x[1] = round(x[1] / sum * 100, 2)

        #   2.3 开始定义饼状图
        pie = (
            Pie(init_opts=opts.InitOpts(theme=THEME_TYPE))
                .add(series_name="第三季度占比情况", data_pair=data_pair_list[0], radius=["0", "30%"],center=["20%", "75%"])
                .add(series_name="第四季度占比情况", data_pair=data_pair_list[1], radius=["0", "30%"],center=["70%", "75%"])
                .set_global_opts(title_opts=opts.TitleOpts(title=title+"占比情况",pos_top="48%"),
                                 legend_opts=opts.LegendOpts(pos_left="90%",pos_top="48%", orient="vertical"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
        )

        # 3.生成最终的组合图
        c = (
            Grid(init_opts=opts.InitOpts(theme=THEME_TYPE,height="700px"))
                .add(line, grid_opts=opts.GridOpts(pos_bottom="60%"))
                .add(pie, grid_opts=opts.GridOpts(pos_top="60%"))
        )

        src_path = "./指标-年度-图片生成/"
        html_file_name = src_path + title + ".html"
        img_file_name = src_path + title + ".png"
        make_snapshot(snapshot, c.render(html_file_name), img_file_name)
        print(img_file_name+"生成完毕...")
    elif type == 2:
        #   1.先生成占比折线图（需要先进行数据加工）
        #   1.1 数据计算
        count = len(x_list)
        sum_value = []
        for i in range(count):          # 初始化为0
            sum_value.append(0)
        radio_list = []
        key_list = []
        for key in data_list.keys():
            key_list.append(key)
            for i in range(count):
                if data_list[key][i] is not None:
                    sum_value[i] = sum_value[i] + data_list[key][i]
        for key in key_list:
            radio = []
            for i in range(count):
                if data_list[key][i] is not None:               # sum_value[i]不会为None，也不好为0（指标选择时选的都是有数据的期数）
                    radio.append(data_list[key][i]/sum_value[i]*100)
                else:
                    radio.append(None)
            radio_list.append(radio)

        #   1.2 生成折线图
        line = (
            Line(init_opts=opts.InitOpts(theme=THEME_TYPE))
                .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                legend_opts=opts.LegendOpts(pos_left="right"),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    name="单位：" + "占比(%)",
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),  # 刻度标记线
                ),
            )
                .add_xaxis(xaxis_data=x_list)
        )
        for i in range(count):
            line.add_yaxis(
                series_name=str(key_list[i]),
                y_axis=radio_list[i],
                symbol="emptyCircle",
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
                # markpoint_opts=opts.MarkPointOpts(
                #     data=[
                #         opts.MarkPointItem(type_="max", name="最大值"),
                #         opts.MarkPointItem(type_="min", name="最小值"),
                #     ]
                # ),
                # markline_opts=opts.MarkLineOpts(
                #     data=[opts.MarkLineItem(type_="average", name="平均值")]
                # ),
            )
            #   2.再生成饼状图（最新两期的饼状图）
            #   2.1 数据格式转换
            data_pair_list = []
            for i in range(0, 2):
                value_list = []
                key_list = []
                for key in data_list.keys():
                    key_list.append(key)
                    value_list.append(data_list[key][len(data_list[key]) - 2 + i])  # 避免数组越界，即期数需要大于2
                data_pair_list.append([list(z) for z in zip(key_list, value_list)])

            #   2.2 计算每个时间截面的占比情况
            for data_pair in data_pair_list:
                sum = 0
                for x in data_pair:
                    if x[1] is not None:  # 数值缺空时的处理方式
                        sum += x[1]
                for x in data_pair:
                    if x[1] is not None:
                        x[1] = round(x[1] / sum * 100, 2)

            #   2.3 开始定义饼状图
            pie = (
                Pie(init_opts=opts.InitOpts(theme=THEME_TYPE))
                    .add(series_name="第三季度占比情况", data_pair=data_pair_list[0], radius=["0", "30%"],
                         center=["20%", "75%"])
                    .add(series_name="第四季度占比情况", data_pair=data_pair_list[1], radius=["0", "30%"],
                         center=["70%", "75%"])
                    .set_global_opts(title_opts=opts.TitleOpts(title=title + "占比情况", pos_top="48%"),
                                     legend_opts=opts.LegendOpts(pos_left="90%", pos_top="48%", orient="vertical"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
            )

            # 3.生成最终的组合图
            c = (
                Grid(init_opts=opts.InitOpts(theme=THEME_TYPE,height="700px"))
                    .add(line, grid_opts=opts.GridOpts(pos_bottom="60%"))
                    .add(pie, grid_opts=opts.GridOpts(pos_top="60%"))
            )

            src_path = "./指标-年度-图片生成/"
            html_file_name = src_path + title + ".html"
            img_file_name = src_path + title + ".png"
            make_snapshot(snapshot, c.render(html_file_name), img_file_name)
            print(img_file_name+"生成完毕...")

#   柱状图+折线图：柱状图是数据原值的表示、折线图作为相应变化率的表示
def create_grid_bar_and_line(title, x_list, data_list, data_unit):
    #   1.先生成上方的柱状图
    bar = Bar()
    bar.add_xaxis(x_list)
    for key in data_list.keys():
        bar.add_yaxis(key, data_list[key])
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title),
                        legend_opts=opts.LegendOpts(pos_left="right"),
                        yaxis_opts=opts.AxisOpts(name="单位:" + data_unit,
                                                 is_scale=True))

    #   2.再生成下方的折线图
    #   2.1 数据计算
    count = len(x_list)
    all_rate_list = []
    key_list = []
    for key in data_list.keys():
        key_list.append(key)
        change_rate_list = [0]
        for i in range(1, len(data_list[key])):
            if data_list[key][i - 1] == 0 or data_list[key][i - 1] is None or data_list[key][i] is None:  # 注意分母不为0
                change_rate_list.append(None)
            else:
                change_rate_list.append(
                    round((data_list[key][i] - data_list[key][i - 1]) / data_list[key][i - 1] * 100, 2))
        all_rate_list.append(change_rate_list)
    #   2.2 生成折线图
    line = (
        Line(init_opts=opts.InitOpts(theme=THEME_TYPE))
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title+"-变化率情况",pos_top="48%"),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            legend_opts=opts.LegendOpts(pos_left="right",pos_top="48%"),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="单位：" + "变化率(%)",
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True# 刻度标记线
            ),
        )
            .add_xaxis(xaxis_data=x_list)
    )
    for i in range(count):
        line.add_yaxis(
            series_name=str(key_list[i]),
            y_axis=all_rate_list[i],
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            # markpoint_opts=opts.MarkPointOpts(
            #     data=[
            #         opts.MarkPointItem(type_="max", name="最大值"),
            #         opts.MarkPointItem(type_="min", name="最小值"),
            #     ]
            # ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
        )
        # 3.生成最终的组合图
        c = (
            Grid(init_opts=opts.InitOpts(theme=THEME_TYPE,height="700px"))
                .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
                .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
        )

        src_path = "./指标-年度-图片生成/"
        html_file_name = src_path + title + ".html"
        img_file_name = src_path + title + ".png"
        make_snapshot(snapshot, c.render(html_file_name), img_file_name)
        print(img_file_name+"生成完毕...")


def create_grid_bar_and_bar(title, x_list, data_list, data_list_2, data_unit_list):
    #   1.先生成上方的柱状图
    bar1 = Bar()
    bar1.add_xaxis(x_list)
    for key in data_list.keys():
        bar1.add_yaxis(key, data_list[key])
    bar1.set_global_opts(title_opts=opts.TitleOpts(title=title),
                        legend_opts=opts.LegendOpts(pos_left="25%", pos_top="5%"),
                        yaxis_opts=opts.AxisOpts(name="单位:" + data_unit_list[0]
                                                 , is_scale=True))

    #   2.下方柱状图
    bar2 = Bar()
    bar2.add_xaxis(x_list)
    for key in data_list_2.keys():
        bar2.add_yaxis(key, data_list_2[key])
    bar2.set_global_opts(title_opts=opts.TitleOpts(title=title),
                        legend_opts=opts.LegendOpts(pos_left="25%", pos_top="55%"),
                        yaxis_opts=opts.AxisOpts(name="单位:" + data_unit_list[1],
                                                 is_scale=True))

    # 3.生成最终的组合图
    c = (
            Grid(init_opts=opts.InitOpts(theme=THEME_TYPE,height="700px"))
                .add(bar1, grid_opts=opts.GridOpts(pos_bottom="60%"))
                .add(bar2, grid_opts=opts.GridOpts(pos_top="60%"))
        )

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+"生成完毕...")
def create_grid_bar_line(title, x_list, data_list, data_list_2, data_unit_list):
    #   1.先生成上方的柱状图
    bar1 = Bar()

    bar1.add_xaxis(x_list)
    for key in data_list.keys():
        bar1.add_yaxis(key, data_list[key])
    bar1.set_global_opts(title_opts=opts.TitleOpts(title=title),
                        legend_opts=opts.LegendOpts(pos_left="right"),
                        yaxis_opts=opts.AxisOpts(name="单位:" + data_unit_list[0],
                                                 is_scale=True))

    #   2.下方线型图
    line = (
        Line(init_opts=opts.InitOpts(theme=THEME_TYPE))
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            legend_opts=opts.LegendOpts(pos_left="25%", pos_top="55%"),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                name="单位：" + data_unit_list[1],
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True
                # 刻度标记线
            ),
        )
            .add_xaxis(xaxis_data=x_list)
    )
    for key in data_list_2.keys():
        line.add_yaxis(
            series_name=str(key),
            y_axis=data_list_2[key],
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            # markpoint_opts=opts.MarkPointOpts(
            #     data=[
            #         opts.MarkPointItem(type_="max", name="最大值"),
            #         opts.MarkPointItem(type_="min", name="最小值"),
            #     ]
            # ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
        )

    # 3.生成最终的组合图
    c = (
            Grid(init_opts=opts.InitOpts(theme=THEME_TYPE,height="700px"))
                .add(bar1, grid_opts=opts.GridOpts(pos_bottom="60%"))
                .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
        )

    src_path = "./指标-年度-图片生成/"
    html_file_name = src_path + title + ".html"
    img_file_name = src_path + title + ".png"
    make_snapshot(snapshot, c.render(html_file_name), img_file_name)
    print(img_file_name+"生成完毕...")


if __name__ == "__main__":
    # ---------------------------常用柱状图测试-------------------------------- #
    # title = "2020年各行业季度产值情况-柱状图"
    # dic = {"旅游业": [59, 48, 67, 43], "餐饮业": [75, None, 97, 83],
    #        "交通运输": [53, 66, 72, 39], "建筑业": [96, 105, 89, 76]}
    # xList = ["第一季度", "第二季度", "第三季度", "第四季度"]
    # create_base_bar(title+"1", xList, dic, "亿元")
    # create_reversal_bar(title + "2", xList, dic, "亿元")
    # create_percent_stack_bar(title + "3", xList, dic, "亿元")
    # dic = {"旅游业": [59, 48, 67, 43]}
    # create_mixed_line_and_bar(1,"2020旅游业业季度产值情况图1",["第一季度", "第二季度", "第三季度", "第四季度"],dic,"亿元")
    # create_mixed_line_and_bar(2,"2020各产业季度产值情况图2",["第一季度", "第二季度", "第三季度", "第四季度"],dic,"亿元")

    # ---------------------------常用折线图测试-------------------------------- #
    # dic = {"旅游业": [59, 48, 67, 43], "餐饮业": [75, 65, None, 83],
    #        "交通运输": [53, 66, 72, 39], "建筑业": [96, 105, 89, 76]}
    # xList = ["第一季度", "第二季度", "第三季度", "第四季度"]
    # create_base_line("2020年各行业季度产值情况折线图",xList,dic,"亿元")
    # create_base_line_with_marks("2020年各行业季度产值情况折线图-含标记线和点",xList,dic,"亿元")

    # ---------------------------常用饼状图测试-------------------------------- #
    # dic = {"旅游业": [59], "餐饮业": [75], "交通运输": [0], "建筑业": [96],"其它":[34]}
    # key_list = []
    # data_list = []
    # for key in dic.keys():
    #     key_list.append(key)
    #     data_list.append(dic[key][len(dic[key])-1])
    # data_pair = [list(z) for z in zip(key_list, data_list)]
    # #data_pair.sort(key=lambda x: x[1])
    # print(data_pair)
    # print(33.92+20.85+26.5+18.73)
    # create_base_pie("2020第一季度各行业占比情况",dic)
    # dic = {"旅游业": [34,45,56,59],
    # }
    # create_base_multiple_pie("2020各季度各行业占比情况图",dic)

    # ---------------------------常用组合图测试-------------------------------- #
    # dic = {"旅游业": [59, 48, 67, 43], "餐饮业": [75, 65, None, 83],
    #        "交通运输": [53, 66, 72, 39], "建筑业": [96, 105, 89, 76]}
    # xList = ["第一季度", "第二季度", "第三季度", "第四季度"]
    # create_grid_bar_and_pie("2020年各季度各行业情况图",xList,dic,"亿元")
    # create_grid_pie_and_line(1,"2020年各季度各行业情况图2",xList,dic,"亿元")
    # create_grid_pie_and_line(2,"2020年各季度各行业情况图3",xList,dic,"亿元")
    # create_grid_bar_and_line("2020年各季度各行业情况图4",xList,dic,"亿元")

    # -----------------------------表格展示数据--------------------------------- #
    dic = {"旅游业": [59, 48, 67, 43], "餐饮业": [75, 65, None, 83],
           "交通运输": [53, 66, 72, 39], "建筑业": [96, 105, 89, 76]}
    xList = ["第一季度", "第二季度", "第三季度", "第四季度"]
    create_base_table("2020年各季度各行业情况表",xList,dic)



    # ----------------------------考虑几个问题-------------------------------------- #
    # 1.饼状图时的summary指标是否存在的两种情况
    # 2.图的命名、组合图中子图的命名
    # 3.table只能生成.html文件 不能生成.png图片
    # 4.代码的优化、解耦：基本图的生成返回charts、全局变量、自适应大小
