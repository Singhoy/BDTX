# coding: utf8
# 百度百家号
import json
import re
import requests
import signal
import sys
import time

from datetime import datetime
from time import sleep

from lxml import etree
from lxml.html import tostring
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def 头信息():
    return {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.8",
        "referer": "https://www.baidu.com",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36",
    }


def 作者(i, j):
    datas = {
        "word": f"{i}+百家号",
        "pd": "cambrian_list",
        "atn": "index",
        "title": f"{i}+百家号",
        "lid": "8219726775998088715",
        "ms": "1",
        "frsrcid": "206",
        "frorder": "1",
        "sig": "593303",
        "pn": 10*j,
        "mod": "1",
    }
    url = "https://m.baidu.com/sf"
    headers = 头信息()
    response = requests.get(url, params=datas, headers=headers, verify=False)
    html = response.text
    tree = etree.HTML(html)
    datas = tree.xpath('//div[@class="sfc-cambrian-list-subscribe"]')
    urls = []
    for data in datas:
        url = data.xpath('./div/a/@href')[0]
        urls.append(url)
    return urls


def 百度身份():  # cookie信息
    _dict = {
        "BAIDUCUID": "g8SKtgu0B8l_u2uNguHn8ga1SuY48Huc0avpigioSaizaB8fgO25i_uqvfYua2tHA",
        "BAIDUID": "93152B7B6EA7D252BE7FF1F22942C5505:FG=1",
        "BDORZ": "AE84CDB3A529C0F8A2B9DCDD1D18B695",
        "MBD_AT": "1555920950",
        "WISE_HIS_PM": "1",
        "fontsize": "1.0",
        "GID": "G1S2QXSERVKJMD5X6821O78AOQ1QJ4P3J8",
        "BAIDULOC": "13523058_3642420_65_289_1555928065154",
        "delPer": "0",
        "PSINO": "5",
        "H_WISE_SIDS": "130510_124622_110086_131021_123289_131093_127417_130611_131210_131264_131263_131257_128806",
    }
    cookies = "".join(f"{k}={v}; " for k, v in _dict.items())[:-2]
    return cookies


def get_id(url):
    response = requests.get(url=url, verify=False)
    html = response.text
    try:
        # https://author.baidu.com/home?from=bjh_article&app_id=1563494548596100
        app_id = re.findall('home/(.*)\?from=dusite_sresults"', html)[0]
        # print("APPID:", app_id)
        return app_id
    except:
        pass


def homepage(app_id):  # 通过id获取个人主页页面信息
    cookies = 百度身份()
    url = f"https://author.baidu.com/home?from=bjh_article&app_id={app_id}"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.8",
        "referer": "https://www.baidu.com",
        "cookies": cookies,
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36",
    }
    html = requests.get(url, headers=headers, verify=False)
    # _当前 = datetime.now()
    # with open(f"BJH/{app_id}-{_当前.second}.html", "wb") as f:
    # f.write(html.content)
    return html.text


def parse(html, app_id):
    author = re.findall(r'display_name":"(.*?)"', html)[0]  # 用户昵称
    author = eval(repr(author).replace(r"\\", "\\"))
    home_url = 'https://author.baidu.com/home/' + app_id  # 用户主页地址
    avatar_url = re.findall('avatar_raw\":\"(.*?)",', html)[0]
    avatar_url = eval(repr(avatar_url).replace(r"\\", ""))  # 用户头像地址
    brief = str(re.findall('sign\":\"(.*?)\",', html)[0])  # 作者简介
    brief = eval(repr(brief).replace(r"\\", "\\"))
    fans_num = re.findall('fans_num.*?:\"(.*?)\",', html)[0]  # 粉丝数量
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 创建时间
    source_name = '百家号'  # 来源名称
    follow_num = re.findall('follow_num.*?:\"(.*?)\",', html)[0]  # 关注数
    uk = re.findall('uk.*?:\"(.*?)\",', html)[0]  # uk码
    biz = app_id+'/'+uk
    item = {"作者": author, "主页链接": home_url, "头像地址": avatar_url, "简介": brief, "粉丝数": fans_num,
            "创建时间": create_time, "来源": source_name, "关注数": follow_num, "UK": uk, "BIZ": biz}
    # print(item)
    return item


def 文章列表(uk, app_id, ct=0):
    """
    uk: QNweF8VzTDPt_xoVhtQcow
    appid: 1563494548596100
    ct: 翻页标记
    """
    cookies = 百度身份()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.0.8793 Safari/537.36"
    }
    headers["Cookie"] = cookies
    headers["Referer"] = f"https://author.baidu.com/home/{app_id}"
    while 1:
        signal.signal(signal.SIGTERM, 退出)
        signal.signal(signal.SIGINT, 退出)
        jp = 造jp()
        if ct == 0:
            url = f"https://mbd.baidu.com/webpage?tab=article&num=10&uk={uk}&source=pc&type=newhome&action=dynamic&format=jsonp&otherext=h5_20210510153345&Tenger-Mhor=3607731347&callback={jp}"
        else:
            url = f"https://mbd.baidu.com/webpage?tab=article&num=10&uk={uk}&source=pc&ctime={ct}&type=newhome&action=dynamic&format=jsonp&otherext=h5_20210510153345&Tenger-Mhor=3607731347&callback={jp}"
        ct = 获取json数据(url, headers)
        sleep(1)
        # return
        if not ct:
            return


def 造jp():
    _t = time.time()
    t_ = str(_t).split(".")
    jp = "__jsonp0" + t_[0] + t_[1][:3]
    return jp


def 获取json数据(url, headers):
    resp = requests.get(url, headers=headers, verify=False)
    _next = 提取数据(resp.content.decode("utf8"))
    return _next


def 提取数据(data):
    a = re.findall(r"\((.*?)\)", data)
    b = json.loads(a[0])
    c = b.get("data").get("list")
    for i in c:
        itemdata = i.get("itemData")
        print("=====" * 20)
        title = itemdata.get("title")
        url = itemdata.get("url")
        item = {"标题": title, "链接": url}
        # print(item)
        访问详情页(item)
    next_ = b.get("data").get("query").get("ctime")
    print(next_)
    return next_


def 访问详情页(data: dict):
    url = data.get("链接")
    cookie = 百度身份()
    headers = {
        "Cookie": cookie,
        "Host": "baijiahao.baidu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, verify=False)
    sleep(1)
    # ss = data.get("标题")
    # title = ss.replace(r"\\", "-").replace("/", "-").replace("|", "-").replace("<", "《").replace(
    #     ">", "》").replace(":", "：").replace("?", "？").replace("*", "-").replace("\"", "'")
    # with open(f"./BJH/{title}.html", 'wb') as f:
    # f.write(resp.content)
    print(resp.status_code)
    # TODO 解析详情页
    item = 解析详情(resp.content.decode("utf8"), data)
    print("******" * 20)
    print(item)
    # 保存(item)


def 保存(ss: dict):
    title = ss.get("标题").replace(r"\\", "-").replace("/", "-").replace("|", "-").replace("<", "《").replace(">", "》")\
        .replace(":", "：").replace("?", "？").replace("*", "-").replace(r"\"", "'")
    with open(f"./BJH/{title}.json", "w", encoding="utf8") as f:
        d = json.dumps(ss, ensure_ascii=False)
        f.write(d)
        f.flush()


def 解析详情(data, item):
    el = etree.HTML(data)
    au = el.xpath('//p[contains(@class, "authorName")]')[0].text
    # print(au)
    t = el.xpath('//div[contains(@class, "articleSource")]//span/text()')
    ct = " ".join(t)
    # print(ct)
    # divs = el.xpath('//div[contains(@class, "articleWrap_")]/div')
    # cons = []
    # for div in divs:
    #     con = tostring(div)
    #     cons.append(con)
    item["作者"] = au
    item["时间"] = ct
    # item["内容"] = cons
    return item


def 退出(signum, frame):
    print("退出~~")
    sys.exit(0)


def 运行():
    kw = "道哥说车"
    urls = 作者(kw, 0)
    print("==========" * 20)
    for url in urls:
        app_id = get_id(url)
        # app_id=1563494548596100
        html = homepage(app_id)
        data = parse(html, app_id)
        name = data.get("作者")
        if kw == name[:len(kw)]:
            break
        sleep(1)
    uk = data.get("UK")
    文章列表(uk, app_id)


if __name__ == "__main__":
    # 作者("道哥说车", 2)
    运行()
