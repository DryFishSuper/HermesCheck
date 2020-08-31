import json
import smtplib
import ssl

import certifi as certifi
import pandas as pd
import requests
from urllib3 import util, ProxyManager, PoolManager

proxy_file = "proxy_list_available.csv"


def get_all_proxies(file):
    res = pd.read_csv(file)
    proxies = []
    for index, proxy in res.iterrows():
        ip = proxy['ip']
        port = proxy['port']
        type = proxy['type']
        proxies.append((type, ip, port))
    return proxies


def get_proxy(proxies, count):
    # if count % (len(proxies) + 1) == len(proxies):
    #     return None
    # return proxies[count % (len(proxies) + 1)]
    return proxies[count % len(proxies)]


def send_email(fromEmail, password, toEmail):
    ssl._create_default_https_context = ssl._create_unverified_context
    with smtplib.SMTP_SSL("smtp.gmail.com", "405") as server:
        server.login(fromEmail, password)
        sender_email = fromEmail
        receiver_email = toEmail

        message = "Subject: Picotin Lock 18 bag (H056289CC18) in stock!\n" \
                  "\n Picotin in taurillon Clemence leather with gold lock closure (H056289CC18) is arrived." \
                  "\n Click https://bck.hermes.com/product-page?locale=us_en&productsku=H056289CC18 to buy!"

        server.sendmail(sender_email, receiver_email, message)


def check_ip(ip_info, port_info, type):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    check_url = "https://www.google.com"
    ip_url = ip_info + ':' + str(port_info)
    proxy_url = '%s://%s' % (type, ip_url)
    proxy = {type: proxy_url}
    try:
        response = requests.get(url=check_url, headers=headers, proxies=proxy, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def check_stock_proxy_manager(url, proxy=None, count=0):
    if proxy is None:
        manager = PoolManager(timeout=5,
                              cert_reqs='CERT_REQUIRED',
                              ca_certs=certifi.where())
    else:
        proxy_url = "%s://%s:%s" % (proxy[0], proxy[1], proxy[2])
        manager = ProxyManager(proxy_url,
                               timeout=5,
                               cert_reqs='CERT_REQUIRED',
                               ca_certs=certifi.where())
    headers = util.make_headers(accept_encoding='gzip, deflate',
                                keep_alive=True,
                                user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0")
    headers['Accept-Language'] = "en-US,en;q=0.5"
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    try:
        response = manager.request('GET',
                                   url,
                                   preload_content=False,
                                   headers=headers)
        content = json.loads(response.data)
        print("%s - Connect Success!" % count)
        return content['hasStock']
    except Exception as ex:
        print("%s - Connect Error!" % count)
        return False


def has_stock(url, count):
    return check_stock_proxy_manager(url, get_proxy(get_all_proxies(proxy_file), count), count)
