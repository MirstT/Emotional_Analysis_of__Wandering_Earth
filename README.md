# 基于TF的CNN 与LSTM/GRU 的《流浪地球》影评数据分析
## Emotional-Analysis-of-The-Wandering-Earth
为了通过影评数据反应电影《流浪地球》的口碑以及其造成热度，并核实网络水军恶意对其刷差评现象是否存在，本文利用猫眼PC端接口，通过控制时间参数，动态爬取了，《流浪地球》在2019年3月5日之前的52万余条影评数据。对这些数据进行预处理操作，特征处理，可视化分析后，引入了卷积神经网络与循环神经网络对影评内容进行了更深一步的情感分析，对今后的的数据分析预测学习有一定的指导意义。

In this paper, in order to reflect the popularity of the movie "Wandering Earth" and its heat, and to verify whether the phenomenon of malicious brushing of the film by the network Navy exists, this paper uses the cat's eye PC interface to dynamically crawl over 520,000 reviews of "Wandering Earth" before March 5, 2019 by controlling the time parameters. After pretreatment, feature processing and visual analysis of these data, convolution neural network and cyclic neural network are introduced to conduct a deeper emotional analysis of the content of film review, which has certain guiding significance for future data analysis and prediction learning. 

## Get_Data.py 1.利用爬虫获取影评数据，输出至input文件夹下

## Analyze_Data.py 2.对获取的影评数据进行可视化分析，输出至output文件夹下（需要用到echarts中国地图包）

## Comments_Group.py 3.影评数据预处理，输出至comments文件夹下，以便后续情感分析数据导入
