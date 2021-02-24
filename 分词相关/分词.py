import json
from collections import Counter
import jieba
import numpy as np
import pandas as pd
import csv

def split(parameter):
    return filter(jieba.lcut(parameter)
def filter(parameter):
    stopword = []
    with open('cn_stopwords.txt', 'r', encoding='utf-8') as s:
        for line in s.readlines():
            l = line.strip()
            if l == '\\n':  # 换行符
                l = '\n'
            if l == '\\u3000':  # 制表符
                l = '\u3000'
            stopword.append(l)
    x = np.array(parameter)
    y = np.array(stopword)
    z = x[~np.in1d(x, y)]  # 去停用词
    k = [i for i in z if not i.isnumeric()]  # 去数字
    m = [i for i in k if len(i) > 1]  # 去长度为1的词
    # for word, flag in m:
    #     print('%s %s' % (word, flag))
    return np.array(m)
all = ""
filenmae = '每条merge.csv'
corpus = []
# with open('停用+切割词'+filenmae, 'w', newline='') as wr:
#     writer = csv.writer(wr)
df = pd.read_csv(filenmae, encoding='GBK')
for txt in df['评论']:
    corpus.append(txt.strip())
all_passages = len(corpus)  # 文本总数量
for line in corpus:
    # print(line)
    wordcount = Counter(filter(jieba.lcut(line)))
    # wordcount = Counter(jieba.lcut(line))
    # for key in wordcount.keys():
    #     print(key)
    # try:
    #     # for row in list:
    #     writer.writerow(wordcount)
    # except UnicodeEncodeError:
    #     pass

    for key in wordcount.keys():
        all+=key
all_words = split(all)
# import jieba.posseg as pseg
# words = pseg.cut(all)
# for word, flag in words:
#        print('%s %s' % (word, flag))
all_wordcount = Counter(all_words)  # 文本库中的词频统计
print(all_wordcount)