# 16124278 王浩 流浪地球 Get_Data
# -*- coding: UTF-8 -*-

import requests  # 爬虫库
import json  # 评论网站（猫眼）json数据解析 http://m.maoyan.com/mmdb/comments/movie/248906.json?_v_=yes&offset=0&startTime=2019-02-05%2020:28:22
import time  # 程序内部时间控制
import datetime  # 获取时间
import pandas as pd


# 请求评论api接口
def requestApi(url):
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    }  # 模仿手机客户端（iPhone ios11 Safari）获取网站json数据

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text

    except requests.HTTPError as e:  # 异常抛出
        print(e)
    except requests.RequestException as e:
        print(e)
    except:
        print("获取数据出错")


# 解析接口返回数据
def getData(html):
    json_data = json.loads(html)['cmts']
    comments = []

    # 解析数据并存入数组
    try:
        for item in json_data:
            comment = []
            comment.append(item['nickName'])  # 用户名
            comment.append(item['cityName'] if 'cityName' in item else '')  # 所在城市（如果有则记录该数据，否则不记录）
            comment.append(item['content'].strip().replace('\n', ''))  # 删除评论中的换行
            comment.append(item['score'])  # 评分星级
            comment.append(item['startTime'])  # 评论上交时间
            comments.append(comment)

        return comments

    except Exception as e:
        print(comment)
        print(e)


# 保存数据，写入excel
def saveData(comments):
    filename = './input/Comments_new.csv'
    # 将评论数据以csv文件格式保存在当前文件夹下

    dataObject = pd.DataFrame(comments)
    dataObject.to_csv(filename, mode='a', encoding="utf_8_sig", index=False, sep=',', header=False)
    # 使用utf_8_sig对字节进行有序编码，防止在系统中用某些软件直接浏览浏览时出现乱码问题，影响阅读；


# 爬虫主函数
def main():
    start = datetime.datetime.now()
    # 当前时间
    # start_time = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    # 开始抓取时间
    start_time = '2019-03-06  00:00:00'
    # 流浪地球电影上映前的所有评论
    end_time = '2018-01-01  00:00:00'

    init_time = start_time  # 记录程序开始运行的时间
    print('开始获取数据!', init_time)

    while start_time > end_time:
        url = 'http://m.maoyan.com/mmdb/comments/movie/248906.json?_v_=yes&offset=0&startTime=' + start_time.replace(
            '  ', '%20')  # 改变 startTime 字段的值来获取更多评论信息，把 offset 置为 0，把每页评论数据中最后一次评论时间作为新的 startTime 去重新请求
        html = None
        print(url)
        try:
            html = requestApi(url)

        except Exception as e:  # 如果有异常,暂停一会再爬
            time.sleep(1)  # 暂停一秒
            html = requestApi(url)

        # else: #开启慢速爬虫，防止封禁ip地址
        # time.sleep(0.5)

        comments = getData(html)
        # print(url)
        start_time = comments[14][4]  # 获取每页中最后一条评论时间,每页有15条评论
        # print(start_time)

        # 最后一条评论时间减一秒，避免爬取重复数据
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d  %H:%M:%S') + datetime.timedelta(seconds=-1)
        end = datetime.datetime.now()
        print(start_time)
        saveData(comments)

    print('获取数据完成！')
    print('程序运行用时:', start - end)


if __name__ == '__main__':
    main()
