##HTML Scraping Tutorial


#pip install: pip install lxml and pip install requests.
from lxml import html
import requests

#page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
#tree = html.fromstring(page.content)

##<div title="buyer-name">Carson Busses</div>
##<span class="item-price">$29.95</span>

#This will create a list of buyers:
#buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
#prices = tree.xpath('//span[@class="item-price"]/text()')

#print 'Buyers: ', buyers
#print 'Prices: ', prices


##Experiment
Link=requests.get("http://www.themarker.com/technation/1.4296705")
tree = html.fromstring(Link.content)

textbody = tree.xpath("//section[@class='article__entry h-group']/p")

for i in range(len(textbody)):
    print textbody[i].text.encode('iso-8859-1')
