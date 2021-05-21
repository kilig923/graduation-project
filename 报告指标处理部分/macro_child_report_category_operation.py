import runSql as rs


if __name__ == "__main__":
    sql = "SELECT DISTINCT moduleId,moduleName,area FROM macro_child_report_module_indicator where id>'94954'"
    try:
        result = rs.SuccessSql(sql, isSelect=True)  # 返回查询得到的文本和其它内容 并保存为元组
    except:
        print("wrong!")
    else:
        for res in result:
            moduleId=res['moduleId']
            moduleName=res['moduleName']
            area=res['area']

            if (area == '常住'):
                continue
            if (area == '户籍'):
                continue
            sql="select indexFreq from macro_economic_child_indicator where id="+str(moduleId)
            data = rs.SuccessSql(sql, isSelect=True)[0]
            indexFreq=data['indexFreq']


            sql="insert into macro_child_report_category (reportName,reportId,area,indexFreq) " \
                "values ('%s','%s','%s','%s') "%(moduleName,moduleId,area,indexFreq)

            resFile = "./macro_child_report_category_insertSql2.txt"
            resultFile = open(resFile, 'a', encoding='utf-8', errors='ignore')
            resultFile.write(sql + ';' + "\n")