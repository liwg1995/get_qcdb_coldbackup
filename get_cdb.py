# -*- coding: utf-8 -*-

import os
from QcloudApi.qcloudapi import QcloudApi
import json
# import requests
import datetime
import urllib2

module = 'cdb'

action = 'GetCdbExportLogUrl'

config = {
    'Region' : '**',  # 地域
    'secretID' : '**', # 腾讯云自己的secretID
    'secretKey' : '**', # 腾讯云自己的secretkey
    'method' : 'get'
}

parmas = {
    'cdbInstanceId' : '**', # 腾讯云自己的CDB的id
    'type' : 'coldbackup' # 类型冷备份
}


def download_qcloud():
    try:
        service = QcloudApi(module,config)

        # 请求前可以通过下面四个方法重新设置请求的secretId/secretKey/region/method参数
        secretId = '**'
        service.setSecretId(secretId)

        serviceKey = '**'
        service.setSecretKey(serviceKey)

        region = '**'
        service.setRegion(region)

        method = '**'
        service.setRequestMethod(method)

        # 生成请求的URL，不发起请求
        # print service.generateUrl(action,parmas)
        # 调用接口，发起请求
        # print service.call(action,parmas)
        s = service.call(action,parmas)
        result = json.loads(s)
        # print result.get("data")
        for i in result.get('data'):
            # print (i)
            pass
        # url_json =json.loads(i)
        # print i.get(u'out_url')

    except Exception,e:
        print 'exception:',e

    # 获取下载链接
    url = i.get(u'out_url')
    # r = requests.get(url)
    # with open("cdb155213_backup_%Y%m%d%H:%M:%S","wb") as cdb:
    #     cdb.write(r.content)
    print (url)

    # file_name = url.split('/')[-1]
    # 命名下载的文件并下载
    i = datetime.datetime.now()
    file_name = "cdb155213_backup_%s-%s-%s.sql" % (i.year,i.month,i.day)
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status
    print ("Download completed")
    f.close()
    if os.path.isfile(file_name) == True :
       try:
            os.system("sudo mysql -uroot mysql < %s " % file_name)
            print "还原成功！数据库密码更改为 '空' "
        except:
            print "不存备份文件或者已经损坏，亦或者数据库帐户或者密码错误！"    
        # 创建只读帐号
        # os.system("sudo mysql  -e 'CREATE USER focuscrm_r@localhost IDENTIFIED BY '1234qwer'' ")
        # os.system("sudo mysql  -e 'GRANT select on focuscrm.* TO focuscrm_r@localhost' ")
    else:
        print "不存在备份文件"
download_qcloud()
