import traceback  #有关捕捉函数异常的库
import re         #有关正则表达式的库

import runSql as rs



class ModuleType:
    total_n=0
    total_w=0   #这两个参数用来统计word和number的数量
    number=[]  # 创建列表来记录number的值
    word=[]
    # 类的构造函数或初始化方法，当创建了这个类的实例时就会调用该方法
    # self 代表类的实例，self 在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数。
    def __init__(self,word,number,result,datarange,area):
        self.word=word
        self.number=number
        self.result=result
        self.datarange=datarange
        self.area=area
        #print("创建新的模板")

#一句话模板
    def module1(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']
        print(datarange)
        text = '据最新统计数据显示，截至[time'+str(datarange)+']，' \
               + str(indexName) + '的数据达到了[a_data'+str(datarange)+']' + str(result['dataUnit']) + '。'

        return text,word,number

#大模板1
    def module2(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 ="[4: a_data%s-a_data%s: 1]" % (datarange, datarange - 2)
        number2 = "[6:number1/a_data%s:2]" % (datarange - 2)
        word1 = "[gapDesc:1:number1]"
        word2 = "[gapLevelDesc:1:number2]"

        number_add=[number1,number2]
        word_add=[word1,word2]
        number=number+number_add
        word=word+word_add


        text=str(indexName)+'是'+str(result['moduleName'])+'所需要考察的一个重要指标，' \
            '通常对此产生不可忽略的作用。' \
            '由最新更新的数据显示，最近三年'+str(indexName)+'的数据呈现[word1]趋势。' \
            '由具体数据来看，[time'+str(datarange)+']该指标的数据为[a_data'+str(datarange)+\
             ']'+result['dataUnit']+'，[time'+str(datarange-1)+']该指标的数据为' \
            '[a_data'+str(datarange-1)+']'+result['dataUnit']+'，[time'+str(datarange-2)+\
             ']该指标的数据为[a_data'+str(datarange-2)+']'+result['dataUnit']+'。这三年的变化率为[number2]，' \
            '相对来说变化速率较为[word2]。同时，我们可以从这三年的统计数据得出，该指标的平均值为[a_avg]'+result['dataUnit']+'。'
        return text,word,number

#模板三的衍生模板1
    def module3(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 ="[4: a_data%s-a_data%s: 1]" % (datarange, datarange - 2)
        number2 = "[6:number1/a_data%s:2]" % (datarange - 2)
        word1 = "[gapDesc:1:number1]"
        word2 = "[gapLevelDesc:1:number2]"

        number_add=[number1,number2]
        word_add=[word1,word2]
        number=number+number_add
        word=word+word_add

        text='从'+str(result['moduleName'])+'的角度来讲，人们对'+str(indexName)+'的考察是必不可少的。' \
            '由最新更新的数据显示，最近三年'+str(indexName)+'的数据呈现[word1]趋势。' \
            '由具体数据来看，[time'+str(datarange)+']该指标的数据为[a_data'+str(datarange)+\
             ']'+result['dataUnit']+'，[time'+str(datarange-1)+']该指标的数据为' \
            '[a_data'+str(datarange-1)+']'+result['dataUnit']+'，[time'+str(datarange-2)+\
             ']该指标的数据为[a_data'+str(datarange-2)+']'+result['dataUnit']+'。这三年的变化率为[number2]，' \
            '相对来说变化速率较为[word2]。同时，我们可以从这三年的统计数据得出，该指标的平均值为[a_avg]'+result['dataUnit']+'。'

        return text,word,number



#大模板1
    def module4(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[3:a_gap%s:2]" % (datarange - 1)
        number2 = "[3:a_changeRate%s:2]" % (datarange - 1)
        number3 = "[4:a_changeRate%s-a_changeRate%s:1]" % (datarange - 1, datarange - 2)
        number4 = "[4:a_changeRate%s-a_changeRate%s:3]" % (datarange - 1, datarange - 2)
        number5 = "[4: a_data%s-a_data1:1]" % (datarange)
        number6 = "[4: a_data%s-a_data1: 2]" % (datarange)
        word1 = "[gapDesc:1:a_gap%s]" % (datarange - 1)
        word2 = "[gapLevelDesc:1:a_changeRate%s]" % (datarange - 1)
        word3 = "[rateChangeDesc:1:number3]"
        word4 = "[gapDesc:1: number5]"

        number_add = [number1, number2, number3, number4, number5, number6]
        word_add = [word1, word2, word3, word4]
        number = number + number_add
        word = word + word_add


        text1 = '据最新统计数据显示，截至[time' + str(datarange) + ']，' \
                +str(indexName)+'的数据达到了[a_data'+str(datarange)+']'+str(result['dataUnit'])+'，' \
                '该指标在[time'+str(datarange-1)+']同期的数据为[a_data'+str(datarange-1)+']'+str(result['dataUnit'])+'。' \
                '与[time'+str(datarange-1)+']同期相比[word1]了[number1]'+str(result['dataUnit'])+'，' \
                '同比[word1][number2]，[word1]规模较为[word2]，变化率较上一年度[word3][number4]个百分点。'
        text2='根据[time1-time'+str(datarange) +']中'+str(indexName)+'的统计数据，' \
            '我们可以很直观的看出，自从[time1]以来，'+str(indexName)+'经历了一定程度的[word4]，' \
             '[time'+str(datarange) +']相比于[time1]，[word4]了[number6]'+str(result['dataUnit'])+'。' \
            '具体来说，从在最开始的[time1]的数据为[a_data1]'+str(result['dataUnit'])+'，' \
            '最后在[time'+str(datarange)+']年末达到了[a_data'+str(datarange)+']'+str(result['dataUnit'])+'。'
        text3='从平均值和最大最小值的角度来分析，[time1-time'+str(datarange)+']期间，'+ \
            str(indexName)+'平均值为[a_avg]'+str(result['dataUnit'])+'。' \
            '同时，由具体数据可知，在这几年中，我国'+str(indexName)+ \
            '最大值曾达到[a_max]'+str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'。'

        text = text1 + text2 + text3
        return text,word,number


#模板一的衍生模板1
    def module5(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[3:a_gap%s:2]" % (datarange - 1)
        number2 = "[3:a_changeRate%s:2]" % (datarange - 1)
        number3 = "[4:a_changeRate%s-a_changeRate%s:1]" % (datarange - 1, datarange - 2)
        number4 = "[4:a_changeRate%s-a_changeRate%s:3]" % (datarange - 1, datarange - 2)
        number5 = "[4: a_data%s-a_data1:1]" % (datarange)
        number6 = "[4: a_data%s-a_data1: 2]" % (datarange)
        word1 = "[gapDesc:1:a_gap%s]" % (datarange - 1)
        word2 = "[gapLevelDesc:1:a_changeRate%s]" % (datarange - 1)
        word3 = "[rateChangeDesc:1:number3]"
        word4 = "[gapDesc:1: number5]"

        number_add = [number1, number2, number3, number4, number5, number6]
        word_add = [word1, word2, word3, word4]
        number = number + number_add
        word = word + word_add

        text1 = '针对统计局对'+str(indexName)+'的统计调查，我们可以得到可靠的统计数据如下。' \
                '截至[time' + str(datarange) + ']，' \
                +str(indexName)+'的值为[a_data'+str(datarange)+']'+str(result['dataUnit'])+'，' \
                '该指标在[time'+str(datarange-1)+']同期的值为[a_data'+str(datarange-1)+']'+str(result['dataUnit'])+'。' \
                '与[time'+str(datarange-1)+']同期相比[word1]了[number1]'+str(result['dataUnit'])+'，' \
                '同比[word1][number2]，[word1]规模较为[word2]，变化率较上一年度[word3][number4]个百分点。'
        text2='根据[time1-time'+str(datarange) +']中'+str(indexName)+'的统计数据，' \
            '从变化率的角度来看，我们可以从大体上看出，自从[time1]以来，'+str(indexName)+'经历了一定程度的[word4]，' \
             '[time'+str(datarange) +']相比于[time1]，[word4]了[number6]'+str(result['dataUnit'])+'。' \
            '具体来说，从在最开始的[time1]的数据为[a_data1]'+str(result['dataUnit'])+'，' \
            '最后在[time'+str(datarange)+']年末达到了[a_data'+str(datarange)+']'+str(result['dataUnit'])+'。'
        text3='[time1-time'+str(datarange)+']期间，'+ \
            str(indexName)+'平均值为[a_avg]'+str(result['dataUnit'])+'。' \
            '从数据的峰值和谷值我们可以具体看出，在这几年中，我国'+str(indexName)+ \
            '最大值曾达到[a_max]'+str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'。'

        text = text1 + text2 + text3
        return text,word,number

#模板一的衍生模板2
    def module6(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[3:a_gap%s:2]" % (datarange - 1)
        number2 = "[3:a_changeRate%s:2]" % (datarange - 1)
        number3 = "[4:a_changeRate%s-a_changeRate%s:1]" % (datarange - 1, datarange - 2)
        number4 = "[4:a_changeRate%s-a_changeRate%s:3]" % (datarange - 1, datarange - 2)
        number5 = "[4: a_data%s-a_data1:1]" % (datarange)
        number6 = "[4: a_data%s-a_data1: 2]" % (datarange)
        word1 = "[gapDesc:1:a_gap%s]" % (datarange - 1)
        word2 = "[gapLevelDesc:1:a_changeRate%s]" % (datarange - 1)
        word3 = "[rateChangeDesc:1:number3]"
        word4 = "[gapDesc:1: number5]"

        number_add = [number1, number2, number3, number4, number5, number6]
        word_add = [word1, word2, word3, word4]
        number = number + number_add
        word = word + word_add

        text1='随着社会的发展，'+str(indexName)+'越来越收到广大民众的关注，统计局最新得出的统计数据如下。'
        text2='从宏观的数据大体来看，[time1-time'+str(datarange)+']期间，'+ \
            str(indexName)+'平均值为[a_avg]'+str(result['dataUnit'])+'。' \
            '从数据的峰值和谷值我们可以具体看出，在这几年中，我国'+str(indexName)+ \
            '最大值曾达到[a_max]'+str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'。'
        text3='截至[time' + str(datarange) + ']，' \
                +str(indexName)+'的值为[a_data'+str(datarange)+']'+str(result['dataUnit'])+'，' \
                '该指标在[time'+str(datarange-1)+']同期的值为[a_data'+str(datarange-1)+']'+str(result['dataUnit'])+'。' \
                '与[time'+str(datarange-1)+']同期相比[word1]了[number1]'+str(result['dataUnit'])+'，' \
                '同比[word1][number2]，[word1]规模较为[word2]，变化率较上一年度[word3][number4]个百分点。'
        text4='根据[time1-time'+str(datarange) +']中'+str(indexName)+'的统计数据，' \
            '从变化率的角度来看，我们可以从大体上看出，自从[time1]以来，'+str(indexName)+'经历了一定程度的[word4]，' \
             '[time'+str(datarange) +']相比于[time1]，[word4]了[number6]'+str(result['dataUnit'])+'。' \
            '具体来说，从在最开始的[time1]的数据为[a_data1]'+str(result['dataUnit'])+'，' \
            '最后在[time'+str(datarange)+']年末达到了[a_data'+str(datarange)+']'+str(result['dataUnit'])+'。'
        text = text1 + text2 + text3+text4
        return text,word,number

#模板一的衍生模板3
    def module7(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[3:a_gap%s:2]" % (datarange - 1)
        number2 = "[3:a_changeRate%s:2]" % (datarange - 1)
        number3 = "[4:a_changeRate%s-a_changeRate%s:1]" % (datarange - 1, datarange - 2)
        number4 = "[4:a_changeRate%s-a_changeRate%s:3]" % (datarange - 1, datarange - 2)
        number5 = "[4: a_data%s-a_data1:1]" % (datarange)
        number6 = "[4: a_data%s-a_data1: 2]" % (datarange)
        word1 = "[gapDesc:1:a_gap%s]" % (datarange - 1)
        word2 = "[gapLevelDesc:1:a_changeRate%s]" % (datarange - 1)
        word3 = "[rateChangeDesc:1:number3]"
        word4 = "[gapDesc:1: number5]"

        number_add = [number1, number2, number3, number4, number5, number6]
        word_add = [word1, word2, word3, word4]
        number = number + number_add
        word = word + word_add

        text1='从宏观的角度分析'+str(indexName)+'，[time1-time'+str(datarange)+']期间，'+ \
            str(indexName)+'平均值为[a_avg]'+str(result['dataUnit'])+'。' \
            '从数据的峰值和谷值我们可以具体看出，在这几年中，我国'+str(indexName)+ \
            '最大值曾达到[a_max]'+str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'。'
        text2='从微观的角度分析，我们可以根据具体数据得出，截至[time' + str(datarange) + ']，' \
                +str(indexName)+'的值为[a_data'+str(datarange)+']'+str(result['dataUnit'])+'，' \
                '该指标在[time'+str(datarange-1)+']同期的值为[a_data'+str(datarange-1)+']'+str(result['dataUnit'])+'。' \
                '与[time'+str(datarange-1)+']同期相比[word1]了[number1]'+str(result['dataUnit'])+'，' \
                '同比[word1][number2]，[word1]规模较为[word2]，变化率较上一年度[word3][number4]个百分点。'
        text3='根据[time1-time'+str(datarange) +']中'+str(indexName)+'的统计数据，' \
            '从变化率的角度来看，我们可以从大体上看出，自从[time1]以来，'+str(indexName)+'经历了一定程度的[word4]，' \
             '[time'+str(datarange) +']相比于[time1]，[word4]了[number6]'+str(result['dataUnit'])+'。' \
            '具体来说，从在最开始的[time1]的数据为[a_data1]'+str(result['dataUnit'])+'，' \
            '最后在[time'+str(datarange)+']年末达到了[a_data'+str(datarange)+']'+str(result['dataUnit'])+'。'
        text = text1 + text2 + text3
        return text,word,number


#模板一的衍生模板4
    def module8(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[3:a_gap%s:2]" % (datarange - 1)
        number2 = "[3:a_changeRate%s:2]" % (datarange - 1)
        number3 = "[4:a_changeRate%s-a_changeRate%s:1]" % (datarange - 1, datarange - 2)
        number4 = "[4:a_changeRate%s-a_changeRate%s:3]" % (datarange - 1, datarange - 2)
        number5 = "[4: a_data%s-a_data1:1]" % (datarange)
        number6 = "[4: a_data%s-a_data1: 2]" % (datarange)
        word1 = "[gapDesc:1:a_gap%s]" % (datarange - 1)
        word2 = "[gapLevelDesc:1:a_changeRate%s]" % (datarange - 1)
        word3 = "[rateChangeDesc:1:number3]"
        word4 = "[gapDesc:1: number5]"

        number_add = [number1, number2, number3, number4, number5, number6]
        word_add = [word1, word2, word3, word4]
        number = number + number_add
        word = word + word_add

        text1 = '由最近获得的对'+str(indexName)+'的统计结果可知，截至[time' + str(datarange) + ']，' \
                +str(indexName)+'的数据达到了[a_data'+str(datarange)+']'+str(result['dataUnit'])+'，' \
                '该指标在[time'+str(datarange-1)+']同期的数据为[a_data'+str(datarange-1)+']'+str(result['dataUnit'])+'。' \
                '与[time'+str(datarange-1)+']同期相比[word1]了[number1]'+str(result['dataUnit'])+'，' \
                '同比[word1][number2]，[word1]规模较为[word2]，变化率较上一年度[word3][number4]个百分点。'
        text2='根据[time1-time'+str(datarange) +']中'+str(indexName)+'的统计数据，' \
            '可以准确的看出，自从[time1]以来，'+str(indexName)+'经历了一定程度的[word4]，' \
             '[time'+str(datarange) +']相比于[time1]，[word4]了[number6]'+str(result['dataUnit'])+'。' \
            '具体来说，从在最开始的[time1]的数据为[a_data1]'+str(result['dataUnit'])+'，' \
            '最后在[time'+str(datarange)+']年末达到了[a_data'+str(datarange)+']'+str(result['dataUnit'])+'。'
        text3='同时，还值得注意的是，[time1-time'+str(datarange)+']期间，'+ \
            str(indexName)+'平均值为[a_avg]'+str(result['dataUnit'])+'。' \
            '同时，由具体数据可知，在这几年中，我国'+str(indexName)+ \
            '最大值曾达到[a_max]'+str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'。'
        text = text1 + text2 + text3
        return text,word,number

#模板一的衍生模板5
    def module9(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        number1 = "[3:a_gap%s:2]" % (datarange - 1)
        number2 = "[3:a_changeRate%s:2]" % (datarange - 1)
        number3 = "[4:a_changeRate%s-a_changeRate%s:1]" % (datarange - 1, datarange - 2)
        number4 = "[4:a_changeRate%s-a_changeRate%s:3]" % (datarange - 1, datarange - 2)
        number5 = "[4: a_data%s-a_data1:1]" % (datarange)
        number6 = "[4: a_data%s-a_data1: 2]" % (datarange)
        word1 = "[gapDesc:1:a_gap%s]" % (datarange - 1)
        word2 = "[gapLevelDesc:1:a_changeRate%s]" % (datarange - 1)
        word3 = "[rateChangeDesc:1:number3]"
        word4 = "[gapDesc:1: number5]"

        number_add = [number1, number2, number3, number4, number5, number6]
        word_add = [word1, word2, word3, word4]
        number = number + number_add
        word = word + word_add

        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        print(area)
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        text1='随着经济社会的发展，在大数据的社会，人们对'+str(indexName)+'的关注程度也越来越高。'
        text2='从平均值角度来讲，在[time1-time'+str(datarange)+']，'+ \
            str(indexName)+'平均值为[a_avg]'+str(result['dataUnit'])+'。' \
            '最高值和最低值也能在一定程度上代表数据的发展趋势，在这几年中，我国'+str(indexName)+ \
            '最大值曾达到[a_max]'+str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'。'
        text3='截至[time' + str(datarange) + ']，' \
                +str(indexName)+'的值为[a_data'+str(datarange)+']'+str(result['dataUnit'])+'，' \
                '该指标在[time'+str(datarange-1)+']同期的值为[a_data'+str(datarange-1)+']'+str(result['dataUnit'])+'。' \
                '与[time'+str(datarange-1)+']同期相比[word1]了[number1]'+str(result['dataUnit'])+'，' \
                '同比[word1][number2]，[word1]规模较为[word2]，变化率较上一年度[word3][number4]个百分点。'
        text4='根据[time1-time'+str(datarange) +']中'+str(indexName)+'的统计数据，' \
            '从变化率的角度来看，可以直观的得出，自从[time1]以来，'+str(indexName)+'经历了一定程度的[word4]，' \
             '[time'+str(datarange) +']相比于[time1]，[word4]了[number6]'+str(result['dataUnit'])+'。' \
            '具体来说，从在最开始的[time1]的数据为[a_data1]'+str(result['dataUnit'])+'，' \
            '最后在[time'+str(datarange)+']年末达到了[a_data'+str(datarange)+']'+str(result['dataUnit'])+'。'
        text = text1 + text2 + text3+text4
        return text,word,number

#模板一的衍生模板6
    def module10(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[3:a_gap%s:2]" % (datarange - 1)
        number2 = "[3:a_changeRate%s:2]" % (datarange - 1)
        number3 = "[4:a_changeRate%s-a_changeRate%s:1]" % (datarange - 1, datarange - 2)
        number4 = "[4:a_changeRate%s-a_changeRate%s:3]" % (datarange - 1, datarange - 2)
        number5 = "[4: a_data%s-a_data1:1]" % (datarange)
        number6 = "[4: a_data%s-a_data1: 2]" % (datarange)
        word1 = "[gapDesc:1:a_gap%s]" % (datarange - 1)
        word2 = "[gapLevelDesc:1:a_changeRate%s]" % (datarange - 1)
        word3 = "[rateChangeDesc:1:number3]"
        word4 = "[gapDesc:1: number5]"

        number_add = [number1, number2, number3, number4, number5, number6]
        word_add = [word1, word2, word3, word4]
        number = number + number_add
        word = word + word_add

        text1='最近这几年来，人们对'+str(indexName)+'的关心程度呈现一定程度的增长趋势。'
        text2='具体来说，截至[time' + str(datarange) + ']，' \
                +str(indexName)+'的值为[a_data'+str(datarange)+']'+str(result['dataUnit'])+'，' \
                '该指标在[time'+str(datarange-1)+']同期的值为[a_data'+str(datarange-1)+']'+str(result['dataUnit'])+'。' \
                '与[time'+str(datarange-1)+']同期相比[word1]了[number1]'+str(result['dataUnit'])+'，' \
                '同比[word1][number2]，[word1]规模较为[word2]，变化率较上一年度[word3][number4]个百分点。'
        text3='根据[time1-time'+str(datarange) +']中'+str(indexName)+'的统计数据，' \
            '从变化率的角度来看，我们可以从大体上看出，自从[time1]以来，'+str(indexName)+'经历了一定程度的[word4]，' \
             '[time'+str(datarange) +']相比于[time1]，[word4]了[number6]'+str(result['dataUnit'])+'。' \
            '具体来说，从在最开始的[time1]的数据为[a_data1]'+str(result['dataUnit'])+'，' \
            '最后在[time'+str(datarange)+']年末达到了[a_data'+str(datarange)+']'+str(result['dataUnit'])+'。'
        text4='从宏观的数据大体来看，[time1-time'+str(datarange)+']期间，'+ \
            str(indexName)+'平均值为[a_avg]'+str(result['dataUnit'])+'。' \
            '从数据的峰值和谷值我们可以具体看出，在这几年中，我国'+str(indexName)+ \
            '最大值曾达到[a_max]'+str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'。'

        text = text1 + text2 + text3+text4
        return text,word,number

#大模板2
    def module11(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[4:a_data%s-a_data%s:1]" % (datarange, datarange - 4)
        number2 = "[4:a_data%s-a_data%s:2]" % (datarange, datarange - 4)
        number3 = "[6:number1/a_data%s:2]" % (datarange - 4)
        number4 = "[4:a_data%s-a_data1:2]" % (datarange)
        word1 = "[gapDesc:1:number1]"
        word2 = "[gapDesc:1:number4]"

        number_add=[number1,number2,number3,number4]
        word_add=[word1,word2]
        number=number+number_add
        word=word+word_add


        text='从最近五年最新的统计局数据来看，' \
             '截止于[time'+str(datarange)+']，'+str(indexName)+'达到[a_data'+str(datarange)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-1)+']，该指标的数据达到[a_data'+str(datarange-1)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-2)+']，该指标的数据达到[a_data'+str(datarange-2)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-3)+']，该指标的数据达到[a_data'+str(datarange-3)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-4)+']，该指标的数据达到[a_data'+str(datarange-4)+']'+result['dataUnit']+'.' \
             '根据所提供的数据来看，该指标最近五年[word1]了[number2]'+result['dataUnit']+'，变化率同比[word1][number3]。' \
             '从历史数据角度来看，时间最久远一期的数据为[time1]，具体统计数据为[a_data1]'+result['dataUnit']+'。' \
             '同时，总整体的角度来分析，在[time1-time'+str(datarange)+']期间，'+str(indexName)+'最大值曾达到[a_max]'+\
             str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'，总体呈现为[word2]趋势。'
        return text,word,number

#模板二的衍生模板1
    def module12(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[4:a_data%s-a_data%s:1]" % (datarange, datarange - 4)
        number2 = "[4:a_data%s-a_data%s:2]" % (datarange, datarange - 4)
        number3 = "[6:number1/a_data%s:2]" % (datarange - 4)
        number4 = "[4:a_data%s-a_data1:2]" % (datarange)
        word1 = "[gapDesc:1:number1]"
        word2 = "[gapDesc:1:number4]"

        number_add=[number1,number2,number3,number4]
        word_add=[word1,word2]
        number=number+number_add
        word=word+word_add

        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''


        text='对于指标'+str(indexName)+'最近几年的统计数据我们可以得到如下数据，' \
             '截止于[time'+str(datarange)+']，'+str(indexName)+'达到[a_data'+str(datarange)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-1)+']，该指标的数据达到[a_data'+str(datarange-1)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-2)+']，该指标的数据达到[a_data'+str(datarange-2)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-3)+']，该指标的数据达到[a_data'+str(datarange-3)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-4)+']，该指标的数据达到[a_data'+str(datarange-4)+']'+result['dataUnit']+'. ' \
             '由计算数据可以得出，最近五年[word1]了[number2]'+result['dataUnit']+'，变化率同比[word1][number3]。 ' \
             '我们可以根据历史数据看出，时间最久远一期的数据为[time1]，具体统计数据为[a_data1]'+result['dataUnit']+'。' \
             '同时，总整体的角度来分析，，在[time1-time'+str(datarange)+']期间，'+str(indexName)+'最大值曾达到[a_max]'+\
             str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'，总体呈现为[word2]趋势。'
        return text,word,number



#模板二的衍生模板2
    def module13(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[4:a_data%s-a_data%s:1]" % (datarange, datarange - 4)
        number2 = "[4:a_data%s-a_data%s:2]" % (datarange, datarange - 4)
        number3 = "[6:number1/a_data%s:2]" % (datarange - 4)
        number4 = "[4:a_data%s-a_data1:2]" % (datarange)
        word1 = "[gapDesc:1:number1]"
        word2 = "[gapDesc:1:number4]"

        number_add=[number1,number2,number3,number4]
        word_add=[word1,word2]
        number=number+number_add
        word=word+word_add


        text='由计算数据可以得出，最近五年指标'+str(indexName)+'[word1]了[number2]'+result['dataUnit']+'，变化率同比[word1][number3]。 ' \
             '具体来说，截止于[time'+str(datarange)+']，'+str(indexName)+'达到[a_data'+str(datarange)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-1)+']，该指标的数据达到[a_data'+str(datarange-1)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-2)+']，该指标的数据达到[a_data'+str(datarange-2)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-3)+']，该指标的数据达到[a_data'+str(datarange-3)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-4)+']，该指标的数据达到[a_data'+str(datarange-4)+']'+result['dataUnit']+'。' \
             '根据历史数据我们可以知道，在[time1]，具体统计数据为[a_data1]'+result['dataUnit']+'。' \
             '同时，总整体的角度来分析，，在[time1-time'+str(datarange)+']期间，'+str(indexName)+'最大值曾达到[a_max]'+\
             str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'，总体呈现为[word2]趋势。'
        return text,word,number


#模板二的衍生模板3
    def module14(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[4:a_data%s-a_data%s:1]" % (datarange, datarange - 4)
        number2 = "[4:a_data%s-a_data%s:2]" % (datarange, datarange - 4)
        number3 = "[6:number1/a_data%s:2]" % (datarange - 4)
        number4 = "[4:a_data%s-a_data1:2]" % (datarange)
        word1 = "[gapDesc:1:number1]"
        word2 = "[gapDesc:1:number4]"

        number_add=[number1,number2,number3,number4]
        word_add=[word1,word2]
        number=number+number_add
        word=word+word_add

        text='指标'+str(indexName)+'最近几年的发展情况已经引起了大多数人的注意，' \
             '截止于[time'+str(datarange)+']，'+str(indexName)+'达到[a_data'+str(datarange)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-1)+']，该指标的数据达到[a_data'+str(datarange-1)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-2)+']，该指标的数据达到[a_data'+str(datarange-2)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-3)+']，该指标的数据达到[a_data'+str(datarange-3)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-4)+']，该指标的数据达到[a_data'+str(datarange-4)+']'+result['dataUnit']+'。' \
             '根据上述数据可以得出，最近五年[word1]了[number2]'+result['dataUnit']+'，变化率同比[word1][number3]。' \
             '我们可以根据历史数据看出，时间最久远一期的数据为[time1]，具体统计数据为[a_data1]'+result['dataUnit']+'。' \
             '同时，总整体的角度来分析，，在[time1-time'+str(datarange)+']期间，'+str(indexName)+'最大值曾达到[a_max]'+\
             str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'，总体呈现为[word2]趋势。'
        return text,word,number


#模板二的衍生模板4
    def module15(self):
        word = self.word
        number = self.number
        result = self.result
        datarange=self.datarange
        area=self.area
        #对单位进行处理
        if (result['dataUnit'] == None):
            result['dataUnit'] = ''
        if (result['dataUnit'] == 'None'):
            result['dataUnit'] = ''
        #对地区area进行处理
        if(area!='-1'):
            if(len(area)==6):
                sql = "select area_name from area where code = " + str(area)
                res1 = rs.SuccessSql(sql, isSelect=True)[0]
                area = res1['area_name']
            indexName=area+'的'+result['indexName']
        else:
            indexName=result['indexName']

        number1 = "[4:a_data%s-a_data%s:1]" % (datarange, datarange - 4)
        number2 = "[4:a_data%s-a_data%s:2]" % (datarange, datarange - 4)
        number3 = "[6:number1/a_data%s:2]" % (datarange - 4)
        number4 = "[4:a_data%s-a_data1:2]" % (datarange)
        word1 = "[gapDesc:1:number1]"
        word2 = "[gapDesc:1:number4]"

        number_add=[number1,number2,number3,number4]
        word_add=[word1,word2]
        number=number+number_add
        word=word+word_add

        text='截止于[time'+str(datarange)+']，'+str(indexName)+'达到[a_data'+str(datarange)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-1)+']，该指标的数据达到[a_data'+str(datarange-1)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-2)+']，该指标的数据达到[a_data'+str(datarange-2)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-3)+']，该指标的数据达到[a_data'+str(datarange-3)+']'+result['dataUnit']+'；' \
             '[time'+str(datarange-4)+']，该指标的数据达到[a_data'+str(datarange-4)+']'+result['dataUnit']+'。' \
             '由计算数据可以得出，最近五年[word1]了[number2]'+result['dataUnit']+'，变化率同比[word1][number3]。' \
             '我们可以根据历史数据看出，时间最久远一期的数据为[time1]，具体统计数据为[a_data1]'+result['dataUnit']+'。' \
             '同时，总整体的角度来分析，，在[time1-time'+str(datarange)+']期间，'+str(indexName)+'最大值曾达到[a_max]'+\
             str(result['dataUnit'])+'，最小值曾达到[a_min]'+str(result['dataUnit'])+'，总体呈现为[word2]趋势。'
        return text,word,number










# word=[]
# number=[]
# m=ModuleType(8)
# text,word,number=m.module1(word,number)
# print(text)
# print(word)
# print(number)