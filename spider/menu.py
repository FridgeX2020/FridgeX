#coding=utf-8"
from bs4 import BeautifulSoup      #网页解析，获取数据
import re       #正则表达式
import matplotlib
from io import BytesIO
import urllib  #制定URL，获取网页数据
import xlwt                         #excel操作
import sqlite3                      #sqlite数据库操作
import gzip
import requests
import difflib
import copy
from selenium import webdriver
import time
import json


def ask_url(baseurl):
    try:
        req = requests.get(baseurl)
        req.encoding = 'utf-8'
        # print("This is soup2\n",soup2.select("body>p"),"\n")
        return req.text
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

def pa_menu(menu_url):
    html_text = ask_url(menu_url)
    html_soup = BeautifulSoup(html_text,"html.parser")
    all_data = []
    find_link = re.compile(r'<a href="(.*)" target="_blank">\n<div class="imgw"><img alt="(.*)')
    # find_name = re.compile(r'<div class="imgw"><img alt="(.*)" class="cell-img" src="(.*)"/></div>')
    for i in html_soup.select("div>ul>li>a"):
        for m in re.findall(find_link,str(i)):
            all_data.append(m[0])
    return all_data

def one_menu(link):
    html_data = ask_url(link)
    data_soup = BeautifulSoup(html_data,"html.parser")
    data = []
    data.append(data_soup.select("h1")[0].get_text().strip())
    find_img_link = re.compile(r'<img class="headerimg" src="(.*)"/>')
    try:
        img = str(data_soup.select("body>div>div>img")[0])
        img = re.findall(find_img_link,img)[0]
        # print(img)
    except:
        img = 'none'
    data.append(img)
    tempt_nutrition = []
    find_nutrition = re.compile(r'<div class="yy_left_item">\n<strong>(.*)</strong><div class="jdw"><div class="jd" style="width:(.*);"></div></div>\n</div>')

    try:
        for i in data_soup.select("body>div>div>div>div>div>div.yy_left_item"):
            tempt_nutrition.append(" ".join(re.findall(find_nutrition,str(i))[0]))
            # tempt_nutrition.append(i.get_text().strip())
    except:
        pass
    data.append(tempt_nutrition)
    tempt_discription = []

    try:
        for i in data_soup.select("body>div>div>div>div>div.cpargsw>div"):
            tempt_discription.append(i.get_text().strip())
    except:
        pass
    data.append(tempt_discription)
    tempt_ingredient_main = []

    try:
        for i in data_soup.select("body>div>div>div>div>div.c_mtr_t~.c_mtr_ul>div.c_mtr_li"):
            tempt_ingredient_main.append(i.get_text().strip())
    except:
        pass
    data.append(tempt_ingredient_main)
    tempt_ingredient_sub = []

    try:
        for i in data_soup.select("body>div>div>div>div>div.c_mtr_t~.c_mtr_ul>div>div"):
            tempt_ingredient_sub.append(i.get_text().strip())
    except:
        pass
    data.append(tempt_ingredient_sub)
    tempt_step = []

    try:
        for i in data_soup.select("body>div>div>div>div>p"):
            tempt_step.append(i.get_text().strip())
    except:
        pass
    data.append(tempt_step)
    # print(data)

    return data


if __name__=="__main__":
    menu_url = ["https://m.meishij.net/fenlei/yingjishishu/","https://m.meishij.net/fenlei/yingjishishu/p2/","https://m.meishij.net/fenlei/kuaishoucai/","https://m.meishij.net/fenlei/sushi/","https://m.meishij.net/fenlei/roushi/","https://m.meishij.net/fenlei/tang/","https://m.meishij.net/fenlei/jiachangcai/"]
    link = []
    for i in menu_url:
        link.extend(pa_menu(i))#[[link,name,jpg_url],[...]...] all str
        time.sleep(1)

    # print(link)
    all_caipu = []
    count = 1
    for i in link:
        # example_url = 'https://m.meishij.net/html5/zuofa/qingchaosijishishu.html'
        all_caipu.append(one_menu(i))
        time.sleep(0.05)
        print(count)
        count+=1
    # example = ['清炒四季时蔬','https://st-cn.meishij.net/r/194/87/271944/s271944_145558547217743.jpg', ['卡路里 9.7%', '碳水化合物 11.9%', '脂肪 9.7%', '蛋白质 11.2%', '钙 18.8%', '铁 100%'], ['炒', '家常味', '<5分钟', '较低热量','新手尝试'], ['紫甘蓝100克', '藕片50克', '芦笋50克', '胡萝卜30克', '木耳(水发)30g'], ['食盐适量', '食用油适量', '葱花5克'], ['紫甘蓝切大块，莲藕切片，芦笋切段，胡萝卜切片，木耳洗干净掰一口大小的块', '炒锅烧热，加入食用油和葱花炝锅，然后下入胡萝卜和木耳，翻炒一下加入莲藕和芦笋，最后加入紫甘蓝，放盐搅拌均匀即可。紫甘蓝切大块，莲藕切片，芦笋切段，胡萝卜切片，木耳洗干净掰一口大小的块', '木耳：禁忌人群：有出血性疾病、腹泻者、孕妇慎食适宜人群：一般人群均可食用。尤适宜心脑血管疾病、结石症患者食用，特别适合缺铁的人士、矿工、冶金工人、纺织工、理发师食用']]
    count = 1
    json_menu = []

    for example in all_caipu:
        json_menu.append({})
        json_menu[-1]["菜名"] = example[0]
        # f.write("菜名:"+example[0]+"\n")
        if example[1]:
            json_menu[-1]["img_link"] = example[1]
            # f.write('img_link:'+example[1]+"\n")
        else:
            json_menu[-1]["img_link"] = None
            # f.write('img_link:无\n')
        if example[2]:
            json_menu[-1]["卡路里"] = example[2][0] if example[2][0] else None
            json_menu[-1]["碳水化合物"] = example[2][1] if example[2][1] else None
            json_menu[-1]["脂肪"] = example[2][2] if example[2][2] else None
            json_menu[-1]["蛋白质"] = example[2][3] if example[2][3] else None
            json_menu[-1]["钙"] = example[2][4] if example[2][4] else None
            json_menu[-1]["铁"] = example[2][5] if example[2][5] else None
        else:
            json_menu[-1]["卡路里"] = None
            json_menu[-1]["碳水化合物"] = None
            json_menu[-1]["脂肪"] = None
            json_menu[-1]["蛋白质"] = None
            json_menu[-1]["钙"] = None
            json_menu[-1]["铁"] = None
                # f.write("中国居民每日推荐摄入营养所得占比数据:"+",".join(example[2])+"\n")
        # else:
        #     f.write("中国居民每日推荐摄入营养所得占比数据:无\n")
        json_menu[-1]["烹饪方式"] = example[3][0] if example[3][0] else None
        json_menu[-1]["菜品风味"] = example[3][1] if example[3][1] else None
        json_menu[-1]["烹饪时间"] = example[3][2] if example[3][2] else None
        json_menu[-1]["热量"] = example[3][3] if example[3][3] else None
        json_menu[-1]["烹饪难度"] = example[3][4] if example[3][4] else None
        # if example[3]:
        #     f.write("烹饪方式:"+example[3][0]+"\n菜品风味:"+example[3][1]+"\n烹饪时间:"+example[3][2]+"\n热量:"+example[3][3]+"\n烹饪难度:"+example[3][4]+"\n")
        # else:
        #     f.write("\n\n\n\n\n")
        json_menu[-1]["主料"] = example[4] if example[4] else None
        # if example[4]:
        #     f.write("主料:"+",".join(example[4])+"\n")
        # else:
        #     f.write("主料:无\n")
        json_menu[-1]["辅料"] = example[5] if example[5] else None
        # if example[5]:
        #     f.write("辅料:"+",".join(example[5])+"\n")
        # else:
        #     f.write("辅料:无\n")
        json_menu[-1]["步骤"] = example[6][:-1] if example[6] else None
        json_menu[-1]["另"] = example[6][-1] if example[6][-1] else None
        # f.write("步骤:"+"\n".join(example[6][:-1])+"\n")
        # f.write("另:"+example[6][-1]+"\n")
        # f.write("\n")
        print("it is writing ",count)
        count+=1
    with open("menu2.json", "w", encoding='utf-8') as f:
        f.write("{\n\"data\":[")
        for i in json_menu:
            json.dump(i, f,ensure_ascii=False)
            f.write(",\n")
        f.write("\n]\n}")
