import requests
import urllib

from requests.models import Response


def countbyte(chStr):
    total = 0
    for ch in chStr:
        if (ord(ch) <= 127 and ord(ch) >= 0) or ch == ' ':
            total += 1
        else :
            total += 2
    return total


# string为输出内容，bytelength即为对其后的长度，align为对其方式l为左对齐，r为右对齐，c为居中对其，symbol为对其时的填充符号
def myFormatPrint2(string=' ', bytelength=0, align='l', symbol=' '):
    string = string.replace(' ', '')
    total = countbyte(string)
    if(total >= bytelength):
        return string
    else:
        symbol = symbol.ljust(bytelength - total, symbol)
        if(align == 'l'):
            string = string + symbol
        else:
            string = symbol + string
    return string

# 访问url，获取内容
def fetchUrl(url, header):
    try:
        r: Response = requests.get(url, headers=header)
        r.raise_for_status()
        print(r.encoding)
        #print(r.url)
        return r.text
        # return r.text.replace(u'\xa0', u' ')
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error!")


def defDownload(url, filename):
    urllib.request.urlretrieve(url, filename)

