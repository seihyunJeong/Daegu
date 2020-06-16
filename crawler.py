import sys
import json
from datetime import datetime
import eventlet
import threading
import time

import settings
#from models import ProductRecord
from helpers import save_DB, save_DB_detail, dequeue_url, enqueue_url, clean_url, get_category_info, get_queue_length,get_DB_product,trigger_slackmessage,update_DB_detail
from helpers_config import make_request_cfg,  save_DB_cfg, dequeue_url_cfg, enqueue_url_cfg, get_queue_url_length, set_header_id, get_header_id, save_DB_completed
from extractors import get_title, get_star, get_reviewnum, get_asin
from extractors_cfg import get_pagenumber, get_pageunit, get_captcha
from extractors_detail import get_title_detail, get_price_detail, get_byLineInfo_detail, get_sellerNum_detail, get_salesRank_detail, get_avgRating_detail,get_ratingNum_detail,get_star5Ratio_detail,get_star4Ratio_detail,get_star3Ratio_detail,get_star2Ratio_detail,get_star1Ratio_detail,get_feature_detail


pool = eventlet.GreenPool(settings.max_threads)
pile = eventlet.GreenPile(pool)
def begin_crawl():
    print("pushing url info in to the stack")
    # explode out all of our category `start_urls` into subcategories
    completed_target = 0
    url = get_category_info(completed_target)
    print(len(url))

    #initialize queue
    if get_queue_length() > 0:
        clean_url()
    #print(url)

    for index in range(0, len(url)):
        #populate urls from page 1 to max
        if url[index]['completed'] == completed_target:
            new_url = {}
            #print(url[index])
            try:
                new_url['category1']    =  url[index]['category1']
                new_url['category2']    =  url[index]['category2']
                new_url['category3']    =  url[index]['category3']
                new_url['category4']    =  url[index]['category4']
                new_url['category5']    =  url[index]['category5']
                new_url['category6']    =  url[index]['category6']
                new_url['category7']    =  url[index]['category7']
                new_url['pageunit']     =  url[index]['pageunit']
                new_url['url']              =  url[index]['url']
            
                #print(url[index]['url'].split("page=")[1])
                if url[index]['url'].split("page=")[1] == "1":
                    new_url['url'] =  url[index]['url'].replace("?", "?bbn=1&dc&")
                    #print(new_url['url'])
            except:
                print(url[index])
            
            enqueue_url(new_url)    

    print(get_queue_length())
    set_header_id(0)
    print("completed url pushing")
"""        
    with open(settings.start_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # skip blank and commented out lines
            enqueue_url(line)
            #print(line)
    print("finsihed asin pushing")
"""            
def fetch_products():
    item = dequeue_url()
    print(item)
    
    page, html = make_request_cfg(item["url"])

    document = {}
    #print(page)
    if page != None:
        captcha = get_captcha(page)
        #print("--------------")
        if captcha != None:
            print("[Warning] caught by captcha!!! id: {}".format(get_header_id()) )
            enqueue_url(item)
            set_header_id( (get_header_id() + 1) % 6)
        if captcha == None:
            #print("no captch")
            # look for subcategory links on this page
            #print(item['url'])

            #print(page)
            asins = get_asin(page)
            #print(asins)
            #print(len(asins))

            titles = get_title(page)
            #print(titles)
            #print(len(titles))

            #stars = get_star(page)
            #print(stars)
            #print("----------------")
            #print(len(stars))
            #print("----------------")

            #reviewnums = get_reviewnum(page)
            #print(reviewnums)
            #print(len(reviewnums))
            if asins != None :
                if len(asins) != 0:
                    for index in range(0, len(asins)):
                        document = {}
                        document['asin'] = asins[index]
                        #document['title'] = titles[index]
                        document['title'] = ""
                        #document['star'] = stars[index]
                        #document['reviewnum'] = reviewnums[index]
                        document['category1'] = item['category1']
                        document['category2'] = item['category2']
                        document['category3'] = item['category3']
                        document['category4'] = item['category4']
                        document['category5'] = item['category5']
                        document['category6'] = item['category6']
                        document['category7'] = item['category7']
                        document['date'] = datetime.now()

                        print(document)
                        #print("inserting")
                        save_DB(document)
                    
                    #complete-> 1
                    prod = {}
                    prod['cat1'] = item['category1']
                    prod['cat2'] = item['category2']
                    prod['cat3'] = item['category3']
                    prod['cat4'] = item['category4']
                    prod['cat5'] = item['category5']
                    prod['cat6'] = item['category6']
                    prod['cat7'] = item['category7']
                    if item['url'].split("page=")[1] == "1":
                        prod['url'] = item['url'].replace("?bbn=1&dc&", "?")
                    else:
                        prod['url'] = item['url']
                    prod['completed'] = 1
                    #print("save complete as 1")
                    save_DB_completed(prod)
                else:
                    print("[Warning] missing product info1" )
                    prod = {}
                    prod['cat1'] = item['category1']
                    prod['cat2'] = item['category2']
                    prod['cat3'] = item['category3']
                    prod['cat4'] = item['category4']
                    prod['cat5'] = item['category5']
                    prod['cat6'] = item['category6']
                    prod['cat7'] = item['category7']
                    if item['url'].split("page=")[1] == "1":
                        prod['url'] = item['url'].replace("?bbn=1&dc&", "?")
                    else:
                        prod['url'] = item['url']
                    prod['completed'] = 1
                
                    save_DB_completed(prod)
            else:
                print(item)
                print("[Warning] missing product info2" )
                prod = {}
                prod['cat1'] = item['category1']
                prod['cat2'] = item['category2']
                prod['cat3'] = item['category3']
                prod['cat4'] = item['category4']
                prod['cat5'] = item['category5']
                prod['cat6'] = item['category6']
                prod['cat7'] = item['category7']
                if item['url'].split("page=")[1] == "1":
                    prod['url'] = item['url'].replace("?bbn=1&dc&", "?")
                else:
                    prod['url'] = item['url']
                prod['completed'] = 1
               
                save_DB_completed(prod)
def begin_crawl_detail():
    print("pushing asin in the stack")
    # explode out all of our category `start_urls` into subcategories
    with open(settings.detail_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # skip blank and commented out lines
            enqueue_url(line)
    
    print(get_queue_length())
    set_header_id(0)
    print("finished asin pushing")

def fetch_products_detail():
    asin = dequeue_url()
    url = 'https://www.amazon.com/dp/'+  asin
    print(url)

    DB_product = get_DB_product(asin)[0]
    
    item = {}
    item['code'] = DB_product['code']
    item['title'] = DB_product['title']
    item['price'] = DB_product['price']
    item['byLineInfo'] = DB_product['byLineInfo']
    item['sellerNum'] = DB_product['sellerNum']
    item['salesRank'] = DB_product['salesRank']
    item['avgRating'] = DB_product['avgRating']
    item['ratingNum'] = DB_product['ratingNum']
    
    page, html = make_request_cfg(url)

    product = {}
    if page == 503:
        return None
    elif page != None:
        
        captcha = get_captcha(page)
        #print(captcha)
        if captcha != None:
            print("[Warning] caught by captcha!!! id: {}".format(get_header_id()) )
            enqueue_url(asin)
            set_header_id( (get_header_id() + 1) % 6)
            #set_header_id( (get_header_id()) % 6)
        else:
            #output.write(str(page))
            #output.close()
            # look for subcategory links on this page
            title = get_title_detail(page)
            #print(title)

            price = get_price_detail(page)
            #print(price)
            
            byLineInfo = get_byLineInfo_detail(page)
            #print(byLineInfo)
            
            sellerNum = get_sellerNum_detail(page)
            #print(sellerNum)

            salesRank = get_salesRank_detail(page)
            #print(salesRank)

            avgRating = get_avgRating_detail(page)
            #print(avgRating)

            ratingNum = get_ratingNum_detail(page)
            #print(ratingNum)
            #print("----------------")


            product['code'] = asin
            product['title'] = title
            product['price'] = price
            product['byLineInfo'] = byLineInfo
            product['sellerNum'] = sellerNum
            product['salesRank'] = salesRank
            product['avgRating'] = avgRating
            product['ratingNum'] = ratingNum

            #print(item)
            #print("-----------------------vs-------------------------")
            #print(product)

            if item != product:
                #price change
                flag= 0

                message_price = ''
                message_salesRank = ''
                message_sellerNum = ''

                if item['price'] != product['price']:
                    print('price changed')
                    message_price = str(item['price']) + '-> ' + str(product['price']) + '\n'
                    flag=1
                #salesRank change
                if item['salesRank'] != product['salesRank']:
                    
                    if len(item['salesRank']) == 2 or len(item['salesRank']) == 4 or len(item['salesRank']) == 6:
                        # increased
                        cat = item['salesRank'][1]
                        previousRank = int(item['salesRank'][0].replace(",", ""))
                        currentRank = int(product['salesRank'][0].replace(",", ""))
                        sign = ''
                        threshold = 5
                        if previousRank != currentRank:
                            if previousRank < currentRank:
                                diff = currentRank - previousRank
                                diff_percentage = float(diff / previousRank * 100)
                                sign = '+'
                            #decreased
                            elif previousRank > currentRank:
                                diff = previousRank - currentRank
                                diff_percentage = float(diff / previousRank * 100)
                                sign = '-'
                            if diff_percentage > threshold and sign == '+':
                                diff_percentage = '%.2f' %  diff_percentage
                                message_salesRank += cat + ' (' + sign +  str(diff_percentage)  + '%, '+ sign  + str(diff) + ') ' + product['salesRank'][0] + '\n'
                                flag=1
                    if len(item['salesRank']) == 4 or len(item['salesRank']) == 6:
                        cat = item['salesRank'][3]
                        previousRank = int(item['salesRank'][2].replace(",", ""))
                        currentRank = int(product['salesRank'][2].replace(",", ""))
                        sign = ''
                        if previousRank != currentRank:
                            if previousRank < currentRank:
                                diff = currentRank - previousRank
                                diff_percentage = float(diff / previousRank)
                                sign = '+'
                            #decreased
                            elif previousRank > currentRank:
                                diff = previousRank - currentRank
                                diff_percentage = float(diff / previousRank)
                                sign = '-'
                            if diff_percentage > threshold and sign == '+':
                                diff_percentage = '%.2f' %  diff_percentage
                                message_salesRank += cat + ' (' + sign + str(diff_percentage)  + '%, '+ sign  + str(diff) + ') ' + product['salesRank'][2] + '\n'
                                flag=1
                    if len(item['salesRank']) == 6:
                        cat = item['salesRank'][5]
                        previousRank = int(item['salesRank'][4].replace(",", ""))
                        currentRank = int(product['salesRank'][4].replace(",", ""))
                        sign = ''
                        if previousRank != currentRank:
                            if previousRank < currentRank:
                                diff = currentRank - previousRank
                                diff_percentage = float(diff / previousRank)
                                sign = '+'
                            #decreased
                            elif previousRank > currentRank:
                                diff = previousRank - currentRank
                                diff_percentage = float(diff / previousRank)
                                sign = '-'
                            if diff_percentage > threshold and sign == '+':
                                diff_percentage = '%.2f' %  diff_percentage
                                message_salesRank += cat + ' (' + sign + str(diff)  + '%, '+ sign  + str(diff) + ') ' + product['salesRank'][4] + '\n'
                                flag=1
                    #print(message_salesRank)
                #seller number change
                if int(item['sellerNum']) != int(product['sellerNum']):
                    print('sellerNum changed')
                    message_sellerNum =  str(item['sellerNum']) + '-> ' + str(product['sellerNum'])+ '\n'
                    flag=1
                
                if flag == 1:
                    message = str(datetime.now()).split('.')[0]+ '\t' + 'https://amazon.com/dp/' + str(asin) + '\n'
                    if message_price != '':
                        message += 'price changed: ' + message_price
                    if message_salesRank != '':
                        message += 'sales rank changed:\n' + message_salesRank
                    if message_sellerNum != '':
                        message += 'seller number changed: ' +message_sellerNum
                    print(message)
                    #trigger_slackmessage(message)
                    update_DB_detail(asin, product)
            #if title != None:
                #save_DB_detail(product)
    
def test_slack():
    trigger_slackmessage("hello world from Zena")

if __name__ == '__main__':
    start_time = datetime.now()
    if len(sys.argv) > 1 and sys.argv[1] == "map":
        print("Seeding the URL frontier with subcategory URLs")
        begin_crawl()  # put a bunch of subcategory URLs into the queue
        print("Beginning crawl at {}".format(start_time))

        while get_queue_length() > 0:
            [pile.spawn(fetch_products) for _ in range(settings.max_threads)]
            pool.waitall()
            print(get_queue_length())
            if get_queue_length() <= 20:
                begin_crawl()

    if len(sys.argv) > 1 and sys.argv[1] == "slack":
        test_slack()
    """
    if len(sys.argv) > 1 and sys.argv[1] == "detail":
        print("Seeding the URL frontier with subcategory URLs")
        begin_crawl_detail()  # put a bunch of subcategory URLs into the queue
        print("Beginning crawl at {}".format(start_time))

        while get_queue_length() > 0:
            [pile.spawn(fetch_products_detail) for _ in range(settings.max_threads)]
            pool.waitall()
            print(get_queue_length())
    """
    if len(sys.argv) > 1 and sys.argv[1] == "detail":
        print("Seeding the URL frontier with subcategory URLs")
        begin_crawl_detail()  # put a bunch of subcategory URLs into the queue

        print("Beginning crawl at {}".format(start_time))

        flag = 1
        while 1:
            crawl_time = datetime.now()
            if flag == 1:
                [pile.spawn(fetch_products_detail) for _ in range(settings.max_threads)]
                #[pile.spawn(begin_crawl) for _ in range(settings.max_threads)]
                pool.waitall()
                print(get_queue_length())

            if get_queue_length() == 0 and flag == 1:
                flag = 0
            elif get_queue_length() == 0 and flag == 0:
                time_delta = (crawl_time-start_time).total_seconds()
                if time_delta > 3600*8:
                    flag = 1
                    start_time = datetime.now()
                    begin_crawl_detail()
