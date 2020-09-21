import os,glob,sys
import json
import numpy as np

user = 'username'
srcdir = [
    'path to hand history1',
    'path to hand history2'
]

def make_pathlist(list_):
    li = []
    for path in list_:
        li += glob.glob(os.path.join(path, '**', '*Varied.txt'), recursive=True)
    return sorted(li)

def getNearestValue(list, num):
    """
    https://qiita.com/icchi_h/items/fc0df3abb02b51f81657
    概要: リストからある値に最も近い値を返却する関数
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """
    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(list) - num).argmin()
    return list[idx]

user_prize = user + ' wins $'
user_win = user + ' wins the tournament'
user_lose = user + ' finished the tournament'
pathlist = make_pathlist(srcdir)
game = [0]*6
debug = [0]*6
debug_diff = 0
cost = 0
prize = 0
buyin_list = [1, 2, 5, 12, 25, 60]
completed = 0

for path in pathlist:
    with open(path, 'r', encoding='utf-8')as f:
        txt = f.read().split('\n')
    buyin = 100
    for line in txt[2:6]:
        for word in line.split(' ')[::-1]:
            if '$' in word:
                buyin = min(buyin, float(word.replace('$','')))
                break
    buyin = getNearestValue(buyin_list, buyin/0.9)
    index = buyin_list.index(buyin)
    game[index] += 1
    cost += buyin
    for line in txt:
        if user_prize in line:
            prize += float(line.split(' ')[2].replace('$', ''))
        elif user_win in line:
            if buyin!=len(buyin_list):
                cost -= buyin_list[index+1]
            else:
                completed += 1
        elif user_lose in line:
            pass
        else:
            pass

    #print(game, cost, buyin)
#print(game, cost, prize, completed)
print('net prize :', round(prize - cost, 3))
