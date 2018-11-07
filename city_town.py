# encoding: utf-8

import pandas as pd
import requests
import re
import json
import copy


if __name__ == '__main__':

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
    for prov in province:
        r = requests.get(filepath, params={"key": "737269e88323592ea805bb6f6f4176db"
            , "keywords": prov
            , "subdistrict": 2
            , "output": "JSON"
            , "ie": "utf-8"})

        for i in r.json()["districts"][0]["districts"]:
            prov = r.json()["districts"][0]["name"]
            city = i["name"]
            for j in i["districts"]:
                town = j["name"]
                dict_t = {"province": prov, 'city': city, "town": town}
                lst.append(dict_t)

    df = pd.DataFrame(lst)
    df["province2"] = list(map(lambda x: re.sub(r"省|市|自治区|特别行政区", "",  x), df["province"]))
    df["city2"] = list(map(lambda x: re.sub(r"市|城区", "", x), df["city"]))
    df["town2"] = list(map(lambda x: re.sub(r"市|县|镇|区", "", x), df["town"]))
    # s = set([x[-1] for x in df['city']])
    df["qu"] = None
    for i in range(len(df)):
        if df["province2"][i] in ["山东", "江苏", "安徽", "江西", "浙江", "福建", "上海"]:
            df["qu"][i] = "华东地区"
        elif df["province2"][i] in ["广东", "广西", "海南"]:
            df["qu"][i] = "华南地区"
        elif df["province2"][i] in ["湖北", "湖南", "河南"]:
            df["qu"][i] = "华中地区"
        elif df["province2"][i] in ["北京", "天津", "河北", "山西", "内蒙古"]:
            df["qu"][i] = "华北地区"
        elif df["province2"][i] in ["宁夏", "新疆维吾尔", "青海", "陕西", "甘肃"]:
            df["qu"][i] = "西北地区"
        elif df["province2"][i] in ["四川", "云南", "贵州", "西藏", "重庆"]:
            df["qu"][i] = "西南地区"
        elif df["province2"][i] in ["辽宁", "吉林", "黑龙江"]:
            df["qu"][i] = "东北地区"
        elif df["province2"][i] in ["台湾", "香港", "澳门"]:
            df["qu"][i] = "港澳台地区"
    print(df)
    print(df[df["qu"] == None])
