# 16124278 王浩 流浪地球 Comments_Group
# -*- coding: UTF-8 -*-
import datetime  # 日期
import os
from Analyze_Data import read_csv


# 根据评分将评论数据分为中评好评和差评
def judgeRank(score):
    if score == 5.0 or score == 4.5 or score == 4.0:
        return '好评'
    elif score == 0.5 or score == 1.0 or score == 1.5:
        return '差评'
    else:
        return '中评'


def preProcess(sen):
    return sen.replace('\n', '').replace('\t', '').replace('\u3000', '')


# 完成数据预处理
def group_comments(comments):
    data = comments[['score', 'content']].dropna()  # 获取评分及评论内容
    data = data[~data['score'].isin([0])]  # 去除没有评分的评论数据（即猫眼评分为0的评论，最低分为0.5）
    data['rank'] = data.score.apply(lambda score: judgeRank(score))  # 根据评分将评论数据分为中评好评和差评
    data['content'] = data.content.apply(lambda sen: preProcess(sen))  # 去除评论数据中的空格与换行符，避免后续模型训练读取数据时出现错误
    data['info'] = data['rank'] + '\t' + data['content']
    print(data['info'])
    # 总计523046条有效影评数据
    if os.path.exists(out_dirname+'comments.train.txt') and \
            os.path.exists(out_dirname+'comments.test.txt') and \
            os.path.exists(out_dirname+'comments.val.txt'): #先判断文件是否存在
        return
    else:
        data[0:10000]['info'].to_csv(out_dirname + 'comments.test.txt', sep='\n', index=False)  # 10000条数据用做测试集
        data[10000:20000]['info'].to_csv(out_dirname + 'comments.val.txt', sep='\n', index=False)  # 10000条数据用作验证集
        data[20000:len(data)]['info'].to_csv(out_dirname + 'comments.train.txt', sep='\n', index=False)  # 剩余的503046条数据用作训练集


if __name__ == "__main__":
    start_time = datetime.datetime.now()  # 开始计时
    in_filename = "./input/Comments.csv"
    out_dirname = "./comments/"
    titles = ['nickName', 'cityName', 'content', 'score', 'startTime']
    comments = read_csv(in_filename, titles)

    group_comments(comments)  # 完成数据预处理

    end_time = datetime.datetime.now()  # 结束记时
    print("全部完成!!!")
    print('程序运行用时(秒):', (end_time - start_time).seconds)
