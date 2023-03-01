from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import time, sleep
import requests
import re
import logging

#设置浏览器头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "www.baidu.com",
    "Cookie": "BIDUPSID=E2985B2B067F67E0D450BBAE34BA9; PSTM=1672821191; BD_UPN=1214753; newlogin=1; BAIDUID=9D2F961A0CA1174C6993A97D398:SL=0:NR=10:FG=1; ispeed_lsm=0; MCITY=-218%3A; BDUSS_BFESS=kp-Wml3OVJLNWtFLTNhV2JhN2lWanNRSjZlQWU2V05heE0yRng0cFN1dTRyaDVrSUFBQUFBJCQAAAAAAAAAAAEAAAC7Hz4DcGxtd29ybGQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALgh92O4Ifdje; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=9D2F961A0E93C2CA1174C6993A97D398:SL=0:NR=10:FG=1; BA_HECTOR=0h25ag84058h2h01al0424tt1hvrfcl1l; ZFY=aJhpeBQhkPNWNpYsRptAqS959kwchy2K9pODSSPLR3A:C; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BD_CK_SAM=1; PSINO=7; delPer=0; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_PSSID=38189_36547_38271_37910_38149_38265_38172_38245_36803_37921_37900_26350_38282_37881; H_PS_645EC=4ecbTB%2BNxKMvhUIHGbDPJCxdUaIaXJ2X9hV1Lw3jWU5OWA44dGl8ndjP2dUtXDVZb28D; BDSVRTM=165"
}

#记录结果
logging.basicConfig(level=logging.ERROR,
                    filename='new.log',
                    filemode='a',
                    format='%(message)s'
                    )


def get_real_url(v_url):
    """
    获取百度链接真实地址
    :param v_url: 百度链接地址
    :return: 真实地址
    """
    r = requests.get(v_url, headers=headers, allow_redirects=False)  # 不允许重定向
    if r.status_code == 302:  # 如果返回302，就从响应头获取真实地址
        real_url = r.headers.get('Location')
    else:  # 否则从返回内容中用正则表达式提取出来真实地址
        real_url = re.findall("URL='(.*?)'", r.text)[0]
    return real_url



def getDeadLink():
    """
    获取页面中的链接并转换为真实链接
    """
    try:
        urls = driver.find_elements(By.XPATH, "//a[@data-showurl-highlight]")
        for url in urls:
            href = url.get_attribute("href")
            real = get_real_url(href)
            print(url.text+"    "+real)
            logging.error(url.text+"    "+real)
    except NoSuchElementException:
        print("ERROR NoSuchElement")
        pass


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
# s = Service("F:\py\chromedriver.exe")  # 驱动path，新版似乎不需要驱动
# driver = webdriver.Chrome(service=s, options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.baidu.com/")

search = driver.find_element(By.ID, "kw") #定位关键词输入框
search.send_keys("佳能") #输入关键词

maxpage = 20 #最大抓取页面数

for i in range(maxpage):
    try:
        send_button = driver.find_element(By.PARTIAL_LINK_TEXT, "下一页 >")
        send_button.click()
    except NoSuchElementException:
        send_button = driver.find_element(By.ID, "su")
        send_button.click()

    sleep(5)
    getDeadLink()
