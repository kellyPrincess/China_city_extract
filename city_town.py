# encoding: utf-8

import pandas as pd
import requests
import re
import time
import json
import copy
import warnings
warnings.filterwarnings("ignore")


def prov_city_town():
    province = ["北京市",
                "天津市",
                "上海市",
                "重庆市",
                "河北省",
                "山西省",
                "辽宁省",
                "吉林省",
                "黑龙江省",
                "江苏省",
                "浙江省",
                "安徽省",
                "福建省",
                "江西省",
                "山东省",
                "河南省",
                "湖北省",
                "湖南省",
                "广东省",
                "海南省",
                "四川省",
                "贵州省",
                "云南省",
                "陕西省",
                "甘肃省",
                "青海省",
                "台湾省",
                "内蒙古自治区",
                "广西壮族自治区",
                "西藏自治区",
                "宁夏回族自治区",
                "新疆维吾尔自治区",
                "香港特别行政区",
                "澳门特别行政区"]
    filepath = r'http://restapi.amap.com/v3/config/district?parameters'
    lst = []
    r_lst = []
    if False:
        with open("raw_json_2.json", "w", encoding="utf-8") as f:
            for prov in province:
                r = requests.get(filepath, params={"key": "737269e88323592ea805bb6f6f4176db"
                    , "keywords": prov
                    , "subdistrict": 2
                    , "output": "JSON"
                    , "ie": "utf-8"})
                f.write(json.dumps(r.json(), ensure_ascii=False) + "\n")
                r_lst.append(r.json())
    if True:
        with open("raw_json_2.json", "r", encoding="utf-8") as f:
            for line in f.readlines():
                r = json.loads(line)
                r_lst.append(r)
    for r in r_lst:
        for i in r["districts"][0]["districts"]:
            prov = r["districts"][0]["name"]
            city = i["name"]
            for j in i["districts"]:
                town = j["name"]
                dict_t = {"province": prov, 'city': city, "town": town}
                lst.append(dict_t)

    df = pd.DataFrame(lst)
    print(df["province"].unique())

    df["province2"] = list(map(lambda x: re.sub(r"省|市|回族自治区|壮族自治区|维吾尔自治区|自治区|特别行政区", "", x), df["province"]))
    df["city2"] = list(map(lambda x: re.sub(r"市|城区|自治州|自治县", "", x), df["city"]))
    df["town2"] = list(map(lambda x: re.sub(r"新区|区|市|自治县|县|镇|", "", x), df["town"]))  # 注意会出现单个字符串
    df["qu"] = None

    print(df["province2"].unique())
    exit()

    for i in range(len(df)):
        if df["province2"][i] in ["山东", "江苏", "安徽", "江西", "浙江", "福建", "上海"]:
            df["qu"][i] = "华东地区"
        elif df["province2"][i] in ["广东", "广西", "海南"]:
            df["qu"][i] = "华南地区"
        elif df["province2"][i] in ["湖北", "湖南", "河南"]:
            df["qu"][i] = "华中地区"
        elif df["province2"][i] in ["北京", "天津", "河北", "山西", "内蒙古"]:
            df["qu"][i] = "华北地区"
        elif df["province2"][i] in ["宁夏", "新疆", "青海", "陕西", "甘肃"]:
            df["qu"][i] = "西北地区"
        elif df["province2"][i] in ["四川", "云南", "贵州", "西藏", "重庆"]:
            df["qu"][i] = "西南地区"
        elif df["province2"][i] in ["辽宁", "吉林", "黑龙江"]:
            df["qu"][i] = "东北地区"
        elif df["province2"][i] in ["台湾", "香港", "澳门"]:
            df["qu"][i] = "港澳台地区"

    p1 = df[["province", "qu"]]
    p2 = df[["province2", "qu"]]
    p1.rename(columns={"province": "pct"}, inplace=True)
    p2.rename(columns={"province2": "pct"}, inplace=True)
    prov_df = pd.concat([p1, p2]).drop_duplicates()
    prov_df.index = [i for i in range(len(prov_df))]

    c1 = df[["city", "qu"]]
    c2 = df[["city2", "qu"]]
    c1.rename(columns={"city": "pct"}, inplace=True)
    c2.rename(columns={"city2": "pct"}, inplace=True)
    city_df = pd.concat([c1, c2]).drop_duplicates()
    city_df.index = [i for i in range(len(city_df))]

    t1 = df[["town", "qu"]]
    t2 = df[["town2", "qu"]]
    t2 = t2[t2["town2"].map(len) > 1]  # 筛选出该列中长度大于1的值
    t1.rename(columns={"town": "pct"}, inplace=True)
    t2.rename(columns={"town2": "pct"}, inplace=True)
    town_df = pd.concat([t1, t2]).drop_duplicates()
    town_df.index = [i for i in range(len(town_df))]

    # pct = pd.concat([prov_df, city_df, town_df]).drop_duplicates()
    # pct.index = [i for i in range(len(pct))]
    return [prov_df, city_df, town_df]


def read_hive():
    df = prov_city_town()
    df = df[0]

    china_qu = open("name_qu.txt", "w", encoding="utf-8")
    china_none = open("name_none.txt", "w", encoding="utf-8")
    for i in range(1, 3):

        cnt = 0
        with open("ent_0{}".format(i), "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                for j in range(len(df)):
                    if str(df["pct"][j]) in name:
                        qu = df["qu"][j]
                        china_qu.write(name.strip() + "$" + qu.strip() + "\n")
                        break
                    else:
                        qu = ''
                        china_none.write(name.strip() + "$" + qu + "\n")

                cnt += 1
                if cnt % 50000 == 0:
                    china_qu.flush()
                    china_none.flush()
                    print("{} cnt={}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), cnt))

    china_qu.close()
    china_none.close()
    print("--over--")


if __name__ == '__main__':
    prov_city_town()
    # print(read_hive())


