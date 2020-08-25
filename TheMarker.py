# -*- coding: utf-8 -*-

from __future__ import print_function
import os
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

# Basic HTML template
doc,tag,text= Doc().tagtext()
doc.asis('<DOCTYPE html>')

# Add head tag for CSS
with tag('head'):
    with tag('link', 
        ('href','http://serve.fontsproject.com/css?family=Alef:400'),
        ('rel','stylesheet'),
        ('type','text/css')
        ):  text('')

article_text=''

# Loop to create HTML
with tag ('html', dir = "rtl"):
    with tag ('body'):
        with tag ('h1', style= "font-family:'Alef', serif;"):
            text (d.feed.title) ##Main title for RSS
        for item in range (len(d.entries)): ##Loop over articles in RSS feed
            with tag ('h2', style= "font-family:'Alef', serif;"): #Article title
                with tag ('a', href=d.entries[item].link): #Add link
                    text (d.entries[item].title)
            with tag ('p', style= "font-family:'Alef', serif; font-weight:bold;font-size: 20px;"): ##Article description
                text (d.entries[item].description)
            with tag('div', id='photo-container'): #Get picture
                links=dict(d.entries[item])
                imageLink=str(links['links'][1]['href'])
                doc.stag('img', src=imageLink, width="150px", klass="photo") #Input pic in html
            with tag ('p', style = "font-family:'Alef', serif; font-size: 15px;"): #Article text
                page=requests.get(d.entries[item].link)
                tree = html.fromstring(page.content)
                textbody = tree.xpath("//p")
                for item in textbody:
                    if sys.version_info[0]>=3: #python3
                        text(item.text_content())
                        doc.stag('br') #Add linebreaks between paragraphs
                        doc.stag('br')
                    else: #python2
                        raw_text="{0}".format(item.text_content().encode('iso-8859-1','replace'))
                        utf_text = raw_text.decode('UTF-8', 'ignore')
                        text(utf_text)
                        doc.stag('br') #Add linebreaks between paragraphs
                        doc.stag('br')

html_str=doc.getvalue().encode('UTF-8', 'ignore')

Html_file= open("TheMarker.html","wb")
Html_file.write(html_str)
Html_file.close()


os.startfile(Html_file.name, 'open')