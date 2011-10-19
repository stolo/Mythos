#!/usr/bin/python

from Ol
from BeautifulSoup import BeautifulSoup 

page = open("./GreekGods.data", 'r')
for line in page.readlines():
    print line.split("||")[0].decode('utf-8')
    print line.split("||")[1].decode('utf-8')
    print line.split("||")[2].decode('utf-8')
