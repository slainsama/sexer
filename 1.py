import requests
import json
import re
url = "https://www.pixiv.net/ranking.php"
proxy = "127.0.0.1:7890"
proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy
}
params = (
    ('p', 1),
    ('format', 'json'),
)
header = {
    'authority': 'www.pixiv.net',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 '
                  'Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'PHPSESSID=49701993_2Y3bte5wkoD2gKbJ85jejuQ0L5IaPW1U',
}


def get_id():
    index_response = requests.get(url=url, headers=header, proxies=proxies, params=params).text
    data = json.loads(index_response)
    url_base = "https://i.pximg.net/img-original/"
    for i in data["contents"]:
        pattern = re.compile('img/[0-9]{4}/[0-9]{2}/[0-9]{2}/[0-9]{2}/[0-9]{2}/[0-9]{2}/[0-9]{8}')
        url_id = pattern.search(i["url"]).group()
        if i["url"][-3:] == "jpg":
            for k in range(0, int(i['illust_page_count'])):
                url_final = url_base + url_id + "_p" + str(k) + ".jpg"
                r = requests.get(url=url_final, headers=header, proxies=proxies)
                if r.status_code == 404:
                    url_final = url_base + url_id + "_p" + str(k) + ".png"
                    print([url_final, i["title"]])
                    r = requests.get(url=url_final, headers=header, proxies=proxies)
                    png = open("pixiv/" + i["title"] + str(k) + ".png", "wb")
                    png.write(r.content)
                else:
                    print([url_final, i["title"]])
                    png = open("pixiv/" + i["title"] + str(k) + ".jpg", "wb")
                    png.write(r.content)


get_id()
