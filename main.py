import requests
from bs4 import BeautifulSoup
import re
import json
import os

headers_last_ep = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate,br',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection':'keep-alive',
    'Host':'bangumi.bilibili.com',
    'Upgrade-Insecure-Requests':'1',
    'Cookie': 'buvid3=94CD553E-C174-4C79-BA0C-B0369C33F27E149011infoc; LIVE_BUVID=AUTO8615317334070855; fts=1531733421; rpdid=oqllxikxwidoskomkpoiw; CURRENT_FNVAL=16; _uuid=6708CA4E-7A00-EC7F-A82A-235B4B22432358996infoc; DedeUserID=15059388; DedeUserID__ckMd5=52b5bf0bb36f6fd7; SESSDATA=a27a1af6%2C1564454175%2Cc91d3661; bili_jct=a5a6546ae939914ef3f45d19df7d82b0; UM_distinctid=16ba779892f87-0c7cf860177303-41564133-1fa400-16ba77989301cb; stardustvideo=1; finger=c650951b; flash_player_gray=false; arrange=list; sid=j1wg9685; bsource=seo_baidu',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
}
headers_first ={
    'Host': 'search.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'buvid3=94CD553E-C174-4C79-BA0C-B0369C33F27E149011infoc; LIVE_BUVID=AUTO8615317334070855; fts=1531733421; rpdid=oqllxikxwidoskomkpoiw; CURRENT_FNVAL=16; _uuid=6708CA4E-7A00-EC7F-A82A-235B4B22432358996infoc; DedeUserID=15059388; DedeUserID__ckMd5=52b5bf0bb36f6fd7; SESSDATA=a27a1af6%2C1564454175%2Cc91d3661; bili_jct=a5a6546ae939914ef3f45d19df7d82b0; UM_distinctid=16ba779892f87-0c7cf860177303-41564133-1fa400-16ba77989301cb; stardustvideo=1; finger=c650951b; flash_player_gray=false; arrange=list; sid=j1wg9685; bsource=seo_baidu',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}
headers = {
    'Host': 'api.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://static.hdslb.com/play.swf',
    'Connection': 'keep-alive',
    'Cookie': 'buvid3=94CD553E-C174-4C79-BA0C-B0369C33F27E149011infoc; LIVE_BUVID=AUTO8615317334070855; fts=1531733421; rpdid=oqllxikxwidoskomkpoiw; CURRENT_FNVAL=16; _uuid=6708CA4E-7A00-EC7F-A82A-235B4B22432358996infoc; DedeUserID=15059388; DedeUserID__ckMd5=52b5bf0bb36f6fd7; SESSDATA=a27a1af6%2C1564454175%2Cc91d3661; bili_jct=a5a6546ae939914ef3f45d19df7d82b0; UM_distinctid=16ba779892f87-0c7cf860177303-41564133-1fa400-16ba77989301cb; stardustvideo=1; finger=c650951b; flash_player_gray=false; arrange=list; sid=j1wg9685; bsource=seo_baidu'
}

def main(bangumi):
    infos_list = get_url_info(bangumi)
    root_path = 'E:/bilibilivideos'
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    for info_list in infos_list:
        info_list = get_url_info(bangumi)
        for info in info_list:
            print(info)
            path = root_path + '/' + info[0]['name']
            if not os.path.exists(path):
                os.mkdir(path)
            avid = info[0]['aid']
            cid = info[0]['cid']
            ep_last_id = info[0]['ep_last_id']
            url = 'https://api.bilibili.com/pgc/player/web/playurl?cid='+str(cid)+'&avid='+str(avid)+'&qn=80&otype=json&player=1&fnval=2&fnver=0&ep%5Fid='+ str(ep_last_id)
            temp = requests.get(url,headers=headers).text
            url_video = json.loads(temp)['result']['durl'][0]['backup_url'][0]
            print('正在下载',info[0]['title'],' ',info[0]['long_title'])
            print(url_video)
            result = requests.get(url_video,headers=headers).content
            with open(path + '/' + info[0]['long_title'] + info[0]['title'] + '.mp4','wb') as f:
                print("正在写入文件"+info[0]['long_title'] + info[0]['title'])
                f.write(result)
                print(info[0]['long_title']+info[0]['title'] + "下载完成")
    return

def get_season_id_and_ep_last(bangumi):
    html = requests.get("https://search.bilibili.com/bangumi?keyword=" + bangumi, headers=headers_first)
    soup = BeautifulSoup(html.text, 'lxml')
    aa = soup.find_all('a', class_="left-img")
    result = []
    for a in aa:
        season_id_compile = re.compile(r'.*?ss(.*?)/.*?')
        name = a['title']
        temp = season_id_compile.search(a['href'])
        season_id = temp.group(1)
        url = 'https://bangumi.bilibili.com/view/web_api/season/user/status?season_id='+season_id
        print(url)
        html2 = requests.get(url,headers=headers_last_ep).text
        print(html2)
        last_ep_id = json.loads(html2)['result']['watch_progress']['last_ep_id']
        temp = {}
        temp['season_id'] = season_id
        temp['last_ep_id'] = last_ep_id
        temp['name'] = name
        result.append(temp)
    return result
def get_url_info(bangumi):
    id_infos = get_season_id_and_ep_last(bangumi)
    infos = []
    for id_info in id_infos:
        season_id = id_info['season_id']
        ep_last_id = id_info['last_ep_id']
        second_url = 'https://api.bilibili.com/pgc/web/season/section?season_id='+season_id
        episodes = json.loads(requests.get(second_url,headers=headers).text)
        info = []
        for episode in episodes['result']['main_section']['episodes']:
            temp = {}
            title = episode['title']
            long_title = episode['long_title']
            aid = episode['aid']
            cid = episode['cid']
            temp['title'] = title
            temp['long_title'] = long_title
            temp['aid'] = aid
            temp['cid'] = cid
            temp['season_id'] = season_id
            temp['ep_last_id'] = ep_last_id
            temp['name'] = id_info['name']
            info.append(temp)
        infos.append(info)
    return infos





if __name__ == '__main__':
    main("我的青春恋爱物语果然有问题")







# url1 = 'http://cn-zjjh5-dx-v-01.acgvideo.com/upgcxcode/06/42/101834206/101834206-1-32.flv?expires=1563373800&platform=pc&ssig=JinI-wZXQZ9VzalxLORUww&oi=454532687&trid=d1ebd2afbca74cae906b9c49775b0f36p&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1'
# url2 = 'http://cn-jstz-dx-v-04.acgvideo.com/upgcxcode/06/42/101834206/101834206-1-32.flv?expires=1563373800&platform=pc&ssig=JinI-wZXQZ9VzalxLORUww&oi=454532687&trid=d1ebd2afbca74cae906b9c49775b0f36p&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1'
# url3 = 'url=http://cn-zjwz3-dx-v-11.acgvideo.com/upgcxcode/06/42/101834206/101834206-1-32.flv?expires=1563373800&platform=pc&ssig=JinI-wZXQZ9VzalxLORUww&oi=454532687&trid=d1ebd2afbca74cae906b9c49775b0f36p&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1'
#
# data1 = requests.get(url=url1,headers=headers)
# print("开始写入")
# with open('1.mp4','wb') as f:
#     f.write(data1.content)
#
# data2 = requests.get(url=url2,headers=headers)
# with open('2.mp4','wb') as f:
#     f.write(data2.content)

#print(data.content)
#print(data.text)