# 16124278 王浩 流浪地球 comments_loader
# coding: utf-8

import sys
from collections import Counter
from imp import reload

import numpy as np
import tensorflow.contrib.keras as kr

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False



def open_file(filename, mode='r'):
    """
    常用文件操作，可在python2和python3间切换.
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)


def read_file(filename):
    """读取文件数据"""
    contents, labels = [], []
    with open_file(filename) as f:
        for line in f:
            try:
                label, content = line.strip().split('\t') #分割
                if content:
                    contents.append(list(content))
                    labels.append(label)
            except:
                pass
    return contents, labels #返回标签和内容


def build_vocab(train_dir, vocab_dir, vocab_size=5000):
    """根据训练集构建词汇表，存储"""
    data_train, _ = read_file(train_dir)

    all_data = []
    for content in data_train:
        all_data.extend(content)

    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)
    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')


def read_vocab(vocab_dir):
    """读取词汇表"""
    words = open_file(vocab_dir).read().strip().split('\n')
    word_to_id = dict(zip(words, range(len(words)))) #为每一个词建立一个id by 位置
    return words, word_to_id #返回


def read_category():
    """读取分类目录，固定"""
    categories = ["好评", "中评", "差评"]
    cat_to_id = dict(zip(categories, range(len(categories)))) #建立一个类别和id的字典
    return categories, cat_to_id #返回


def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)

#数据预处理
# max_length=600
def process_file(filename, word_to_id, cat_to_id, max_length=100):
    """将文件转换为id表示"""
    contents, labels = read_file(filename) #文件读取


    data_id, label_id = [], []
    for i in range(len(contents)): #将影评和标签全部id化
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id]) #把影评中的每个字按词汇目录转换为id
        label_id.append(cat_to_id[labels[i]])#把标签按分类目录转换为id

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length) #取每句影评后max_length个字，取不到的地方则置为0
    y_pad = kr.utils.to_categorical(label_id, num_classes=len(cat_to_id))  # 将标签转换为one-hot表示

    return x_pad, y_pad


def batch_iter(x, y, batch_size=64):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]
