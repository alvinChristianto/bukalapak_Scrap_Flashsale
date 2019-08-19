import sys
import time
import requests
import mysql.connector

from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from mysql.connector import Error
from mysql.connector import errorcode


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def initial():
    with open("docu/flashdeal.html") as fp:
        soup = BeautifulSoup(fp, "html5lib")
        
        header = soup.find("body", {"class", "reskinned_page"})
        header1 = header.find("div", {"class", "c-outer-wrapper c-outer-wrapper--split flash_deal-c index-a js-layout layout"})
        #header2 = header1.find("div", {"class", "jupiter"})
        header2 = header1.contents[11]
        header3 = header2.contents[0]
        header4 = header3.find("div", {"class", "o-container o-container--responsive"}) 
        header5 = header4.find("div", {"class", "c-tab c-tab--inside"})
        header6 = header5.find("ul", {"class", "c-tab c-tab__nav o-layout"})
        headerli = header6.find("li", {"class", "c-tab__list c-tab__list--inside o-layout__item u-width-2of10 u-mrgn--0 is-active"})
        headerA = headerli.find("a", {"class", "c-tab__link u-align-center u-pad-bottom--2"})
        headerTime = headerA.contents[2]
        print headerTime.text
 
##########
        headerContent = header3.find("div", {"class", "u-bg--sand"})
        headerContent1 = headerContent.find("div", {"class", "o-container o-container--responsive u-pad-v--4"})
        headerContent2 = headerContent1.contents[5]
        headerContent3 = headerContent2.contents[2]
        headerContent4 = headerContent3.contents[0]
       
        print headerContent4
        #headerContent4 = headerContent3.find("div", {"class", "o-layout__item u-width-2of10 u-mrgn-bottom--2"})
     

def initial2():
    with open("docu/flashdeal.html") as fp:
        soup = BeautifulSoup(fp, "html5lib")
        
        header = soup.find("body", {"class", "reskinned_page"})
        header1 = header.find("div", {"class", "c-outer-wrapper c-outer-wrapper--split flash_deal-c index-a js-layout layout"})
        #header2 = header1.find("div", {"class", "jupiter"})
        header2 = header1.contents[11]
        header3 = header2.contents[0]
        header4 = header3.find("div", {"class", "u-bg--sand"})
        header5 = header4.find("div", {"class", "o-container o-container--responsive u-pad-v--4"})
        header6 = header5.contents[4]
        header7 = header6.contents[2]
        #header7a = header7.contents[0]
        print header7 
        #header8 = header7a.contents[0] 
      
        
        print("\r\r\r")
        i = 0 
        while True:
            try:
                pass
                header7a = header7.contents[i]
                header9 = header7a.contents[0]   
                header10 = header9.find("div", {"class", "c-card"})
                header11 = header10.find("div", {"class", "c-card__body"})
               
                #get text per columns
                header12 = header11.contents[0]
                header13 = header11.contents[2]
                header14 = header11.contents[8]
                header15 = header11.contents[10]
                header15a = header15.text
                header15a = header15a.replace(" Tersisa", "")
                header13a = header13.find("span", {"class", "c-product-price__original u-mrgn-right--0"})
                header13b = header13.find("span", {"class", "c-product-price__reduced u-fg--red-brand"})
                print('item %d = %s'%(i,header12.text))
                print('harga original  '+header13a.text)
                print('harga reduced  '+header13b.text)
                print('sisa  '+header15a) 
                i += 1
            except(IndexError):
                break
            print("\n\n\n")
        #for looping
       
     
       
       



if __name__ == "__main__":
    print(initial2())



