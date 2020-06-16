import os

current_dir = os.path.dirname(os.path.realpath(__file__))

# Database
database = "amazon_crawler"
host = "localhost:27017"
user = "admin"

# Redis
redis_host = ""
redis_port = 6379
redis_db = 0

# Request
"""
"Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
"""


headers = [{
    "User-Agent" : "",
    "Accept-Encoding":"gzip, deflate, br", 
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Language": "en-us",
    "DNT":"1",
    "Connection":"close", 
    "Upgrade-Insecure-Requests":"1"
    },{
    "User-Agent" : "",
    "Accept": "test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "br, gzip, deflate",
    "Accept-Language": "en-gb",
    
    "Referer": "http://amazon.com/"
    },{
    "User-Agent" : "",
    "Accept-Encoding":"gzip, deflate", 
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "DNT":"1",
    "Connection":"close", 
    "Upgrade-Insecure-Requests":"1"
    },{
    "User-Agent" : "",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language": "en-us",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests" : "1"
    },{
    "User-Agent" : "",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-us",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": ""
    }
    ]

cookies = {
"ad-id":  "A3qhkXZIrEJujA97NAXuN2c",
"ad-privacy":	"0",
"csm-hit":	"tb:s-C6GX6R49GBT8B8CB5XVA|1592192667930&t:1592192668576&adb:adblk_no",
"i18n-prefs":	"USD",
"session-id":	"138-1796179-3114535",
"session-id-time":	"2082787201l",
"session-token":	"Ww1hT/yluTx9H/ACRD4PiH6jLjAyOyFNEJXpLqaHKsbzg6Wok5yKhPHnTqVedSGw0/6rb7GidZgWHu/xTaYza3Wcylwjiwo/p77sBOn36XoF98l/9NfSn/z+Qn2OndFFU0vSWHhld2ENBtrhFR0eaF4a2aIGobp1ZvtcRl1Jm5tsLOGN/U7f4xm9THqRM5f9rrn+FEZy3JsY+FRfUXsJpMjWb9jnr/bWLhxEnJaa8dWwbBLIx88vBgS+wCw1QbKv",
"skin":	"noskin",
"ubid-main":	"130-7346853-6050008",
"x-wl-uid":	"178ta6PEw4v0j+hs8K3fahTuAl4ZsOSXS8gQdwNKp1GiZgFqESTiAKZvFK0tOhFKh7t3mA4IlBPM=
"   
}


allowed_params = ["node", "rh", "page"]

# Proxies
proxy_db_url = "http://localhost:3000/api/proxylist/index/"
proxy_num = 1475
proxies = [
    # your list of proxy IP addresses goes here
    # check out https://proxybonanza.com/?aff_id=629
    # for a quick, easy-to-use proxy service
]
proxy_user = ""
proxy_pass = ""
proxy_port = ""

#DB


# Crawling Logic
start_file = os.path.join(current_dir, "start-urls.txt")
config_file = os.path.join(current_dir, "start-config.txt")
detail_file = os.path.join(current_dir, "start-urls.txt")
max_requests = 8 * 10**6  # two million
max_details_per_listing = 9999

# Threads
max_threads = 1

# Logging & Storage
log_stdout = True
image_dir = "/tmp/crawl_images"
export_dir = "/tmp"
