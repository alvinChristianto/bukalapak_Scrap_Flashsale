import sys
import time
import requests
import mysql.connector

from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from mysql.connector import Error
from mysql.connector import errorcode


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Initial:
	def __init__(self):
		pass

	def getUrl(self):
		f = open("docu/flashdeal.html", "r")
		contents = f.read()
		#url = 'https://www.bukalapak.com/flash-deal'
		#contents = requests.get(url)
		print(self.scrapDealText(contents))
		print(self.scrapTime(contents))
                
        #looping to get every item name, original price, discount price, left item 
		i = 0
		while True:
			try:
				print(self.scrapItem(contents, i))
				print(self.hargaNormal(contents, i))
				print(self.hargaReduce(contents, i))
				print(self.itemSisa(contents, i))
				i += 1
			except(IndexError):
				break
			print("\n\n\n")
		#print(self.scrapDealText(contents))

	def scrapBase1(self, contnt):
		self.contnt = contnt
		soup = BeautifulSoup(contnt, "html5lib")
		header = soup.find("body", {"class", "reskinned_page"})
		header1 = header.find("div", {"class", "c-outer-wrapper c-outer-wrapper--split flash_deal-c index-a js-layout layout"})
		#header1 = soup.find("div", {"class", "c-outer-wrapper c-outer-wrapper--split flash_deal-c index-a js-layout layout"})
		header2 = header1.contents[11]
		header3 = header2.contents[0]
		#header3 = header2.find("div", {"class", "c-new-header__content"})
		header4 = header3.find("div", {"class", "o-container o-container--responsive"})
		header5 = header4.find("div", {"class", "c-tab c-tab--inside"})
		header6 = header5.find("ul", {"class", "c-tab c-tab__nav o-layout"})
		headerli = header6.find("li", {"class", "c-tab__list c-tab__list--inside o-layout__item u-width-2of10 u-mrgn--0 is-active"})
		headerA = headerli.find("a", {"class", "c-tab__link u-align-center u-pad-bottom--2"})
		
		return headerA
        #scrap time flashdeal
	def scrapTime(self, contents):
		self.contents = contents
		headerTime = self.scrapBase1(self.contents).contents[2]
		return headerTime.text

        #scrap Text on flashDeal (header)
	def scrapDealText(self, contents):
		self.contents = contents
		headerDeal = self.scrapBase1(self.contents).contents[0]
		return headerDeal.text

	def scrapBase2(self, contnt):
		self.contnt = contnt
		soup = BeautifulSoup(self.contnt, "html5lib")
		header = soup.find("body", {"class", "reskinned_page"})
		header1 = header.find("div", {"class", "c-outer-wrapper c-outer-wrapper--split flash_deal-c index-a js-layout layout"})
		header2 = header1.contents[11]
		header3 = header2.contents[0]
		header4 = header3.find("div", {"class", "u-bg--sand"})
		header5 = header4.find("div", {"class", "o-container o-container--responsive u-pad-v--4"})
		header6 = header5.contents[4]
		header7 = header6.contents[2]
		return header7
        #scrap all item name and return item name
	def scrapItem(self, contents, cnt):
		self.contents = contents
		self.cnt = cnt
		header = self.scrapBase2(self.contents)
		
		header7a = header.contents[cnt]
		header9 = header7a.contents[0]
		header10 = header9.find("div", {"class", "c-card"})
		header11 = header10.find("div", {"class", "c-card__body"})

		#get text per columns
		header12 = header11.contents[0]
		
		return header12.text
	
        #scrap original price 
	def hargaNormal(self, contents, cnt):
		self.contents = contents
		self.cnt = cnt
		header = self.scrapBase2(self.contents)
		
		header7a = header.contents[cnt]
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
				#print('item %d = %s'%(i,header12.text))

		return header13a.text

        #scrap discount price
	def hargaReduce(self, contents, cnt):
		self.contents = contents
		self.cnt = cnt
		header = self.scrapBase2(self.contents)
		
		header7a = header.contents[cnt]
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
				#print('item %d = %s'%(i,header12.text))

		return header13b.text

        #scrap remain item left
	def itemSisa(self, contents, cnt):
		self.contents = contents
		self.cnt = cnt
		header = self.scrapBase2(self.contents)
		
		header7a = header.contents[cnt]
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
				#print('item %d = %s'%(i,header12.text))

		return header15a


#main 
temp = Initial()
print(temp.getUrl())
