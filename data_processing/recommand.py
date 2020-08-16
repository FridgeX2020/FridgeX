# -*- coding: utf-8 -*-  
# [
# 菜名,
# img_link,
# [卡路里(空格)百分比，碳水化合物，脂肪，蛋白质，钙，铁],#中国居民每日推荐摄入营养所得占比数据
# [烹饪方式,味道,时间,热量,难度],
# [主材料多种，长度不定],
# [副材料多种，长度不定],
# [制作步骤，多步,（最后一个str为烹饪技巧或注意事项，可能含禁忌人群，适宜人群，没有则为‘无’）]
# ]
import json 
import re
import numpy as np

person_data = [150,170,150,80,70,60] # 卡路里(空格)百分比，碳水化合物，脂肪，蛋白质，钙，铁
weight = [0]*6
for i in range(6):
    weight[i] = 100 - person_data[i]

with open('menu_without_invalid.json') as f:
    menu = f.read()
menu = json.loads(menu)
menu = menu['data']
# print(menu[0])

delete = 0
total = []
for item in menu:
    tmp = []
    for key in item:
        if item[key] == None:
            delete = 1
        tmp.append(item[key])
    if delete==0:
        total.append(tmp)
    delete = 0

recommand_order0 = []
recommand_order1 = []
recommand_order2 = []
recommand_order3 = []
recommand_order4 = []
recommand_order5 = []

percentage = []
for menu in total:
    menu = menu[2:8]
    item = []
    for perc in menu:
        perc = perc.split(' ')[1][:-1]
        # print(perc)
        item.append(eval(perc))
    percentage.append(item)
# print(percentage)
min_item = []
max_item = []

for j in range(6):
    max_item.append(percentage[0][j])
    min_item.append(percentage[0][j])
    for i in range(len(percentage)): 
        if (percentage[i][j] < min_item[-1]): 
            min_item[j] = percentage[i][j]
        if (percentage[i][j] > max_item[-1]): 
            max_item[j] = percentage[i][j]
# print(max_item, min_item)

normal_list = percentage
for j in range(6):
    for i in range(len(percentage)):
        percentage[i][j] = (percentage[i][j] - min_item[j]) / (max_item[j] - min_item[j] + 0.001)

weighted_recommand = []
for item in percentage:
    one_weighted = 0
    for i in range(6):
        one_weighted += (item[i]) * weight[i]
    weighted_recommand.append(one_weighted)
# print(weighted_recommand)
index = np.argsort(np.array(weighted_recommand))
# print(index)
# print(total[index[-1]][0])
final = []
for i in range(1,7):
    # print(total[index[-i]][0])
    final.append(index[-i])
# print(final)
dic = {}
dic["0"] = final[0]
dic["1"] = final[1]
dic["2"] = final[2]
dic["3"] = final[3]
dic["4"] = final[4]
dic["5"] = final[5]

final_str = str(dic).replace("'", '"')
print(final_str)
with open('output.json', 'w') as f:
    f.write(final_str)

# recommand_orders = []
# for i in range(6):
#     recommand = []
#     for item in percentage:
#         recommand.append(item[i])
#     recommand_order = np.array(recommand)
#     recommand_order = (np.argsort(recommand_order))
#     recommand_orders.append(recommand_order)
# recommand_order0 = recommand_orders[0]
# recommand_order1 = recommand_orders[1]
# recommand_order2 = recommand_orders[2]
# recommand_order3 = recommand_orders[3]
# recommand_order4 = recommand_orders[4]
# recommand_order5 = recommand_orders[5]
# # print(recommand_order1)
# print(total[recommand_order1[-1]][0])