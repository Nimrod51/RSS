#html creator


from yattag import Doc


doc,tag,text= Doc().tagtext()

doc.asis('<!DOCTYPE html>')

for i in range (1,11):
    #print i
    with tag ('html'):
        with tag ('body'):
            with tag ('p'):
                text (i)

#print doc.getvalue()
html_str=doc.getvalue()

Html_file= open("Themarker.html","w")
Html_file.write(html_str)
Html_file.close()
