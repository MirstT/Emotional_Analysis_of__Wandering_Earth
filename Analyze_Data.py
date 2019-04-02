# 16124278 王浩 流浪地球 Analyze_Data
# -*- coding: UTF-8 -*-

import pandas as pd
from collections import Counter  # 计数器
from pyecharts import Geo, Bar, Page, Style, ThemeRiver, Line  # 数据可视化图表
from pyecharts.datasets.coordinates import search_coordinates_by_keyword  # 关键字匹配（地名）
import jieba  # 结巴分词
import jieba.analyse
import matplotlib.pyplot as plt  # 绘图
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  # 词云
import datetime  # 日期

startTime_tag = datetime.datetime.strptime('2019-02-04', '%Y-%m-%d')  # 将2019.2.4号之前的数据汇总到2.4 统一标识为电影上映前影评数据

# 提前自定义pyecharts渲染图格式
style_map = Style(
    title_color="#fff",
    title_pos="center",
    width=1900,
    height=950,
    background_color='#404a59'
)
style_others = Style(
    title_pos='center',
    width=1900,
    height=950
)
style_size = Style(
    width=1900,
    height=950
)


# 读取csv文件数据
def read_csv(filename, titles):
    print("正在读取csv文件数据......")
    comments = pd.read_csv(filename, names=titles, encoding='utf_8_sig')  # 指定读取格式utf_8_sig
    return comments


# 数据城市名称与热力地图名称匹配（模糊匹配到热力图中的地址名称：例如 上海 = 上海市  舟山 = 舟山市）
def remove_None(areas, values):
    None_areas = []  # 储存无效区域
    i = 0  # 计数器
    while (i != len(areas)):
        # 取前两个字符作模糊查询
        if search_coordinates_by_keyword(areas[i][:2]) == {}:  # 匹配失败，删除这条数据
            None_areas.append(areas[i])
            areas.remove(areas[i])
            values.remove(values[i])
        else:
            # 将模糊查询结果替代原地名
            areas[i] = search_coordinates_by_keyword(areas[i][:2]).popitem()[0]
            i = i + 1  # 计数器加一
    if len(None_areas) == 0:
        print('区域名称已全部匹配完成！')
    else:
        print('无效区域：', None_areas)
    return areas, values


# 观众地域图
def draw_map(comments):
    print("正在处理观众地域图......")
    try:
        page = Page()  # 页面储存器
        attr = comments['cityName'].fillna("zero_token")  # 将不包含城市数据的数据置为空标志
        data = Counter(attr).most_common(300)  # 计数并选取数据最多的300个城市
        data.reverse()  # 反转数据，为了热力图有更好的显示效果（数据量大的城市在最上方）
        data.remove(data[data.index([(i, x) for i, x in (data) if i == 'zero_token'][0])])  # 删除没有城市名称的空标志数据

        geo = Geo("《流浪地球》全国观众地域分布点", "数据来源：猫眼电影 数据分析：16124278-王浩", **style_map.init_style)  # 初始一张热力图并设置外观
        # attr, value = geo.cast(data)
        attr, value = remove_None(geo.cast(data)[0], geo.cast(data)[1])  # 地图名称模糊匹配
        geo.add("", attr, value, visual_range=[0, 4000], maptype='china', visual_text_color="#fff", symbol_size=10,
                is_visualmap=True, is_legend_show=False,
                tooltip_formatter='{b}',
                label_emphasis_textsize=15,
                label_emphasis_pos='right')  # 加入数据并设置热力图风格参数-点图
        page.add(geo)  # 添加到渲染队列

        geo = Geo("《流浪地球》全国观众地域分布域", "数据来源：猫眼电影 数据分析：16124278-王浩", **style_map.init_style)  # 初始一张热力图并设置外观
        geo.add("", attr, value, type="heatmap", is_visualmap=True,
                visual_range=[0, 4000], visual_text_color='#fff',
                is_legend_show=False)  # 加入数据并设置热力图风格参数-区域图
        page.add(geo)  # 添加到渲染队列

        geo = Geo("《流浪地球》全国观众地域分布点域", "数据来源：猫眼电影 数据分析：16124278-王浩", **style_map.init_style)  # 初始一张热力图并设置外观
        geo.add("", attr, value, visual_range=[0, 4000], maptype='china', visual_text_color="#fff", symbol_size=10,
                is_visualmap=True, is_legend_show=False,
                tooltip_formatter='{b}',
                label_emphasis_textsize=15,
                label_emphasis_pos='right')
        geo.add("", attr, value, type="heatmap", is_visualmap=True,
                visual_range=[0, 4000], visual_text_color='#fff',
                is_legend_show=False)  # 加入数据并设置热力图风格参数-区域图
        page.add(geo)  # 添加到渲染队列

        page.render("./output/观众地域分布-地理坐标图.html")  # 渲染热力图
        print("全国观众地域分布已完成!!!")
    except Exception as e:  # 异常抛出
        print(e)


# 观众地域排行榜单（前20）
def draw_bar(comments):
    print("正在处理观众地域排行榜单......")
    data_top20 = Counter(comments['cityName']).most_common(20)  # 筛选出数据量前二十的城市
    bar = Bar('《流浪地球》观众地域排行榜单', '数据来源：猫眼电影 数据分析：16124278-王浩', **style_others.init_style)  # 初始化柱状图
    attr, value = bar.cast(data_top20)  # 传值
    bar.add('', attr, value, is_visualmap=True, visual_range=[0, 16000], visual_text_color='black', is_more_utils=True,
            is_label_show=True)  # 加入数据与其它参数
    bar.render('./output/观众地域排行榜单-柱状图.html')  # 渲染
    print("观众地域排行榜单已完成!!!")


# lambda表达式内置函数
# 将startTime_tag之前的数据汇总到startTime_tag
def judgeTime(time, startTime_tag):
    if time < startTime_tag:
        return startTime_tag
    else:
        return time


# 观众评论数量与日期的关系
def draw_DateBar(comments):
    print("正在处理观众评论数量与日期的关系......")
    time = pd.to_datetime(comments['startTime'])  # 获取评论时间并转换为标准日期格式
    time = time.apply(lambda x: judgeTime(x, startTime_tag))  # 将2019.2.4号之前的数据汇总到2.4 统一标识为电影上映前影评数据
    timeData = []
    for t in time:
        if pd.isnull(t) == False:  # 获取评论日期（删除具体时间）并记录
            t = str(t)  # 转换为字符串以便分割
            date = t.split(' ')[0]
            timeData.append(date)

    data = Counter(timeData).most_common()  # 记录相应日期对应的评论数
    data = sorted(data, key=lambda data: data[0])  # 使用lambda表达式对数据按日期进行排序

    bar = Bar('《流浪地球》观众评论数量与日期的关系', '数据来源：猫眼电影 数据分析：16124278-王浩', **style_others.init_style)  # 初始化柱状图
    attr, value = bar.cast(data)  # 传值
    bar.add('', attr, value, is_visualmap=True, visual_range=[0, 43000], visual_text_color='black', is_more_utils=True,
            is_label_show=True)  # 加入数据和其它参数
    bar.render('./output/观众评论日期-柱状图.html')  # 渲染
    print("观众评论数量与日期的关系已完成!!!")


# 观众情感曲线
def draw_sentiment_pic(comments):
    print("正在处理观众情感曲线......")
    score = comments['score'].dropna()  # 获取观众评分
    data = Counter(score).most_common()  # 记录相应评分对应的的评论数
    data = sorted(data, key=lambda data: data[0])  # 使用lambda表达式对数据按评分进行排序
    line = Line('《流浪地球》观众情感曲线', '数据来源：猫眼电影 数据分析：16124278-王浩', **style_others.init_style)  # 初始化
    attr, value = line.cast(data)  # 传值

    for i, v in enumerate(attr):  # 将分数修改为整数便于渲染图上的展示
        attr[i] = v * 2

    line.add("", attr, value, is_smooth=True, is_more_utils=True, yaxis_max=380000, xaxis_max=10)  # 加入数据和其它参数
    line.render("./output/观众情感分析-曲线图.html")  # 渲染
    print("观众情感曲线已完成!!!")


# 观众评论数量与时间的关系图
def draw_TimeBar(comments):
    print("正在处理观众评论数量与时间的关系......")
    time = comments['startTime'].dropna()  # 获取评论时间
    timeData = []
    for t in time:
        if pd.isnull(t) == False:  # 获取评论时间（当天小时）并记录
            time = t.split(' ')[1]
            hour = time.split(':')[0]
            timeData.append(int(hour))  # 转化为整数便于排序

    data = Counter(timeData).most_common()  # 记录相应时间对应的的评论数
    data = sorted(data, key=lambda data: data[0])  # 使用lambda表达式对数据按时间进行排序

    bar = Bar('《流浪地球》观众评论数量与时间的关系', '数据来源：猫眼电影 数据分析：16124278-王浩', **style_others.init_style)  # 初始化柱状图
    attr, value = bar.cast(data)  # 传值
    bar.add('', attr, value, is_visualmap=True, visual_range=[0, 40000], visual_text_color='black', is_more_utils=True,
            is_label_show=True)  # 加入数据和其它参数
    bar.render('./output/观众评论时间-柱状图.html')  # 渲染
    print("观众评论数量与时间的关系已完成!!!")


# 观众评论走势与时间的关系
def draw_score(comments):
    print("正在处理观众评论走势与时间的关系......")
    page = Page()  # 页面储存器
    score, date, value, score_list = [], [], [], []
    result = {}  # 存储评分结果

    d = comments[['score', 'startTime']].dropna()  # 获取评论时间
    d['startTime'] = d['startTime'].apply(lambda x: pd.to_datetime(x.split(' ')[0]))  # 获取评论日期（删除具体时间）并记录
    d['startTime'] = d['startTime'].apply(lambda x: judgeTime(x, startTime_tag))  # 将2019.2.4号之前的数据汇总到2.4 统一标识为电影上映前影评数据

    for indexs in d.index:  # 一种遍历df行的方法（下面还有第二种，iterrows）
        score_list.append(tuple(d.loc[indexs].values[:]))  # 评分与日期连接  转换为tuple然后统计相同元素个数
    print("有效评分总数量为：", len(score_list), " 条")
    for i in set(list(score_list)):
        result[i] = score_list.count(i)  # dict类型，统计相同日期相同评分对应数

    info = []
    for key in result:
        score = key[0]  # 取分数
        date = key[1]  # 日期
        value = result[key]  # 数量
        info.append([score, date, value])
    info_new = pd.DataFrame(info)  # 将字典转换成为数据框
    info_new.columns = ['score', 'date', 'votes']
    info_new.sort_values('date', inplace=True)  # 按日期升序排列df，便于找最早date和最晚data，方便后面插值

    # 以下代码用于插入空缺的数据，每个日期的评分类型应该有10种，依次遍历判断是否存在，若不存在则往新的df中插入新数值
    mark = 0
    creat_df = pd.DataFrame(columns=['score', 'date', 'votes'])  # 创建空的dataframe
    for i in list(info_new['date']):
        location = info_new[(info_new.date == i) & (info_new.score == 5.0)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [5.0, i, 0]
            mark += 1
        location = info_new[(info_new.date == i) & (info_new.score == 4.5)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [4.5, i, 0]
            mark += 1
        location = info_new[(info_new.date == i) & (info_new.score == 4.0)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [4.0, i, 0]
            mark += 1
        location = info_new[(info_new.date == i) & (info_new.score == 3.5)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [3.5, i, 0]
            mark += 1
        location = info_new[(info_new.date == i) & (info_new.score == 3.0)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [3.0, i, 0]
            mark += 1
        location = info_new[(info_new.date == i) & (info_new.score == 2.5)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [2.5, i, 0]
            mark += 1
        location = info_new[(info_new.date == i) & (info_new.score == 2.0)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [2.0, i, 0]
            mark += 1
        location = info_new[(info_new.date == i) & (info_new.score == 1.5)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [1.5, i, 0]
            mark += 1
        location = info_new[(info_new.date == i) & (info_new.score == 1.0)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [1.0, i, 0]
            mark += 1
        location = info_new[(info_new.date == i) & (info_new.score == 0.5)].index.tolist()
        if location == []:
            creat_df.loc[mark] = [0.5, i, 0]
            mark += 1

    info_new = info_new.append(creat_df.drop_duplicates(), ignore_index=True)
    score_list = []  # 重置score_list
    info_new = info_new[~(info_new['score'] == 0.0)]  # 剔除无评分的数据
    info_new.sort_values('date', inplace=True)  # 按日期升序排列df，便于找最早date和最晚data，方便后面插值
    for index, row in info_new.iterrows():  # 第二种遍历df的方法
        score_list.append([row['date'], row['votes'], row['score']])

    tr = ThemeRiver('《流浪地球》观众评论走势与时间的关系-河流图', '数据来源：猫眼电影 数据分析：16124278-王浩', **style_size.init_style)  # 河流图初始化
    tr.add([5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5], score_list, is_label_show=True,
           is_more_utils=True)  # 设置参数
    page.add_chart(tr)  # 加入渲染队列

    attr, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10 = [], [], [], [], [], [], [], [], [], [], []
    attr = list(sorted(set(info_new['date'])))
    bar = Bar('《流浪地球》观众评论走势与时间的关系-横向柱状图', '数据来源：猫眼电影 数据分析：16124278-王浩', **style_others.init_style)  # 初始化图表
    for i in attr:
        v1.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 5.0)]['votes']))
        v2.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 4.5)]['votes']))
        v3.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 4.0)]['votes']))
        v4.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 3.5)]['votes']))
        v5.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 3.0)]['votes']))
        v6.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 2.5)]['votes']))
        v7.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 2.0)]['votes']))
        v8.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 1.5)]['votes']))
        v9.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 1.0)]['votes']))
        v10.append(int(info_new[(info_new['date'] == i) & (info_new['score'] == 0.5)]['votes']))
    bar.add(5.0, attr, v1, is_stack=True)
    bar.add(4.5, attr, v2, is_stack=True)
    bar.add(4.0, attr, v3, is_stack=True)
    bar.add(3.5, attr, v4, is_stack=True)
    bar.add(3.0, attr, v5, is_stack=True)
    bar.add(2.5, attr, v6, is_stack=True)
    bar.add(2.0, attr, v7, is_stack=True)
    bar.add(1.5, attr, v8, is_stack=True)
    bar.add(1.0, attr, v9, is_stack=True)
    bar.add(0.5, attr, v10, is_stack=True, is_convert=True, is_more_utils=True, xaxis_max=45000)
    page.add_chart(bar)

    line = Line('《流浪地球》观众评论走势与时间的关系', '数据来源：猫眼电影 数据分析：16124278-王浩', **style_others.init_style)  # 初始化图表
    line.add(5.0, attr, v1, is_stack=True, mark_line=["average"])
    line.add(4.5, attr, v2, is_stack=True, mark_line=["average"])
    line.add(4.0, attr, v3, is_stack=True, mark_line=["average"])
    line.add(3.5, attr, v4, is_stack=True, mark_line=["average"])
    line.add(3.0, attr, v5, is_stack=True, mark_line=["average"])
    line.add(2.5, attr, v6, is_stack=True, mark_line=["average"])
    line.add(2.0, attr, v7, is_stack=True, mark_line=["average"])
    line.add(1.5, attr, v8, is_stack=True, mark_line=["average"])
    line.add(1.0, attr, v9, is_stack=True, mark_line=["average"])
    line.add(0.5, attr, v10, is_stack=True, is_convert=False, mark_line=["average"], is_more_utils=True,
             yaxis_max=45000)
    page.add_chart(line)

    page.render("./output/观众评论与日投票-走势图.html")  # 渲染
    print("观众评论走势与时间的关系已完成!!!")


# 绘制词云
def draw_wordCloud(comments):
    print("数据量较大，正在分词中，请耐心等待......")
    data = comments['content']  # 获取评论内容

    comment_data = []
    for item in data:
        if pd.isnull(item) == False:
            comment_data.append(item)

    comment_after_split = jieba.cut(str(comment_data), cut_all=False)  # jieba分词
    words = ' '.join(comment_after_split)  # 连接分词
    backgroud_Image = plt.imread('./input/worldcloud_sample.jpg')  # 设置词云背景图
    # 自定义停用词
    stopwords = STOPWORDS.copy()
    with open('./input/stopwords.txt', 'r', encoding='utf-8') as f:  # 打开文件读取停用词
        for i in f.readlines():
            stopwords.add(i.strip('\n'))
        f.close()

    # 字体路径
    wc = WordCloud(width=1024, height=768, background_color='white',
                   mask=backgroud_Image, font_path="C:\simhei.ttf",
                   stopwords=stopwords, max_font_size=500,
                   random_state=80)  # 设置词云参数
    wc.generate_from_text(words)  # 传入关键词
    img_colors = ImageColorGenerator(backgroud_Image)  # 取背景图色彩
    wc.recolor(color_func=img_colors)  # 给词云上色美化

    # plt.figure(figsize=(10, 8))
    plt.imshow(wc)  # 设置参数
    plt.axis('off')  # 关闭坐标轴显示
    plt.savefig('./output/WordCloud.png', dpi=300)  # 保存高清打印图片
    plt.show()  # 展示


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    filename = "./input/Comments.csv"
    titles = ['nickName', 'cityName', 'content', 'score', 'startTime']
    comments = read_csv(filename, titles)
    draw_map(comments)
    draw_bar(comments)
    draw_DateBar(comments)
    draw_TimeBar(comments)
    draw_score(comments)
    draw_sentiment_pic(comments)
    draw_wordCloud(comments)
    end_time = datetime.datetime.now()
    print("全部完成!!!")
    print('程序运行用时(秒):', (end_time - start_time).seconds)
