#!/usr/bin/env python3

import subprocess
import urllib
import json
import urllib.request
import sys
import http.cookiejar
import re
import time
import random

class Fetcher(object):
    def __init__(self):
        self.cookiejar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
        urllib.request.install_opener(self.opener)

    def fetch_url(self, url, filename=None):
        request = urllib.request.Request(url)
        request.add_header("User-Agent", "FreshFetcher 1.0")
        print("Loading", url)
        with urllib.request.urlopen(request) as response:
            content = response.read()
            #print(content)
            if filename is not None:
                open(filename, "wb").write(content)

            return content

zipcode = sys.argv[1]

fetcher = Fetcher()
content = fetcher.fetch_url("https://primenow.amazon.com", "/tmp/step0.html")
token = re.findall("offer-swapping-token=([^&]+)", content.decode('utf-8'))[0]
print("TOKEN:", token)
content = fetcher.fetch_url("https://primenow.amazon.com/onboard/check?postalCode=%s&offerSwappingToken=%s" % (zipcode, token), "/tmp/step2.html")
content_data = json.loads(content)
print(content_data["result"])
if content_data["action"] != "NAVIGATE":
    print("Unexpected action:", content_data["action"])
    sys.exit(1)

fetcher.fetch_url(content_data["url"], "/tmp/step3.html")

while True:
    content = fetcher.fetch_url("https://primenow.amazon.com/storefront?merchantId=A3AL0FVYY7M4WX&ref_=pn_gw_fs_1_A3AL0FVYY7M4WX", "/tmp/step4.html")
    match = re.findall("Delivery</div><div[^>]+> temporarily sold out", content.decode('utf-8'))
    if match:
        print("sold out", match)
    else:
        open("/tmp/succ.html", "wb").write(content)
        subprocess.check_call(["notify-send", "AVAILABLE", "AVAILABLE"])
    time.sleep(random.randint(1, 5))
