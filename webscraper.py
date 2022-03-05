#probably outdated

import smtplib
import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from io import open
from datetime import datetime
from datetime import date
from urllib3.exceptions import InsecureRequestWarning
import random 
import time
from fake_useragent import UserAgent
import sys

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ua = UserAgent()
filename = "a71prices.csv"

urlsouq = "https://egypt.souq.com/eg-en/samsung-galaxy-a71-dual-sim-128gb-8gb-ram-4g-lte-black-106860801/i/"
urljumia = "https://www.jumia.com.eg/samsung-galaxy-a71-6.7-inch-128gb8gb-dual-sim-4g-mobile-phone-prism-crush-black-16623197.html"
urlnoon = "https://www.noon.com/uae-ar/a71-8-128-4g-lte/N33635420A/p?o=c6808b95b85508bc"
urlamazon = "https://www.amazon.ae/dp/B083WNGJ6Q/ref=cm_sw_r_wa_apa_i_4.VyFbZQBQZ9X"
url = "https://transferwise.com/gb/currency-converter/aed-to-egp-rate"

#souq
def get_proxies() :
	import requests
	from bs4 import BeautifulSoup
	from fake_useragent import UserAgent
	ua = UserAgent()
	proxies = []
	o = 0
	while (o == 0):
		try:
			res = requests.get('https://free-proxy-list.net/', headers={'User-Agent': ua.random, "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}, verify=False)
		except:
			print("hdr didn't work")
		else:
			o = 1
	o = 0
	soup = BeautifulSoup(res.text,"lxml")
	for items in soup.select("#proxylisttable tbody tr"):
		proxy_list = [item.text for item in items.select("td")[:9]]
		if proxy_list[4] == "elite proxy" and proxy_list[6] == "yes" :
		    proxy_list = ':'.join(proxy_list[:2])
		    proxies.append(proxy_list)
	return(proxies)
i = 0
j=0
t=0
l = 0
x = get_proxies()
u = 6
while i == 0:
	if(j < u):	
		proxy_ip = x[t]
		proxies = {
	    	"http": 'http://{}'.format(proxy_ip), 
    		"https": 'http://{}'.format(proxy_ip)
		}
	else:
		x = get_proxies()
		t = 0
		j=0
		proxy_ip = x[t]
		proxies = {
	    	"http": 'http://{}'.format(proxy_ip), 
    		"https": 'http://{}'.format(proxy_ip)
		}
		
	print(proxies)
	try :
		hdr = {"User-Agent": ua.random, "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
		response = requests.get(urlsouq, headers=hdr, proxies=proxies, verify=False , timeout=5)
	except:
		t = t+1
		j = j+1
		i = 0
	else:
		j = 0
		i = 1
		t = 0
		print("done")
i = 0


page_html = response.content

#soup works
page_soup = soup(page_html, "html.parser")


#souqprice
pricesouq = page_soup.find("h3",{"class" : "price is sk-clr1"})

price_txtsouq = pricesouq.text.strip().replace("\n" , "").replace("\t" , "").replace(",",".").replace("جنيه" , "").replace("Â EGP","").replace(" EGP","").replace("\xa0EGP","").replace(".","",1)
print(price_txtsouq)
print(float(price_txtsouq))
price_txtsouq = float(price_txtsouq)



#bug is a problem in code it could be in the logic or in the syntax or in the main library and most likly in the version
#like the case with selenium here the webdriver version isn't compatible
#currency
driver = webdriver.Chrome()
driver.get(url)
page_htmlcurrency = driver.page_source
driver.close()

page_soupcurrency = soup(page_htmlcurrency, "html.parser")

print("done")

AEDtoEGP = page_soupcurrency.find("span",{"class" : "text-success"})
currency = float(AEDtoEGP.text)
print(currency)

#jumia
driver = webdriver.Chrome()
driver.get(urljumia)
time.sleep(3)

page_htmljumia = driver.page_source
driver.close()

#soup works
page_soupjumia = soup(page_htmljumia, "html.parser")

pricejumia = page_soupjumia.find("span",{"dir" : "ltr"},{"class" : "-b -ltr -tal -fs24"})
try:
	price_txtjumia = str(pricejumia.text).replace(",","").replace(" ","").replace("حنيه","").replace("EGP", "")
	print(price_txtjumia)
	priceintjumia = int(price_txtjumia)
except:
	pass
else:
	pass


#.replace(",","").replace(" ","").replace("جنيه","").replace("EGP", "")

try:
	sale_perjumia = page_soupjumia.find("span", {"class": "tag _dsct _dyn -mls"}).text
	priceintjumia = int(str(slae_per).replace("%", ""))
	price_beforejumia = priceintjumia + (priceintjumia * (priceintjumia/100))
except:
	pass
else:
	pass
#except:
#	l = 0
#else:
#	l=1


#noon
driver = webdriver.Chrome()
driver.get(urlnoon)
time.sleep(3)
page_htmlnoon = driver.page_source
driver.close()
page_soupnoon = soup(page_htmlnoon, "html.parser")
print("done")

try:
	pricenoon = page_soupnoon.find("span",{"class" : "value"})
	price_txtnoon = str(pricenoon.text).replace(" د.إ.\u200f(شاملاً ضريبة القيمة المضافة)","")
	priceintnoon = float(price_txtnoon)

	priceintegpnoon = priceintnoon * currency
except:
	pass
else:
	pass

#amazon
driver = webdriver.Chrome()
driver.get(urlamazon)
time.sleep(3)

page_htmlamazon = driver.page_source
driver.close()

#soup works
page_soupamazon = soup(page_htmlamazon, "html.parser")
print("done")
try:
	priceamazon = page_soupamazon.find("span",{"id" : "priceblock_ourprice"},{"class" : "a-size-medium a-color-price priceBlockBuyingPriceString"})

	price_txtamazon = str(priceamazon.text).replace(",","").replace(" ","").replace("حنيه","").replace("EGP", "").replace("$", "").replace("AED&nbsp;","").replace("AED\xa0","")
	price_floatamazon = float(price_txtamazon)

	priceintegpamazon = price_floatamazon * currency
except:
	pass
else:
	pass
#sending email
gmail_user = 'gmailusername'
gmail_password = 'gmailpassword'
sent_from = gmail_user
to = ['from', 'to']
subject = 'today prices'
if bool(l) :
	body = f"""\
	Hi sir prices bot wishes you a good day
	- souq : price: {price_txtsouq} [free shipping]
	- jumia :  price: {"contact developer for information"} [free shipping] , price before: {"contact developer for information"} sale percentage:{"contact developer for information"}
	- noon :  price:{"contact developer for information"} [free shipping]
	- amazon : price:{"contact developer for information"} [free shipping]
	"""
else:
	body = f"""\
	Hi sir prices bot wishes you a good day
	- souq : price: {price_txtsouq} [free shipping]
	- jumia :  price: {"contact developer for information"} [free shipping]
	- noon :  price:{"contact developer for information"} [free shipping]
	- amazon : price:{"contact developer for information"} [free shipping]

	!this bot can't recive gmails!
	"""
email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)
print(body)

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
server.sendmail(sent_from, to, email_text)
server.close()
print("sth went wrong...")
print("email sent!")
