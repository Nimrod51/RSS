# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import pdb
import sys

try:
    from builtins import input
except ImportError:
    print("Error: Future not installed\nInstall using: pip install future")
    exit()
try:
    import feedparser
except ImportError:
    print("Error: FeedParser not installed\nInstall using: pip install feedparser")
    exit()
try:
    from yattag import Doc, indent
except ImportError:
    print("Error: yattag not installed\nInstall using: pip install yattag")
    exit()
try:
    from lxml import html
except ImportError:
    print("Error: lxml not installed\nInstall using: pip install lxml")
    exit()
try:
    import requests
except ImportError:
    print("Error: requests not installed\nInstall using: pip install requests")
    exit()

rss = input("""Enter your preferred feed:
1 - כל פרשנויות היום
2 - כל כותרות היום
3 - כותרות דף הבית
""")

if rss=="1":
    themarker = "http://www.themarker.com/cmlink/1.146"
elif rss=="2":
    themarker = "http://www.themarker.com/cmlink/1.144"
else:
    themarker = "http://www.themarker.com/cmlink/1.145"

# print(themarker)

d = feedparser.parse(themarker)

# Title of Service
# print(d['feed']['title'])

##Basic HTML template
doc,tag,text= Doc().tagtext()
doc.asis('<DOCTYPE html>')


article_text=''

##Loop to create HTML
with tag ('html', dir = "rtl"):
    with tag ('body'):
        with tag ('h1', style= "font-family:sans-serif;"):
            text (d.feed.title) ##Main title for RSS
        for item in range (len(d.entries)): ##Loop over articles in RSS feed
            with tag ('h2', style= "font-family:sans-serif;"): #Article title
                with tag ('a', href=d.entries[item].link): #Add link
                    text (d.entries[item].title)
            with tag ('p', style= "font-family:sans-serif; font-weight:bold;"): ##Article description
                text (d.entries[item].description)
            with tag('div', id='photo-container'): #Get picture
                links=dict(d.entries[item])
                imageLink=str(links['links'][1]['href'])
                doc.stag('img', src=imageLink, width="150px", klass="photo") #Input pic in html
            with tag ('p', style = 'font-family:sans-serif;'): #Article text
                page=requests.get(d.entries[item].link)
                tree = html.fromstring(page.content)
                textbody = tree.xpath("//section[@class='article__entry h-group']/p[@class='t-body-text']") ##//section[@class='article__entry h-group']/p/child::text()
                for item in textbody:
                    if sys.version_info[0]<3:
                        raw_text="{0}".format(item.text_content().encode('iso-8859-1','replace'))
                        utf_text = raw_text.decode('UTF-8', 'ignore')
                        text(utf_text)
                        doc.stag('br') #Add linebreaks between paragraphs
                        doc.stag('br')
                        #pdb.set_tracerace()
                    else:
                        raw_text=item.text_content().encode('iso-8859-1','replace')
                        utf_text=raw_text.decode('UTF-8', 'ignore')
                        text(utf_text)
                        doc.stag('br') #Add linebreaks between paragraphs
                        doc.stag('br')
                        #pdb.set_tracerace()


html_str=doc.getvalue().encode('UTF-8', 'ignore')

Html_file= open("TheMarker.html","wb")
Html_file.write(html_str)
Html_file.close()


os.startfile(Html_file.name, 'open')

# print("DONE")
