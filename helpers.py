import os
import json
import random
from datetime import datetime
from urllib.parse import urlparse

import eventlet
requests = eventlet.import_patched('requests.__init__')
time = eventlet.import_patched('time')
import redis

#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

import settings

num_requests = 0

redis = redis.StrictRedis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
stack = []

def make_request(url, return_soup=True):
    # global request building and response handling

    url = format_url(url)

    if "picassoRedirect" in url:
        return None  # skip the redirect URLs

    global num_requests
    if num_requests >= settings.max_requests:
        raise Exception("Reached the max number of requests: {}".format(settings.max_requests))

    proxies = get_proxy()
    #print(proxies)

    if proxies != None:   
        try:
            print("url: {} proxies: {}".format(url, proxies))
            r = requests.get(url, headers=settings.headers, proxies=proxies)
            #r = requests.get(url, headers=settings.headers)
        except RequestException:
            #log("WARNING: Request for {} failed, trying again.".format(url))
            print("WARNING: Request for {} failed, trying again.".format(url))
            return make_request(url)  # try request again, recursively

        num_requests += 1
        
        if r.status_code != 200:
            os.system('say "Got non-200 Response"')
            print("WARNING: Got a {} status code for URL: {}".format(r.status_code, url))
            return None

        
        if return_soup:
            return BeautifulSoup(r.text, "lxml"), r.text
        return r


def format_url(url):
    # make sure URLs aren't relative, and strip unnecssary query args
    u = urlparse(url)

    scheme = u.scheme or "https"
    host = u.netloc or "www.amazon.com"
    path = u.path

    if not u.query:
        query = ""
    else:
        query = "?"
        for piece in u.query.split("&"):
            k, v = piece.split("=")
            if k in settings.allowed_params:
                query += "{k}={v}&".format(**locals())
        query = query[:-1]

    return "{scheme}://{host}{path}{query}".format(**locals())

"""
def log(msg):
    # global logging function
    if settings.log_stdout:
        try:
            print "{}: {}".format(datetime.now(), msg)
        except UnicodeEncodeError:
            pass  # squash logging errors in case of non-ascii text
"""

def get_proxy():
    proxy_url = settings.proxy_db_url + str(random.randint(1, settings.proxy_num))
    #print("proxy print")
    #print(proxy_url)
    
    try:
        r = requests.get(proxy_url)
    except RequestException:
        print("WARNING: Request for {} failed, trying again.".format(proxy_url))
        return make_request(proxy_url)  # try request again, recursively

    #print(r.text)
    json_data = json.loads(r.text)

    #formatting in sentence, think!
    """
    return {
        "http": "socks5://" + json_data['ip'] + ":" + json_data['port'],
        "https": json_data['ip'] + ":" + json_data['port']
    }
    """
    return {
        "http": "socks5://" + json_data['ip'] + ":" + json_data['port']
    }

def get_DB_product(obj):
    dbURL = 'http://localhost:3000/api/product_competitors/id/'+obj  

    try:
        r = requests.get(dbURL)
    except RequestException:
        #log("WARNING: Request for {} failed, trying again.".format(url))
        print("WARNING: Request for db insertion failed, trying again.")
        return get_DB_product(obj)  # try request again, recursively

    if r.status_code != 200:
        os.system('say "Got non-200 Response"')
        print("WARNING: Got a {} status code for get all".format(r.status_code))
        return None
    else:
        return r.json()
    return None

def trigger_slackmessage(obj):
    url = "https://slack.com/api/chat.postMessage"
    payload = "{ \"channel\": \"amazon-notification\",\"text\": \"" + obj+ "\"}"

    headers = {
    'Authorization': 'Bearer xoxb-1105318809761-1092953985539-uBqWaN5pnSY0N9G4vUtywR9n',
    'Content-Type': 'application/json'
    }

    try:
        r = requests.post(url, headers=headers, data=payload)
    except RequestException:
        #log("WARNING: Request for {} failed, trying again.".format(url))
        print("WARNING: Request for {} failed, trying again.".format(url))
        return trigger_slackmessage(url)  # try request again, recursively
    
    if r.status_code != 200:
        os.system('say "Got non-200 Response"')
        print("WARNING: Got a {} status code for URL: {}".format(r.status_code, url))
    else:
        print("slack message success with status code: {}".format(r.status_code))

def save_DB_detail(obj):
    dbURL = 'http://localhost:3000/api/product_competitors'
    #dbURL = 'http://ec2-52-87-191-124.compute-1.amazonaws.com:3000/api/tracking_list'
    
    try:
        r = requests.post(dbURL, data=obj)
    except RequestException:
        #log("WARNING: Request for {} failed, trying again.".format(url))
        print("WARNING: Request for db insertion failed, trying again.")
        return save_DB(obj)  # try request again, recursively

    if r.status_code != 200:
        os.system('say "Got non-200 Response"')
        print("WARNING: Got a {} status code for URL: {}".format(r.status_code, obj))
        return None
    else:
        print("insert success")
    return None

def update_DB_detail(asin, obj):
    dbURL = 'http://localhost:3000/api/product_competitors/update'
    
    try:
        r = requests.post(dbURL, data=obj)
    except RequestException:
        #log("WARNING: Request for {} failed, trying again.".format(url))
        print("WARNING: Request for db insertion failed, trying again.")
        return save_DB(obj)  # try request again, recursively

    if r.status_code != 200:
        os.system('say "Got non-200 Response"')
        print("WARNING: Got a {} status code for Obj: {}".format(r.status_code, obj))
        return None
    else:
        print("insert success")
    return None    


def save_DB(obj):
    dbURL = 'http://localhost:3000/api/product_map_competitors'
    #dbURL = 'http://ec2-52-87-191-124.compute-1.amazonaws.com:3000/api/product_map'
    
    #print(obj)
    try:
        r = requests.post(dbURL, data=obj)
    except RequestException:
        #log("WARNING: Request for {} failed, trying again.".format(url))
        print("WARNING: Request for db insertion failed, trying again.")
        return save_DB(obj)  # try request again, recursively

    if r.status_code != 200:
        os.system('say "Got non-200 Response"')
        print("WARNING: Got a {} status code for URL: {}".format(r.status_code, obj))
        return None
    #else:
    #    print("insert success: {}".format(obj['title']))
    return None

def get_category_info(completed_target):
    dbURL = "http://localhost:3000/api/productmap_config_competitors/completed/"+str(completed_target)
    #dbURL = "http://ec2-52-87-191-124.compute-1.amazonaws.com:3000/api/productmap_config/completed/"+str(completed_target)
    print(dbURL)
    try:
        r = requests.get(dbURL)
    except RequestException:
        #log("WARNING: Request for {} failed, trying again.".format(url))
        print("WARNING: Request for db insertion failed, trying again.")
        return get_category_info(completed_target)  # try request again, recursively

    if r.status_code != 200:
        os.system('say "Got non-200 Response"')
        print("WARNING: Got a {} status code for get all".format(r.status_code))
        return None
    else:
        print("get all list success")
        return r.json()
    return None



def enqueue_url(u):
    stack.append(u)
    


def dequeue_url():
    return stack.pop()

def clean_url():
    while len(stack) > 0:
        stack.pop()

def get_queue_length():
    #print(len(stack))
    return len(stack)

if __name__ == '__main__':
    # test proxy server IP masking
    r = make_request('https://api.ipify.org?format=json', return_soup=False)
    #print r.text