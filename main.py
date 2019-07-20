import requests
from bs4 import BeautifulSoup
import re
import json
import os
from queue import Queue
import threading


headers_last_ep = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate,br',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection':'keep-alive',
    'Host':'bangumi.bilibili.com',
    'Upgrade-Insecure-Requests':'1',
    'Cookie': 'buvid3=94CD553E-C174-4C79-BA0C-B0369C33F27E149011infoc; LIVE_BUVID=AUTO8615317334070855; fts=1531733421; rpdid=oqllxikxwidoskomkpoiw; CURRENT_FNVAL=16; UM_distinctid=16ba779892f87-0c7cf860177303-41564133-1fa400-16ba77989301cb; stardustvideo=1; finger=c650951b; flash_player_gray=false; arrange=list; im_notify_type_15059388=0; html5_player_gray=false; sid=5f3ry19x; stardustpgcv=0606; DedeUserID=15059388; DedeUserID__ckMd5=52b5bf0bb36f6fd7; SESSDATA=d4782adf%2C1566177984%2C22789371; bili_jct=920c83187e7bca56c614c8d7aa31a7bf',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
}
headers_first ={
    'Host': 'search.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'buvid3=94CD553E-C174-4C79-BA0C-B0369C33F27E149011infoc; LIVE_BUVID=AUTO8615317334070855; fts=1531733421; rpdid=oqllxikxwidoskomkpoiw; CURRENT_FNVAL=16; UM_distinctid=16ba779892f87-0c7cf860177303-41564133-1fa400-16ba77989301cb; stardustvideo=1; finger=c650951b; flash_player_gray=false; arrange=list; im_notify_type_15059388=0; html5_player_gray=false; sid=5f3ry19x; stardustpgcv=0606; DedeUserID=15059388; DedeUserID__ckMd5=52b5bf0bb36f6fd7; SESSDATA=d4782adf%2C1566177984%2C22789371; bili_jct=920c83187e7bca56c614c8d7aa31a7bf',
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
    'Cookie': 'buvid3=94CD553E-C174-4C79-BA0C-B0369C33F27E149011infoc; LIVE_BUVID=AUTO8615317334070855; fts=1531733421; rpdid=oqllxikxwidoskomkpoiw; CURRENT_FNVAL=16; UM_distinctid=16ba779892f87-0c7cf860177303-41564133-1fa400-16ba77989301cb; stardustvideo=1; finger=c650951b; flash_player_gray=false; arrange=list; im_notify_type_15059388=0; html5_player_gray=false; sid=5f3ry19x; stardustpgcv=0606; DedeUserID=15059388; DedeUserID__ckMd5=52b5bf0bb36f6fd7; SESSDATA=d4782adf%2C1566177984%2C22789371; bili_jct=920c83187e7bca56c614c8d7aa31a7bf'
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
def get_url(temp):
    url = []
    for video in json.loads(temp)['result']['durl']:
        #if not video['backup_url']:
        #    for backup_url in video['backup_url']:
        #        url.append(video['backup_url'])
        #else:
        url.append(video['url'])
    return url
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
        i = 1
        urls = get_url(temp)
        for url_video in urls:
            print('正在下载',info['title'],' ',info['long_title'],'第',i,'部分')
            print(url_video)
            result = requests.get(url_video,headers=headers).content
            if not os.path.exists(path + '/' + (info['long_title'] + info['title']).replace('/','')):
                os.mkdir(path + '/' + (info['long_title'] + info['title']).replace('/',''))
            with open(path + '/' + (info['long_title'] + info['title']).replace('/','') + '/' + str(i) + '.mp4','wb') as f:
                f.write(result)
                print(info['long_title']+info['title'] + "下载完成")
                i = i + 1
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
    id_info = get_season_id(bangumi)[0]
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
    main("凹凸世界。")
    #url = 'http://upos-hz-mirrorcosu.acgvideo.com/upgcxcode/88/40/55444088/55444088-1-32.flv?e=ig8euxZM2rNcNbhBhwdVhoMz7WdVhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNo8g2ENvNo8i8o859r1qXg8xNEVE5XREto8GuFGv2U7SuxI72X6fTr859r1qXg8gNEVE5XREto8z5JZC2X2gkX5L5F1eTX1jkXlsTXHeux_f2o859IB_&deadline=1563587123&gen=playurl&nbs=1&oi=454531465&os=cosu&platform=pc&trid=74a8105055f44bacad9ea93d79ac4157p&uipk=5&upsig=3e44be7eb9623d019a4700f93f17f92f&uparams=e,deadline,gen,nbs,oi,os,platform,trid,uipk'
    #result = requests.get(url,headers=headers).content
    #with open('1.mp4','wb+') as f:
    #    f.write(result)





