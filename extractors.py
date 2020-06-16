from html.parser import HTMLParser

htmlparser = HTMLParser()


def get_title(item):
    #<span class="a-size-base-plus a-color-base a-text-normal" dir="auto">Wecando Foldable Pop-Up Mesh Laundry Hamper with Side Pocket Clothes Laundry Basket Storage Bag with Carry Handles for Dirty Clothes (2 Pack)</span>
    title = item.findAll('span', class_="a-size-base-plus a-color-base a-text-normal")
    title1 = item.findAll('span', class_="a-size-medium a-color-base a-text-normal")
    
    #print(title)
    titles = []
    if len(title) != 0:
        for obj in title:
            #print("----------------------------------")
            #print(obj.text)
            titles.append(obj.text)
        if titles:
            return titles
        else:
            #print("[Warning] missing product titles" )
            return None
    elif len(title1) != 0:
        for obj in title1:
            #print("----------------------------------")
            #print(obj.text)
            titles.append(obj.text)
        if titles:
            return titles
        else:
            #print("[Warning] missing product titles" )
            return None

def get_star(item):
    #<span class="a-icon-alt">2.9 out of 5 stars</span>
    rate = item.findAll('span', class_="a-icon-alt")
    #print(rate)
    rates  = []
    for obj in rate:
        if "out of" in obj.text:
            #print(obj.text)
            rates.append(obj.text)
    if rates:
        return rates
    else:
        #print("[Warning] missing product stars" )
        return None


def get_reviewnum(item):
    #<span class="a-size-base" dir="auto">102</span>
    review_num = item.findAll('span', class_="a-size-base")
    #print(review_num)
    
    review_nums = []
    for obj in review_num:
        if obj.text.isdigit():
            review_nums.append(obj.text)

    if review_nums:
        return review_nums
    else:
        print("[Warning] missing product reviewnums" )
        return None
    

def get_asin(item):
   # <div data-asin="B07BNZH5HV" data-index="0" class="sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32" data-cel-widget="search_result_0"><div class="sg-col-inner">
   #sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32
    #sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28
    #sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32
    #sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28
    #sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32

    asin = item.findAll("div", class_="sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32")
    asin1 = item.findAll("div", class_="sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28")
    asin2 = item.findAll("div", class_="sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32")
    asin3 = item.findAll("div", class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28")

    #print(len(asin))
    #print(asin)
    #print(asin[0]['data-asin'])
    #print(len(asin1))
    #print(asin1[0]['data-asin'])
    #asin = asin | asin1
    #print(asin[0])
    #print(asin)
    #print(asin1)
    #print(asin2)
    #print(asin3)
    if len(asin) != 0:
        #print("asin")
        asins = []
        for obj in asin:
            #print(obj['data-asin'])
            asins.append(obj['data-asin'])

        if asins:
            return asins
        else:
            #print("[Warning] missing product asins" )
            return None
    elif len(asin1) != 0:
        #print("asin1")
        asins = []
        for obj in asin1:
            #print(obj['data-asin'])
            asins.append(obj['data-asin'])

        if asins:
            return asins
        else:
            #print("[Warning] missing product asins" )
            return None
    elif len(asin2) != 0:
        #print("asin2")
        asins = []
        for obj in asin2:
            #print(obj['data-asin'])
            asins.append(obj['data-asin'])

        if asins:
            return asins
        else:
            #print("[Warning] missing product asins" )
            return None
    elif len(asin3) != 0:
        #print("asin1")
        asins = []
        for obj in asin3:
            #print(obj['data-asin'])
            asins.append(obj['data-asin'])

        if asins:
            return asins
        else:
            #print("[Warning] missing product asins" )
            return None
    else:
        print("wrong parser")      


