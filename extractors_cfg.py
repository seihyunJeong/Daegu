from html.parser import HTMLParser
import math

htmlparser = HTMLParser()


def get_pagenumber(item, url):
    #<div class="a-section a-spacing-small a-spacing-top-small">
    div = item.find('div', class_="a-section a-spacing-small a-spacing-top-small")
    if div != None:
        number =div.find('span')
        #print("number: {}".format(number))
        if number != None:
            number = number.text.split(" of ")[0].split("-")
            #print("2nd number: {}".format(number))
            #print(pagenumber.find('span').text.split(" of ")[0].split("-"))
            try:
                num1 = int(number[0].replace(",", ""))
                num2 = int(number[1].replace(",", ""))
                num3 = int(div.find('span').text.split(" of ")[1].split(" results ")[0].replace(",", "").replace("over ", ""))
                if num1 > num2:
                    pageUnit = num1 - 1
                else:
                    pageUnit = num2 - num1 + 1

                pageNumber = int(math.ceil(int(num3) / pageUnit))
            except:
                pageNumber = 1
                pageUnit = 24
                print("-----------------")
                print(number[0])
                print(url)
                print("-----------------")
        else:
            return 
        #print("pagernumber: {}, pageUnit: {}".format(pageNumber, pageUnit))
        if pageNumber:
            return pageNumber
        else:
            return 1
    else:
        return 1

def get_pageunit(item):
    #<div class="a-section a-spacing-small a-spacing-top-small">
    div = item.find('div', class_="a-section a-spacing-small a-spacing-top-small")
    if div != None:
        number =div.find('span')
        if number != None:
            try:
                number = number.text.split(" of ")[0].split("-")
                #print(pagenumber.find('span').text.split(" of ")[0].split("-"))
                num1 = int(number[0].replace(",", ""))
                num2 = int(number[1].replace(",", ""))

                if num1 > num2:
                    pageUnit = (num1 - 1) / 400
                else:
                    pageUnit = num2 - num1 + 1
            except:
                pageUnit = 24

            if pageUnit:
                if pageUnit < 24:
                    return 24
                else:
                    return pageUnit
            else:
                return 24
    else:
            return 24

def get_captcha(item):
    captcha = item.find("h4")
    #print("-----")
    #print(captcha.text)
    #f = open('sample.txt', mode='wt', encoding='utf-8')
    #f.write(str(item))
    #f.close
    if captcha:
        if captcha.text == "Enter the characters you see below":
            #print(captcha.text)
            return captcha.text
    else:
        return None
