# coding=utf-8
import urllib.request
import json
from pyquery import PyQuery as pq
import requests
from bs4 import BeautifulSoup
import re
import csv

# 定义要爬取的微博大V的微博ID
ids = {'Airbnb':'3787942764',
       '哈啰出行':'6028267033',
       '滴滴出行':'2838754010',
       '美团外卖':'3949575070',
       '饿了么':'1282440983',
       '贝壳找房':'6512266446',
       '曹操出行':'5624879103',
       'ofo':'5122220173',
       '闲鱼':'2191744334',
       '掌上链家':'2298955763',
       '蛋壳公寓':'5712515570',
       '怪兽充电':'6270489029',
       '街电':'5889599357',
       '来电':'5902738661',
       '优信':'6252807875'}
# 设置代理IP
proxy_addr = "192.168.1.101"


# 定义页面打开函数
def use_proxy(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    return data


# 获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data = use_proxy(url, proxy_addr)
    content = json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if (data.get('tab_type') == 'weibo'):
            containerid = data.get('containerid')
    return containerid


# 获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
    data = use_proxy(url, proxy_addr)
    content = json.loads(data).get('data')
    profile_image_url = content.get('userInfo').get('profile_image_url')
    description = content.get('userInfo').get('description')
    profile_url = content.get('userInfo').get('profile_url')
    verified = content.get('userInfo').get('verified')
    guanzhu = content.get('userInfo').get('follow_count')
    name = content.get('userInfo').get('screen_name')
    fensi = content.get('userInfo').get('followers_count')
    gender = content.get('userInfo').get('gender')
    urank = content.get('userInfo').get('urank')
    print("微博昵称：" + name + "\n" + "微博主页地址：" + profile_url + "\n" + "微博头像地址：" + profile_image_url + "\n" + "是否认证：" + str(
        verified) + "\n" + "微博说明：" + description + "\n" + "关注人数：" + str(guanzhu) + "\n" + "粉丝数：" + str(
        fensi) + "\n" + "性别：" + gender + "\n" + "微博等级：" + str(urank) + "\n")
    return name


# 获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id, file):
    # 创建csv文件
    with open(file, 'w+', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(("微博地址", "发布时间", "微博内容", "点赞数", "评论数", "转发数", "评论"))
    i = 1
    itemid = ''
    while True:
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + get_containerid(
            url) + '&page=' + str(i)
        try:
            data = use_proxy(weibo_url, proxy_addr)
            content = json.loads(data).get('data')
            cards = content.get('cards')
            if len(cards) > 0 and cards[0].get('itemid') != itemid:
                itemid = cards[0].get('itemid')
                for j in range(len(cards)):
                    print("-----正在爬取第" + str(i) + "页，第" + str(j) + "条微博------")
                    card_type = cards[j].get('card_type')
                    if (card_type == 9):
                        mblog = cards[j].get('mblog')
                        attitudes_count = mblog.get('attitudes_count')
                        comments_count = mblog.get('comments_count')
                        created_at = mblog.get('created_at')
                        reposts_count = mblog.get('reposts_count')
                        scheme = cards[j].get('scheme')
                        ids = mblog.get('id')
                        with open(file, 'a', encoding='utf-8') as csvFile:
                            writer = csv.writer(csvFile)
                            writer.writerow((scheme, created_at, get_detail(ids), attitudes_count, comments_count,
                                             reposts_count, get_comment(ids)))
                i += 1
            else:
                break
        except Exception as e:
            print(e)


def get_comment(id):
    comments = []
    try:
        url = 'https://m.weibo.cn/comments/hotflow?id=' + id + '&mid=' + id + '&max_id_type=0'
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        datas = content.get('data')
        for i in range(0, 15):
            comments.append(pq(datas[i].get('text')).text().replace('<span class=\"Text\".*?>.*?</span>', ''))
    except Exception as e:
        print(e)
        pass
    return comments


def get_detail(id):
    try:
        url = 'https://m.weibo.cn/statuses/extend?id=' + id
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        longTextContent = content.get('longTextContent')
        text = pq(longTextContent).text().replace('\n', '')
    except Exception as e:
        print(e)
        pass
    return text


if __name__ == "__main__":
    for id in ids.values():
        name = get_userInfo(id)
        file = name + ".csv"
        directory = "sharingEconomy"
        file = directory + "\\" + file
        get_weibo(id, file)
