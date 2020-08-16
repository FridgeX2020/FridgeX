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

def diff_str(little,big):
    return difflib.SequenceMatcher(None,little,big).quick_ratio()


def return_third(data):
    return data[2]

def liebiao():
    baseurl = "https://myingyang.911cha.com/list_4.html"
    cha_browser = webdriver.Chrome()
    cha_browser.get(baseurl)
    vege = []
    for i in cha_browser.find_elements_by_tag_name('li'):
        vege.append(i.text)
    vege = vege[:-6]
    return vege


def pa(fruit):
    loul = []
    # fruit = ['香蕉']#,'苹果','枇杷','草莓','柠檬','梨','石榴','葡萄','橘子','芒果','西瓜','柿子',
             #'桂圆','荸荠','桑葚','李子','菠萝','菠萝蜜','杨梅','银杏','无花果',
             #'乌梅','甘蔗','人参果','樱桃','黄桃','鳄梨','海棠果',
             #'甜瓜','山楂','荔枝','金桔','柑桔','椰子','杨桃','木瓜']#,'桃子''红枣','柚子','哈密瓜','火龙果','橙子',
    all_data = []
    baseurl = "https://myingyang.911cha.com/"
    cha_browser = webdriver.Chrome()
    cha_browser.get(baseurl)
    for m in range(len(fruit)):
        try:

            cha_browser.find_element_by_id('q').send_keys(fruit[m])
            btn = cha_browser.find_element_by_class_name('but')
            btn.click()
            time.sleep(2)
            tempt = []
            for i in cha_browser.find_elements_by_css_selector('body>div>ul>li>a'):
                tempt.append(i.text)
            for i in range(len(tempt)):
                # print(diff_str(fruit[m], tempt[i][0:2]))
                # print(i,"\n",tempt[i],"\n",diff_str(fruit[m],tempt[i][0:2]))
                tempt[i] = [i,tempt[i],float(diff_str(fruit[m],tempt[i][0:2]))]
            # print(tempt)
            tempt = tempt[:]
            tempt.sort(key=return_third,reverse=True)
            key = tempt[0][0]
            name = tempt[0][1]
            # print("??",key)
            go = cha_browser.find_elements_by_css_selector('body>div>ul>li>a')[key]
            go.click()
            left = [i.text for i in cha_browser.find_elements_by_css_selector('body>div>div>table>tbody>tr>th')]
            right = [i.text.split(" ")[0] for i in cha_browser.find_elements_by_css_selector('body>div>div>table>tbody>tr>td')]#.replace("千卡",'kilocalorie').replace("卡","calories").replace("毫克","mg").replace("微克","ug").replace("克","g")
            nutrition = [[left[a],right[a]] for a in range(len(left))]
            # print(nutrition)
            all_data.append([fruit[m],nutrition])       #[[str,[[str,str],[str,str]],...],...]
            # print("this is fruit",fruit[m],"\nthis is ntn",nutrition)
        except:
            loul.append(fruit[m])
            continue
    print(loul)
    return all_data     #list套list套两个str

def init_db(dbpath):#retinol, na, se
    sql = '''
        create table vegetable              
            (id int primary key not null,
            heat text,
            thiamine text,
            calcium text,
            protein text,
            riboflavin text,
            magnesium text,
            fat text,
            niacin text,
            fe text,
            carbohydrate text,
            vitamin_C text,
            mn text,
            fiber text,
            vitamin_E text,
            zinc text,
            vitamin_A text,
            cholesterol text,
            cu text,
            carotene text,
            k text,
            p text,
            retinol text,
            na text,
            se text
            );
    '''
    connect_data = sqlite3.connect(dbpath)
    db_cursor = connect_data.cursor()
    db_cursor.execute(sql)
    connect_data.commit()
    connect_data.close()

if __name__=="__main__":
    vege_name = ['白萝卜[莱菔]', '变萝卜[红皮萝卜]', '红旦旦萝卜', '红萝卜', '红心萝卜', '花叶萝卜', '青萝卜', '水萝卜[脆萝卜]', '小水萝卜[算盘子，红皮萝卜]', '心里美萝卜', '胡萝卜(红)[金笋，丁香萝\
卜]', '胡萝卜(黄)', '胡萝卜(脱水)', '芥菜头[大头菜，水芥]', '苤蓝[玉蔓菁，球茎甘蓝]', '甜菜根[甜菜头，糖萝卜]', '扁豆[月亮菜]', '刀豆', '豆角', '豆角(白)', '荷兰豆', '龙豆', '龙牙豆[\
玉豆]', '毛豆[青豆，菜用大豆]', '四季豆[菜豆]', '豌豆(带荚)[回回豆]', '豌豆尖', '油豆角[多花菜豆]', '垅船豆', '芸豆', '豇豆(长)', '发芽豆', '黄豆芽', '绿豆芽', '豌豆苗', '茄子(均值)'\
, '茄子(绿皮)', '茄子(圆)', '茄子(紫皮，长)', '番茄[西红柿]', '番茄(整个，罐头)', '奶柿子[西红柿]', '辣椒(红，尖，干)', '辣椒(红，小)', '辣椒(青，尖)', '甜椒[灯笼椒，柿子椒]', '甜椒(\
脱水)', '葫子', '秋葵[黄秋葵，羊角豆]', '白瓜', '菜瓜[生瓜，白瓜]', '冬瓜', '方瓜', '佛手瓜[棒瓜，菜肴梨]', '葫芦[长瓜，蒲瓜，瓠瓜]', '葫芦条(干)', '黄瓜[胡瓜]', '节瓜[毛瓜]', '金瓜'\
, '金丝瓜[裸瓣瓜]', '苦瓜[凉瓜，癞瓜]', '南瓜[倭瓜，番瓜]', '南瓜粉', '蛇瓜[蛇豆，大豆角]', '丝瓜', '笋瓜[生瓜]', '西葫芦', '面西胡瓜', '小西胡瓜', '大蒜[蒜头]', '大蒜(脱水)', '大蒜(\
紫皮)', '青蒜', '蒜黄', '蒜苗', '蒜苔', '大葱', '大葱(红皮)', '分葱[四季葱，菜葱]', '细香葱[香葱，四季葱]', '小葱', '洋葱[葱头]', '洋葱(白皮，脱水)', '洋葱(紫皮，脱水)', '韭菜', '韭\
黄[韭芽]', '韭苔', '薤[皎头]', '薤白[小根蒜，山蒜，团蒜]', '大白菜(均值)', '大白菜(白梗)[黄芽白]', '大白菜(青白口)', '大白菜(小白口)', '白菜(脱水)', '酸白菜[酸菜]', '小白菜', '白菜薹\
[菜薹，菜心]', '红菜薹[紫菜薹]', '瓢儿白[瓢儿菜]', '乌菜[乌塌菜，塌棵菜]', '油菜', '油菜(黑)', '油菜(脱水)', '油菜(小)', '油菜薹[菜薹]', '甘蓝[圆白菜，卷心菜]', '菜花[花椰菜]', '菜花\
(脱水)[脱水花椰菜]', '西兰花[绿菜花]', '芥菜[雪里红，雪菜]', '芥菜(大叶)[盖菜]', '芥菜(茎用)[青头菜]', '芥菜(小叶)[小芥菜]', '芥蓝[甘蓝菜，盖蓝菜]', '菠菜[赤根菜]', '菠菜(脱水)', '冬\
寒菜[冬苋菜，冬葵]', '观达菜[根达菜，牛皮菜]', '胡萝卜缨(红)', '苦菜[节节花，拒马菜]', '萝卜缨(白)', '萝卜缨(青)', '萝卜缨(小萝卜)', '落葵[木耳菜，软浆菜]', '芹菜(白茎)[旱芹，药芹]',\
 '芹菜茎', '芹菜叶', '生菜(牛俐)[油麦菜]', '生菜(叶用莴苣)', '甜菜叶', '香菜[芫荽]', '香菜(脱水)', '苋菜(绿)', '苋菜(紫)[红苋]', '茼蒿[蓬蒿菜，艾菜]', '茴香[小茴香]', '荠菜[蓟菜，菱\
角菜]', '莴笋[莴苣]', '莴笋叶[莴苣叶]', '蕹菜[空心菜，藤藤菜]', '竹笋', '白笋(干)', '鞭笋[马鞭笋]', '春笋', '冬笋', '黑笋(干)', '毛笋[毛竹笋]', '玉兰片', '百合', '百合(干)', '百合(脱\
水)', '金针菜[黄花菜]', '菊苣', '芦笋[石刁柏，龙须菜]', '慈菇[乌芋，白地果]', '豆瓣菜[西洋菜，水田芥]', '菱角(老)[龙角]', '藕[莲藕]', '蒲菜[香蒲，甘蒲，野茭白]', '水芹菜', '茭白[茭笋\
，茭粑]', '荸荠[马蹄，地栗]', '莼菜(瓶装)[花案菜]', '大薯[参薯]', '豆薯[凉薯，地瓜，沙葛]', '葛[葛署，粉葛]', '山药[薯蓣，大薯]', '山药(干)', '芋头[芋艿，毛芋]', '槟榔芋', '姜[黄姜]'\
, '姜(干)', '姜(子姜)[嫩姜]', '洋姜[菊芋，鬼子姜]', '艾蒿', '白花菜', '白花桔梗', '白沙蒿[沙蒿]', '白沙蒿籽[沙蒿籽]', '白薯叶[甘薯叶]', '百里香', '败酱[胭脂麻]', '扁蓄菜[竹节草]', '\
朝鲜蓟', '刺儿菜[小蓟，蓟蓟菜]', '刺楸', '达乌里胡枝子[牛枝子，豆豆苗]', '达乌里胡枝子籽[牛枝子籽，豆豆苗籽]', '大玻璃草叶[大车前]', '大巢菜[野苕子，野豌豆]', '大蓟叶[飞廉叶]', '地肤\
[益明，扫帚苗]', '地笋[地古牛，地瓜儿苗叶]', '豆腐柴', '独行菜', '独行菜(宽)', '番杏[夏菠菜，新西兰菠菜]', '胡枝子[山豆子]', '槐花[洋槐花，豆槐花]', '黄麻叶', '碱蓬[棉蓬，猪毛菜]', '\
苦苦菜', '轮叶党参', '罗勒[兰香]', '马齿苋[长寿菜，瓜子菜]', '马兰头[马兰，鸡儿肠，路边菊]', '麦瓶草[米瓦罐]', '牛至', '牛蒡叶', '爬景天[石头菜]', '喷瓜', '婆罗门参(白)', '婆罗门参(\
黑)[鸦葱]', '蒲公英叶[黄花苗叶，孛孛丁叶]', '掐不齐[鸡眼草，牛黄草]', '清明菜[鼠曲菜]', '球茎茴香', '沙参叶[白参]', '沙蓬子[沙米]', '山苦荬叶[启明菜叶]', '食用大黄', '食用黄麻', '酸\
模', '汤菜', '土三七[景天三七]', '歪头菜(草豆，二叶萩)', '梧桐子[瓢儿果]', '夏枯草[铁色草]', '香椿[香椿芽]', '香茅', '小旋花[狗儿蔓]', '鸭跖草[竹叶菜，淡竹叶]', '野葱[沙葱，麦葱]', '\
野韭菜[山韭]', '野菊', '野蒜[小蒜，野葱]', '野苋菜[假苋菜]', '茵陈蒿[茵陈]', '榆钱', '鱼腥草[蕺菜，臭菜]', '珍珠花菜', '紫花桔梗', '紫萼香茶菜', '苣荬菜(尖叶)[取荬菜，苦麻子]', '苜蓿\
[草头，金花菜]', '苜蓿籽[紫苜蓿籽]', '茴芹', '荞菜[野荞]', '蒌蒿', '蕨菜[龙头菜，如意菜]', '蕨菜(脱水)', '蕨麻[鹅绒委陵菜]', '枸杞菜[枸杞，地骨]', '酢浆草[酸酸草，酸溜溜]']
    fruit_name = ['香蕉','苹果','枇杷','草莓','柠檬','梨','石榴','葡萄','橘子','芒果','西瓜','柿子','桂圆','荸荠','桑葚','李子','菠萝','菠萝蜜','杨梅','银杏','无花果','乌梅','甘蔗','人参果','樱桃','黄桃','鳄梨','海棠果','甜瓜','山楂','荔枝','金桔','柑桔','椰子','杨桃','木瓜']
    danwei = ["千卡","毫克","毫克","克","毫克","毫克","克","毫克","毫克","克","毫克","毫克","克","毫克","毫克","微克","毫克","毫克","微克","毫克","毫克","微克","毫克","微克"]
    # vege = liebiao()
    # print(vege,"this is vege")
    # data233 = pa(vege)
    # # init_db("nutrition.db")
    data_base = sqlite3.connect("nutrition.db")
    # print(data233)
    json_vege = []
    c = data_base.cursor()          #获取游标

    sql = "select heat,thiamine,calcium,protein,riboflavin,magnesium,fat,niacin,fe,carbohydrate,vitamin_C,mn,fiber,vitamin_E,zinc,vitamin_A,cholesterol,cu,carotene,k,p,retinol,na,se from fruit"
    result = c.execute(sql)
    # print(result)
    name_id = "heat,thiamine,calcium,protein,riboflavin,magnesium,fat,niacin,fe,carbohydrate,vitamin_C,mn,fiber,vitamin_E,zinc,vitamin_A,cholesterol,cu,carotene,k,p,retinol,na,se".split(",")
    count = 0
    for n in result:
        json_vege.append({})
        json_vege[-1]["name"] = fruit_name[count]
        n_len = len(n)
        for m in range(n_len):
            json_vege[-1][name_id[m]] = str(n[m])+danwei[m]
        count+=1
    # print(vege_name[0],json_vege[0])
    with open("ingredient_fruit.json","w",encoding='utf-8') as f:
        f.write("{\n\"fruit\":[")
        for i in json_vege:
            json.dump(i,f,ensure_ascii=False)
            f.write(",\n")
        f.write("\n]\n}")

    # # print("1 in")
    # for i in range(len(data233)):
    #     try:
    #         # print("2 in")
    #         sql1 = '''INSERT INTO vegetable VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23},{24});
    #         '''.format(i,data233[i][1][0][1],data233[i][1][1][1],data233[i][1][2][1],
    #         data233[i][1][3][1],data233[i][1][4][1],data233[i][1][5][1], data233[i][1][6][1],data233[i][1][7][1],
    #         data233[i][1][8][1],data233[i][1][9][1],data233[i][1][10][1],data233[i][1][11][1],data233[i][1][12][1],
    #         data233[i][1][13][1],data233[i][1][14][1],data233[i][1][15][1],data233[i][1][16][1],data233[i][1][17][1],
    #         data233[i][1][18][1],data233[i][1][19][1],data233[i][1][20][1],data233[i][1][21][1],data233[i][1][22][1],
    #         data233[i][1][23][1])
    #         # print(sql1)
    #         c.execute(sql1)                  #执行sql语句
    #     except:
    #         continue
    # # c.execute(sql2)
    # # sql = "select name from company"
    # # output = c.execute(sql)
    # # for i in output:print(i[0])
    # data_base.commit()              #提交数据库操作
    # data_base.close()               #关闭数据库连接
    print("database is ok!")




'''    
[['热量', '91千卡'], ['硫胺素', '0.02毫克'], ['钙', '7毫克'], ['蛋白质', '1.4克'], ['核黄素', '0.04毫克'], ['镁', '43毫克'], ['脂肪', '0.2克'], ['烟酸', '0.7毫克'], ['铁', '0.4毫克']
, ['碳水化合物', '20.8克'], ['维生素C', '8毫克'], ['锰', '0.65毫克'], ['膳食纤维', '1.2克'], ['维生素E', '0.24毫克'], ['锌', '0.18毫克'], ['维生素A', '10微克'], ['胆固醇', '0毫克'],
['铜', '0.14毫克'], ['胡罗卜素', '0.6微克'], ['钾', '256毫克'], ['磷', '28毫克'], ['视黄醇', '75.8微克'], ['钠', '0.8毫克'], ['硒', '0.87微克']]
'''