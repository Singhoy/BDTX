import json
import re
import time

import requests


def 测试():
    ids = 提取id()
    if len(ids) > 0:
        res = 获取文章(ids)
        for i in res:
            print("======" * 20)
            ii = 解析(i)
            保存(ii)
            time.sleep(1)
    print("完成~~~")


def 保存(ss):
    title = ss.get("标题").replace(r"\\", "-").replace("/", "-").replace("|", "-").replace("<", "《").replace(">", "》")\
        .replace(":", "：").replace("?", "？").replace("*", "-").replace(r"\"", "'")
    with open(f"./QEH/{title}.json", "w", encoding="utf8") as f:
        s = json.dumps(ss, ensure_ascii=False)
        f.write(s)
        f.flush()


def 解析(data: dict):
    title = data.get("title")
    url = data.get("url")
    print(url)
    abstract = data.get("abstract")
    item = {
        "标题": title,
        "作者": data.get("source"),
        "发布时间": data.get("time"),
        "来源": "企鹅号",
        "链接": url,
        "摘要": abstract
    }
    resp = requests.get(url)
    print(resp.status_code)
    # with open(f"./QEH/{title}.html", "wb") as f:
    # f.write(resp.content)
    datas = resp.content.decode("utf8")
    cnt_html = re.findall(r"cnt_html\":\"(.*?)\",\"", datas)
    # print(cnt_html)
    cnt_attr = re.findall(r"cnt_attr\":(.*)}},\"", datas)
    cnt_attr = list(cnt_attr)
    # print(cnt_attr)
    for i in cnt_attr:
        imgs = json.loads(i+"}}")
        # print(imgs)
    for i in cnt_html:
        a = i.replace(r"\u003cP\u003e", "").replace(r"\u003c/P\u003e", "\n\r")
        # print(a)
        print("--------" * 20)
        b = re.findall(r"!--(.*?)--", a)
        # print(b)
        for _ in b:
            try:
                img = imgs.get(_).get("img").get("imgurl1000").get("imgurl")
            except:
                try:
                    img = imgs.get(_).get('imgurl')
                except:
                    img = "--多媒体链接丢失--"
            a = a.replace(_, img)
        cont = a.replace(r"\u003c!--", "{链接：").replace(r"--\u003e", " 链接结束}").replace(
            r"\u003cSTRONG\u003e", "{加粗：").replace(r"\u003c/STRONG\u003e", "：加粗结束}")
        print(cont)
    item["正文"] = cont
    return item


def 获取文章(ids):
    try:
        ids = str(ids).replace(']', '').replace(
            '[', '').replace("'", '').replace(' ', '')
        url = f'https://r.inews.qq.com/getSubNewsListItems?ids={ids}&appver=25_android_5.8.12&devid=44ce3651532c37f9&qn-sig=0b59fd561bfbad40747db5fea582b5af&qn-rid=f4af5a1d-34c1-44dd-aa04-c31b470c03b4'
        response = requests.get(url)
        # with open("./QEH/文章.json", "wb") as f:
        # f.write(response.content)
        datas = json.loads(response.text)['newslist']
    except:
        datas = []
    return datas


def 提取id():
    info = {"biz": "qiehao10002244"}
    author_id = info['biz'].replace('qiehao', "")
    ids = []
    try:
        url = f'https://r.inews.qq.com/getSubNewsIndex?chlid={author_id}'
        response = requests.get(url=url)
        # with open("./QEH/文章.json", "wb") as f:
        # f.write(response.content)
        nums = json.loads(response.text)['ids']
        if len(nums) >= 100:
            for i in range(100):
                ids.append(nums[i]['id'])
        else:
            for i in range(len(nums)):
                ids.append(nums[i]['id'])
        return ids
    except:
        ids = []
        return ids


def 获取作者():
    headers = 头信息()
    data = 请求数据("道哥说车")
    url = 'https://r.inews.qq.com/verticalSearch?chlid=_qqnews_custom_search_qiehao&search_from=click&uid=44ce3651532c37f9&omgid=e76c5bfab95b6547ffab46fb08c39bd795f60010213414&trueVersion=5.8.12&qimei=44ce3651532c37f9&appver=25_android_5.8.12&devid=44ce3651532c37f9&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&qn-sig=f50e2c8c758767a6bc87be6605573722&qn-rid=219c9f88-e74a-4670-bb7d-3497cec83c8a'
    response = requests.post(url, data=data, headers=headers, timeout=15)
    html = json.loads(response.text)
    # with open("./QEH/测试.json", "wb") as f:
    # f.write(response.content)
    datas = html['secList']
    # print(datas)
    # return datas
    for i in datas:
        print("=====" * 20)
        # print(i)
        data = i['omList'][0]
        nick = data.get("nick")
        if "道哥说车" == nick[:4]:
            print(nick)
            res = 提取信息(data, nick)
            return res
        time.sleep(1)


def 粉丝数(url):
    try:
        res = requests.get(url)
        # with open("./QEH/粉丝.json", "wb") as f:
        # f.write(res.content)
        fans_num = json.loads(res.text)[
            'channelInfo']['subCount']
    except:
        fans_num = 0
    return fans_num


def 提取信息(data, keyword):
    print(data)
    try:
        author = data.get("chlname")  # 用户昵称
        biz = f"qiehao{data.get('chlid')}"
        # 用户主页地址
        home_url = f"https://r.inews.qq.com/getSubItem?chlid={data.get('chlid')}"
        avatar_url = data.get("head_url")  # 用户头像地址
        brief = data.get("user_desc")  # 作者简介
        create_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())  # 创建时间
        source_name = '企鹅号'  # 来源名称
        fans_num = int(粉丝数(home_url))  # 粉丝数量
        tags = keyword
        # sql1 = 'select * from spider_user_info where author="%s"' % author
        # cursor = self.tools.sqll(sql1)
        # result = cursor.fetchall()
        # if not result and fans_num >= 1:
        # sql2 = 'insert into spider_user_info(id,author,biz,home_url,avatar_url,brief,create_time,source_name,fans_num,tags) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
        # id, author, biz, home_url, avatar_url, brief, create_time, source_name, fans_num, tags)
        # self.tools.sqll(sql2)
        # print(id, author, biz, home_url, avatar_url, brief,
        #   create_time, source_name, fans_num, tags)
        # else:
        # pass
        res = {
            "作者": author,
            "biz": biz,
            "主页链接": home_url,
            "头像链接": avatar_url,
            "简介": brief,
            "抓取时间": create_time,
            "来源": source_name,
            "粉丝量": fans_num,
            "标签": tags
        }
        # print(res)
        return res
    except Exception as e:
        print("ERROR", e)


def 请求数据(keyword):
    data = {
        "search_type": "qiehao",
        "query": keyword,
        "cp_type": "0",
        "disable_qc": "0",
        "searchStartFrom": "header",
        "launchSearchFrom": "btn",
        "isDefault": "0",
        "searchTag": keyword,
        "provinceId": "12",
        "currentChannelId": "news_news_top",
        "isElderMode": "0",
        "apptype": "android",
    }
    return data


def 头信息():
    headers = {
        "Cookie": "lskey=;skey=;uin=; luin=;logintype=0; main_login=;",
        "RecentUserOperation": "1_news_background,1_news_news_top,2_ChannelSetting",
        "Referer": "http://inews.qq.com/inews/android/",
        "User-Agent": "%E8%85%BE%E8%AE%AF%E6%96%B0%E9%97%BB5810(android)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "2275",
        "Host": "r.inews.qq.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "client-ip-v4": "180.154.220.183",
    }
    return headers


if __name__ == "__main__":
    测试()
