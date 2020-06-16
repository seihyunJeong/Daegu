from html.parser import HTMLParser

htmlparser = HTMLParser()


def get_title_detail(item):
    title = item.find('span', id="productTitle")
    
    if title:
        return title.text.strip()
    else:
        return None

def get_price_detail(item):
   # <span id="priceblock_ourprice" class="a-size-medium a-color-price priceBlockBuyingPriceString">$9.59</span>
    price1 = item.find("span", id="priceblock_ourprice")
    price2 = item.find("span", id="priceblock_saleprice")
    price3 = item.find("span", id="priceblock_pospromoprice")
    price4 = item.find('span', class_='a-color-price')
    price5 = item.findAll("span",  class_='a-size-mediufm a-color-price')
    #print(price)
       
    if price1:
        #print("1: {}".format(price1.text))
        return price1.text.replace(" ", "").replace("\n", "").replace("\t", "")
    if price2:
        #print("2: {}".format(price2.text))
        return price2.text.replace(" ", "").replace("\n", "").replace("\t", "")        
    if price3:
        #print("3: {}".format(price3.text))
        return price3.text.replace(" ", "").replace("\n", "").replace("\t", "")
    if price4:
        #print("4: {}".format(price4.text.replace(" ", "").replace("\n", "").replace("\t", "")))
        return price4.text.replace(" ", "").replace("\n", "").replace("\t", "")
    if price5:
        #print("5: {}".format(price5[0].text))
        return price5.text     .replace(" ", "").replace("\n", "").replace("\t", "")   
    return None

def get_byLineInfo_detail(item):
    #byLineInfo = item.find('a', id="byLineInfo") or item.find('img', id="logoByLine") or item.find('a', id="brand")
    byLineInfo1 = item.find('a', id="bylineInfo")
    #byLineInfo1 = item.find('a', class_="a-link-normal")
    byLineInfo2 = item.find('img', id="logoByLine", alt=True)
    byLineInfo3 = item.find('a', id="brand")
    #print(byLineInfo1)
    #print(byLineInfo2)
    #print(byLineInfo3)
    
    if byLineInfo1 != None:
        #print('1: ', byLineInfo1)    
        return byLineInfo1.text
    if byLineInfo2  != None:
        #print('2: ',byLineInfo2['alt'])
        return byLineInfo2['alt']
    if byLineInfo3  != None:
        #print('3: ',byLineInfo3)
        return byLineInfo3.text

    return None

def get_sellerNum_detail(item):
    defaultSellerNum = 1
    sellerNum = item.find('span', class_="olp-padding-right")
    #print("here")
    #print(sellerNum)
    if sellerNum:
        return sellerNum.select('a')[0].text.split('\xa0')[0]
    return defaultSellerNum

def get_salesRank_detail(item):
    
    salesRank1 = item.find('li', id="SalesRank")
    salesRank2 = item.find('table', id="productDetails_detailBullets_sections1")
    salesRank3  = item.find('tr', id="SalesRank")
    
    #print("here")
    
    #print("------------------------------------------------------------------")
    
    #print(category.text)
    category = salesRank1
    if salesRank1 != None:
        category = salesRank1.text.split(" (See Top")[0].split("#")[1].split(" in ")
        #subCategory = []
        sub_rank = item.find('span', class_='zg_hrsr_rank')
        sub_category = item.find('span', class_='zg_hrsr_ladder')
        if sub_rank:
            category.append( sub_rank.text.split('#')[1] )
        if sub_category:
            category.append( sub_category.select('a')[0].text )

    flag = 0
    if salesRank2 != None:
        category = []
        try:
            categories = salesRank2.text.split("Best Sellers Rank")[1].split("#")
        except:
            #print(salesRank2.text)
            flag = 1

        #print(categories)
        if flag == 0:
            for cat in categories:
                cat = cat.strip()
                #print(cat)
                #print(len(cat))
                if len(cat) > 0:
                    cat = cat.split("(")[0].strip()
                    cat = cat.split(" in ")
                    if cat[1].find("\n\n") > 0:
                        cat[1] = cat[1].split("\n\n")[0]
                        #print("error")
                    #print(cat)
                    category.append(cat[0])
                    category.append(cat[1])
        
        """
        category = salesRank2.text.split("Best Sellers Rank")[1].split("(")[0].split(" in ")
        #category[0] = category[0].replace("\n", "").replace(" ", "").replace("#", "")
        sub_category = salesRank2.text.split("Best Sellers Rank")[1].split(")")[1].split("\n\n\n")[0].strip()
        category[0] = category[0].strip().replace("#", "")
        category[1] = category[1].strip()
        print(sub_category)
        sub_category =sub_category.split(" in ")
        sub_category[0] = sub_category[0].strip().replace("#", "")
        sub_category[1] = sub_category[1].strip()
        category.append(sub_category[0])
        category.append(sub_category[1])
        #category.append(salesRank2.text.split("Best Sellers Rank")[1].split("(See Top 100 in Beauty & Personal Care)")[1].trim())
        #print(salesRank2.text.split("Best Sellers Rank")[1].split("(See Top 100 in Beauty & Personal Care)"))
        #print(salesRank2.findAll('tr'))
        """
    if salesRank3 != None:
        category = salesRank3.text.split("<td class=\"value\">")[0].split("(")[0].split("#")[1].split(" in ")
        #print(salesRank3.text.split("<td class=\"value\">")[0].split("("))
        sub_category = salesRank3.text.split("<td class=\"value\">")[0].split("#")
        #print(len(sub_category))
        sub_category = sub_category[len(sub_category)-1].replace("\n", " ").split("in")
        sub_category[0] = sub_category[0].strip()
        sub_category[1] = sub_category[1].strip()
        category.append(sub_category[0])
        category.append(sub_category[1])
        #print(sub_category)
        
    #print(category)
    if category:
        return category
    return ['']

"""
    avgRating : String,
    ratingNum : String,
    star5Ratio : String,
    star4Ratio : String,
    star3Ratio : String,
    star2Ratio : String,
    star1Ratio : String,
"""
def get_avgRating_detail(item):
    avgRating = item.find('div', class_="a-fixed-left-grid-col aok-align-center a-col-right")
    
    if avgRating:
        return avgRating.text.strip()
    else:
        return ''
def get_ratingNum_detail(item):
    ratingNum1 = item.find('span', class_="a-size-base a-color-secondary")
    ratingNum2 = item.find('span', id="acrCustomerReviewText")
    if ratingNum2:
        #print(ratingNum2.text)
        return ratingNum2.text.split(" ratings")[0].replace(",", "").strip()
    elif ratingNum1:
        #print(ratingNum1.text)
        return ratingNum1.text.split("  customer")[0].replace(",", "").strip()
    
    else:
        return None
def get_star5Ratio_detail(item):
    table = item.find('table', id="histogramTable")
    star5Ratio = table.text.split("4 star")[0].split("5 star")[1].strip()
    #print(subtable)

    if star5Ratio:
        #0% case
        if len(star5Ratio) > 5:
            star5Ratio = star5Ratio.split(")")[1].strip()
        return star5Ratio
    else:
        return None
def get_star4Ratio_detail(item):
    table = item.find('table', id="histogramTable")
    star4Ratio = table.text.split("3 star")[0].split("4 star")[1].strip()
    #print(subtable)

    if star4Ratio:
        #0% case
        if len(star4Ratio) > 5:
            star4Ratio = star4Ratio.split(")")[1].strip()
        return star4Ratio
    else:
        return None
def get_star3Ratio_detail(item):
    table = item.find('table', id="histogramTable")
    star3Ratio = table.text.split("2 star")[0].split("3 star")[1].strip()
    #print(subtable)

    if star3Ratio:
        #0% case
        if len(star3Ratio) > 5:
            star3Ratio = star3Ratio.split(")")[1].strip()
        return star3Ratio
    else:
        return None
def get_star2Ratio_detail(item):
    table = item.find('table', id="histogramTable")
    star2Ratio = table.text.split("1 star")[0].split("2 star")[1].strip()
    #print(subtable)

    if star2Ratio:
        #0% case
        if len(star2Ratio) > 5:
            star2Ratio = star2Ratio.split(")")[1].strip()
        return star2Ratio
    else:
        return None                 
def get_star1Ratio_detail(item):
    table = item.find('table', id="histogramTable")
    star1Ratio = table.text.split("1 star")[1].strip()
    #print(subtable)
    
    if star1Ratio:
        if len(star1Ratio) > 5:
            star1Ratio = star1Ratio.split(")")[1].strip()
        return star1Ratio
    else:
        return None                           
def get_feature_detail(item):
    div = item.find('span',  class_="cr-widget-SummaryAttribute")
    print("----------")
    print(div)

    return None
    #star1Ratio = table.text.split("1 star")[1].strip()
    #print(subtable)
    
#    if star1Ratio:
#        if len(star1Ratio) > 5:
#            star1Ratio = star1Ratio.split(")")[1].strip()
#        return star1Ratio
#    else:
#        return None                           

"""
def get_url(item):
    link = item.find("a", "s-access-detail-page")
    if link:
        return link["href"]
    else:
        return "<missing product url>"
"""
"""
def get_primary_img(item):
    thumb = item.find("img", "s-access-image")
    if thumb:
        src = thumb["src"]

        p1 = src.split("/")
        p2 = p1[-1].split(".")

        base = p2[0]
        ext = p2[-1]

        return "/".join(p1[:-1]) + "/" + base + "." + ext

    return None
    """