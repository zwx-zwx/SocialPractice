#导入模块
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import expon
import statsmodels.api as sm
import pylab
import xlrd
import csv


filename = 'merge.csv'
df = pd.read_csv(filename, encoding='utf-8')
filename2='每条'+filename
df2= pd.read_csv(filename2, encoding='GBK')

# print(df2)
# print(df2.shape)
# print()
# print(df2.columns)
# print()
# print(df2.index)
# print()
# print(df2.dtypes)

# (3862, 7)
# Index(['微博地址', '发布时间', '微博内容', '点赞数', '评论数', '转发数', '评论'], dtype='object')
#
# RangeIndex(start=0, stop=3862, step=1)
#
# 微博地址    object
# 发布时间    object
# 微博内容    object
# 点赞数     object
# 评论数     object
# 转发数     object
# 评论      object
# dtype: object

#                        评论
# 0                马住，周末心愿单
# 1                      马住
# 2                 周末可以去看看
# 3                     有意思
# 4                   电影即视感
# ...                   ...
# 35224                土味可爱
# 35225      可是不开学，饿了么券都过期了
# 35226              好土味的感觉
# 35227  大哥，wifi下无法显示图片解决了没
# 35228                 棒棒棒
#
# [35229 rows x 1 columns]
# (35229, 1)
#
# Index(['评论'], dtype='object')
#
# RangeIndex(start=0, stop=35229, step=1)
#
# 评论    object
# dtype: object



#转换成 每条评论
with open('每条'+filename, 'w', newline='') as wr:
    writer = csv.writer(wr)
    with open(filename, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            # 行号从1开始
            try:
                dic=row[6]
                # print(dic)(1, '微博地址')
                # print(dic+"1")
                # print(dic)
                # str = dic[1]
                try:
                    list = dic.split("'")
                    print(list)
                    for str in list:
                        if ((len(str) > 1)&(str!=', ')):
                            try:
                            # for row in list:
                                writer.writerow([str])
                            except UnicodeEncodeError:
                                pass
                except AttributeError:
                    pass
            except IndexError:
                pass




#字典统计
# # df = pd.read_json('人民日报.json')
# df = pd.read_excel("stage4-检验.xlsx", sheet_name='JSON',usecols=[0,1, 2, 3, 4])
# # (5401, 5)
# context=2
# rel=4
# sta=100
# end=sta+100
#
#
# # s1 = pd.Series([1,'a',5.2,7])
# # print(s1[3])
#
# # print(df.columns)#Index(['微博地址:', '发布时间:', '微博标题:', '转发数', '疫情相关 1 相关  0 无关'], dtype='object')
# # print(df)
# # print(df.shape)
# # print(df.columns)#Index(['微博地址:', '微博内容:', '点赞数:', '评论数', '转发数', '评论'], dtype='object')
# # print(df.loc[1])#字典输出

# rela1=["诚信",
# "欺诈",
# "承诺",
# "骗钱",
# "杀熟",
# "信用",
# "欺骗",
# "诈骗",
# "骗子"
# ]
# rela2=[
# "价格"
# "便宜",
# "收费",
# "费用",
# "涨价",
# ]
# rela3=[
# "违规",
# "维权",
# "强制",
# "法律",
# "督促",
# "利益",
# "监督",
# "权益",
# "保障"
# ]
# rela4=[
# "态度恶劣",
# "踢皮球",
# "投诉无门",
# "客服",
# "赔偿",
# "报修",
# "理赔"
# ]
# rela5=[
# "界面",
# "设计",
# "打不开",
# "好看",
# "功能",
# "创意"
# ]
# rela6=[
# "浪费时间",
# "麻烦",
# "方便",
# "越来越少"
# ]
# rela7=[
# "安全",
# "健康",
# "平安"
# ]
# rela8=[
# "浪费",
# "环保"
# ]
rela1=[
"卸载",
"投诉",
"垃圾",
"恶心",
"退钱",
"恶意",
"欺骗",
"辣鸡",
"态度恶劣",
"骗钱",
"滚蛋",
"无耻",
"黑心",
"解决不了",
"不要脸",
"呵呵",
"差评",
"搞笑",
"欺诈",
"极差",
]
rela2=[
"批评",
"投诉无门",
"浪费时间",
"建议",
"踢皮球",
"莫名其妙",
"解释一下",
"不够",
"麻烦",
"管管",
"忽悠",
"担心",
"维护",
"越来越少",
"不好",
"失望",
]
rela3=[
"方便",
"便宜",
"放心",
"感兴趣",
"很棒",
"安全",
"舒服",
"好评",
"良心",
"支持",
"点赞",
"羡慕",
"有趣",
"开心",
"美好",
"想要",
'好看',
"不错",
"赶紧",
"感谢",
"哈哈哈",
"加油"
]
rela4=[
"棒棒",
"卧槽",
"好棒",
"激动",
"厉害",
"哇塞",
"太棒了",
"期待",
"真棒",
"好好",
"幸福"
]
q=0
w=0
e=0
r=0
# t=0
# y=0
# u=0
# l=0
for i in range(0,len(df2)):
    s = df2.loc[i]
    st =s[0]
    # print(st)
    for re in rela1:
        if(st.find(re)!=-1):
            q+=1
            break
    for re in rela2:
        if(st.find(re)!=-1):
            w+=1
            break
    for re in rela3:
        if(st.find(re)!=-1):
            e+=1
            break
    for re in rela4:
        if(st.find(re)!=-1):
            r+=1
            break
    # for re in rela5:
    #     if(st.find(re)!=-1):
    #         t+=1
    #         break
    # for re in rela6:
    #     if(st.find(re)!=-1):
    #         y+=1
    #         break
    # for re in rela7:
    #     if(st.find(re)!=-1):
    #         u+=1
    #         break
    # for re in rela8:
    #     if(st.find(re)!=-1):
    #         l+=1
    #         break
print(q)
print(w)
print(e)
print(r)
# print(t)
# print(y)
# print(u)
# print(l)
