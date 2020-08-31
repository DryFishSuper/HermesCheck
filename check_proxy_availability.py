import json
import urllib.request

import certifi
import pandas as pd
import requests
import urllib3.contrib.pyopenssl
from bs4 import BeautifulSoup
from urllib3 import ProxyManager, util

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}
urllib3.contrib.pyopenssl.inject_into_urllib3()


def get_ip(page):
    url = "http://free-proxy.cz/zh/proxylist/country/US/http/ping/all/%s" % page
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
    response = requests.get(url,
                            timeout=10,
                            headers=headers,
                            cert_reqs='CERT_REQUIRED',
                            ca_certs=certifi.where())
    print("Getting IPs from %s" % url)
    print(response.status_code)
    page = urllib.request.urlopen(url)
    content = BeautifulSoup(page, 'html.parser')
    print(content)


def check_ip(ip_info, port_info, type):
    check_url = "https://bck.hermes.com/product-page?locale=us_en&productsku=H056289CC18"
    ip_url = "%s://%s:%s" % (type, ip_info, port_info)
    manager = ProxyManager(ip_url,
                           timeout=10,
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
                                   check_url,
                                   preload_content=False,
                                   headers=headers)
        res = response.data
        print(res)
        json.loads(res)
        return True
    except Exception as ex:
        return False


def get_all_proxies(file):
    proxies = pd.read_csv(file)
    ips = []
    ports = []
    types = []
    for id, proxy in proxies.iterrows():
        ip = proxy["ip"]
        port = proxy["port"]
        print("check %s://%s:%s" % ("https", ip, port))
        if check_ip(ip, port, "https"):
            ips.append(ip)
            ports.append(port)
            types.append("https")
            print("%s://%s:%s works" % ("https", ip, port))
    res = pd.DataFrame({'ip': ips, 'port': ports, 'type': types})
    res.to_csv("proxy_list_available.csv", index=False, sep=',')


get_all_proxies('proxy_list.csv')