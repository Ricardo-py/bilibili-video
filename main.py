import requests
from bs4 import BeautifulSoup
import re
import json
import os
from queue import Queue
import threading


#需要解决的问题：
#1.cookie要定时更新
#2.这种爬取方法对于所有视频不是通用的

headers_last_ep = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate,br',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection':'keep-alive',
    'Host':'bangumi.bilibili.com',
    'Upgrade-Insecure-Requests':'1',
    'Cookie': 'buvid3=94CD553E-C174-4C79-BA0C-B0369C33F27E149011infoc; LIVE_BUVID=AUTO8615317334070855; fts=1531733421; rpdid=oqllxikxwidoskomkpoiw; CURRENT_FNVAL=16; DedeUserID=15059388; DedeUserID__ckMd5=52b5bf0bb36f6fd7; SESSDATA=a27a1af6%2C1564454175%2Cc91d3661; bili_jct=a5a6546ae939914ef3f45d19df7d82b0; UM_distinctid=16ba779892f87-0c7cf860177303-41564133-1fa400-16ba77989301cb; stardustvideo=1; finger=c650951b; flash_player_gray=false; arrange=list; sid=5lqkwn06',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
}
headers_first ={
    'Host': 'search.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'buvid3=94CD553E-C174-4C79-BA0C-B0369C33F27E149011infoc; LIVE_BUVID=AUTO8615317334070855; fts=1531733421; rpdid=oqllxikxwidoskomkpoiw; CURRENT_FNVAL=16; DedeUserID=15059388; DedeUserID__ckMd5=52b5bf0bb36f6fd7; SESSDATA=a27a1af6%2C1564454175%2Cc91d3661; bili_jct=a5a6546ae939914ef3f45d19df7d82b0; UM_distinctid=16ba779892f87-0c7cf860177303-41564133-1fa400-16ba77989301cb; stardustvideo=1; finger=c650951b; flash_player_gray=false; arrange=list; sid=5lqkwn06',
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
    'Cookie': 'buvid3=94CD553E-C174-4C79-BA0C-B0369C33F27E149011infoc; LIVE_BUVID=AUTO8615317334070855; fts=1531733421; rpdid=oqllxikxwidoskomkpoiw; CURRENT_FNVAL=16; DedeUserID=15059388; DedeUserID__ckMd5=52b5bf0bb36f6fd7; SESSDATA=a27a1af6%2C1564454175%2Cc91d3661; bili_jct=a5a6546ae939914ef3f45d19df7d82b0; UM_distinctid=16ba779892f87-0c7cf860177303-41564133-1fa400-16ba77989301cb; stardustvideo=1; finger=c650951b; flash_player_gray=false; arrange=list; sid=5lqkwn06'
}

class MyThread(threading.Thread):
    def __init__(self,func,name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.name = name

    def run(self):
        self.func()


info_queue = Queue()
root_path = 'E:/bilibilivideos'
def video_download():
    global info_queue
    while (not info_queue.empty()):
        print("队列是否为空:" + str(info_queue.empty()))
        info = info_queue.get(1)
        print(info)
        path = root_path + '/' + info['name']
        if not os.path.exists(path):
            os.mkdir(path)
        avid = info['aid']
        cid = info['cid']
        ep_last_id = info['ep_last_id']
        url = 'https://api.bilibili.com/pgc/player/web/playurl?cid='+str(cid)+'&avid='+str(avid)+'&qn=64&otype=json&player=1&fnval=2&fnver=0&ep%5Fid='+ str(ep_last_id)
        temp = requests.get(url,headers=headers).text
        print(temp)
        url_video = json.loads(temp)['result']['durl'][0]['url']
        print('正在下载',info['title'],' ',info['long_title'])
        print(url_video)
        result = requests.get(url_video,headers=headers).content
        with open(path + '/' + (info['long_title'] + info['title']).replace('/','') + '.mp4','wb') as f:
            f.write(result)
            print(info['long_title']+info['title'] + "下载完成")
    print("结束")
    return

def main(bangumi):
    info_list = get_url_info(bangumi)
    for info in info_list:
        info_queue.put(info)
    threads = []
    nloops = range(5)
    for i in nloops:
        t = MyThread(video_download,video_download.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print("下载完成")
def get_season_id(bangumi):
    html = requests.get("https://search.bilibili.com/bangumi?keyword="+bangumi, headers=headers_first)
    soup = BeautifulSoup(html.text, 'lxml')
    aa = soup.find_all('a', class_="left-img")
    result = []
    for a in aa:
        season_id_compile = re.compile(r'.*?ss(.*?)/.*?')
        name = a['title']
        temp = season_id_compile.search(a['href'])
        season_id = temp.group(1)
        temp = {}
        temp['season_id'] = season_id
        temp['name'] = name
        result.append(temp)
    print(result)
    return result

def get_url_info(bangumi):
    #得到season_id
    id_info = get_season_id(bangumi)[0]
    #得到第一部分的ep_id
    html = requests.get("https://search.bilibili.com/bangumi?keyword="+bangumi, headers=headers_first)
    soup = BeautifulSoup(html.text, 'lxml')
    find_ep = re.compile(r'.*?"eps":(.*?)}],*?')
    temp = find_ep.search(html.text)
    find_ep_id = re.compile(r'"id":(.*?),')
    ep_ids = find_ep_id.findall(temp.group(1))
    print(ep_ids)
    season_id = id_info['season_id']
    second_url = 'https://api.bilibili.com/pgc/web/season/section?season_id='+season_id
    episodes = json.loads(requests.get(second_url,headers=headers).text)
    info = []
    for ep_id, episode in list(zip(ep_ids,episodes['result']['main_section']['episodes'])):
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
        temp['ep_last_id'] = ep_id
        temp['name'] = id_info['name']
        info.append(temp)
    return info





if __name__ == '__main__':
    main("搞笑漫画日和")
    #strr = "sdffs/sdfsaf"
    #print(strr.replace('/',''))







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