# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from lxml import etree
from CommonClass import *
from web_browser import *
import re


# 爬取腾讯企业邮箱
def getQQMailInfo():
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Cookie' : ''
    }
    nextPage = 'https://exmail.qq.com/cgi-bin/mail_list?sid=GakMxEIWM1OXe1YJ,7&folderid=3&page=0&topmails=0&loc=folderlist,,,3'
    while nextPage != "":
        htmlText = fetchUrl(nextPage, headers)
        # 解析html
        html = etree.HTML(htmlText)

        # 邮件发件人，标题，时间
        sendUser = html.xpath('//*[@class="tl tf"]/nobr')
        title = html.xpath('//*[@class="gt tf"]//*[@class="black "]')
        sendTime = html.xpath('//*[@class="dt"]/div')

        # 下一页
        nextEle = html.xpath('//*[@id="nextpage"]')
        if(len(nextEle) > 0):
            nextPage = "https://exmail.qq.com" + nextEle[0].attrib['href']
        else:
            nextPage = ""

        for index in range(len(sendUser)):
            if(index < len(title) and index < len(sendTime)):
                print(myFormatPrint2(sendUser[index].text, 30), myFormatPrint2(title[index].text, 100), myFormatPrint2(sendTime[index].text, 10))
        print("End")


# 爬取腾讯企业邮箱具体内容
def getQQMailDetailInfo():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Cookie' : ''
    }
    url = 'https://exmail.qq.com/cgi-bin/readmail?folderid=3&t=readmail&mailid=ZC1127-61tPvDrrQCDgQm8wSjQAOan&mode=pre&maxage=3600&base=20.0210&ver=15556&sid=GakMxEIWM1OXe1YJ,7'

    try:
        file = open('mailDetail.txt', 'w',encoding='UTF-8')
        while url != '':
            htmlText = fetchUrl(url, headers)
            # 解析html
            html = etree.HTML(htmlText)

            title = html.xpath('//*[@class="sub_title s0"]//text()')
            mailTxt = html.xpath('//*[@id="mailContentContainer"]//text()')

            if len(title) > 0 and len(mailTxt) > 0:
                file.writelines(title[0] + '\n')
                print(title[0])
                if re.search(r'^ 【健診】桂林作業進捗報告_202011', title[0]):
                    for str in mailTxt:
                        file.writelines(str + '\n')
            file.writelines("=========================================================================================")

            #获取下一封邮件的id
            nextId = html.xpath('//*[@mailid]')
            try:
                if len(nextId) > 0:
                    url = 'https://exmail.qq.com/cgi-bin/readmail?folderid=3&t=readmail&mailid=' + nextId[0].attrib['mailid'] + '&mode=pre&maxage=3600&base=20.0210&ver=10000&sid=GakMxEIWM1OXe1YJ,7'
                else:
                    url = ''
            except Exception as error:
                url = ''
                print(error)
    except Exception as error:
        print(error)
    file.close()

# 爬京东商品信息
def getJDGoodsInfo():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Cookie':'__jdu=2015812710; shshshfpa=26c5ceff-0fa4-08d2-d1b6-0d21ffb2db91-1590458995; shshshfpb=g2qq65MXuJtZr3vt3ZdCN1g%3D%3D; qrsc=3; unpl=V2_ZzNtbRcDERd3WBYAfEwIBWJTElhKU0YXfABEUXJKWlA0UxNZclRCFnQURlVnGl8UZwYZX0RcRxdFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHgYXAFuAxFbQlZzJXI4dmR5GF4HbzMTbUNnAUEpD0dVexBVSGQCEllLV0ATdQl2VUsa; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_dec33aae6de14a14954389348b7dba05|1603348673309; areaId=20; ipLoc-djd=20-1726-22885-0; __jda=122270672.2015812710.1587021704.1600052416.1603348673.17; __jdc=122270672; shshshfp=3251172e0a1cc04f1b307dba3c275da9; rkv=1.0; 3AB9D23F7A4B3C9B=URMP4LEGN3ALKQ72EYRQQ26CDB6PN34O5MCK3XN4WC7EH74SZ3O7C73JM2OIFSNZCQ4SPVAHRBJG4Y3I6CL6GBYSFQ; __jdb=122270672.4.2015812710|17.1603348673; shshshsID=f108f3bb73164816ee17d9dcb5ceecba_4_1603348732813'
    }
    nextPage = 'https://search.jd.com/Search?keyword=3080&wq=3080&page=1&s=1&click=0'
    while nextPage != "":
        htmlText = fetchUrl(nextPage, headers)
        # 解析html
        html = etree.HTML(htmlText)

        # 商品图片 价格 店铺
        goodsList = html.xpath('//*[@class="gl-i-wrap"]')
        for goods in goodsList:
            # 图片
            img = goods.xpath('.//img')
            if(len(img) > 0):
                imgurl = "https:" + str(img[0].attrib["data-lazy-img"])
            # 价格
            p = goods.xpath('.//*[@class="p-price"]/strong/i/text()')
            if(len(p) > 0):
                price = p[0]
            # 名字
            nstr = goods.xpath('.//em/text()')
            if(len(nstr) > 0):
                name = ",".join(nstr)
            # 店铺
            ss = goods.xpath('.//*[@class="curr-shop hd-shopname"]/text()')
            if(len(ss) > 0):
                shop = ss[0]

            print("===============================================================================")
            print("商品名：" + name)
            print("价格：" + price)
            print("店铺：" + shop)
            print("图片地址：" + imgurl)
            print("===============================================================================")
            print("                                                                               ")
            print("                                                                               ")
            nextPage = ""

if __name__=='__main__':
    getQQMailDetailInfo()


