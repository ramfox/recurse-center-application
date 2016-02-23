import time
import os
import urllib2
import re
import contextlib
import selenium.webdriver as webdriver
import csv

##############
#  GRAB HTML  #
##############


def grabHTML(beforeURL, fileName):
        #
        htmlFile = open(fileName, 'w')
        #
        url = beforeURL
        fp = webdriver.FirefoxProfile()
        with contextlib.closing(webdriver.Firefox(firefox_profile=fp)) as driver:
                driver.get(url)
                time.sleep(10)
                fullcode = driver.page_source.encode('utf-8')
        htmlFile.write(fullcode)
        
def parseList( vendor ):
    outputFile = open( vendor + '_file_list.txt', 'w' )
    linkFile = open( vendor + '_pulled_links.txt', 'r').read()
    textReviewed = linkFile.find('"')
    count = 0
    while ( textReviewed != -1 ):
        dressFileName = vendor + '_dress_page_' + str(count) + '.html'
        urlStart = linkFile.find('"', textReviewed) + 1 
        urlEnd = linkFile.find('"', urlStart)
        grabHTML( linkFile[ urlStart:urlEnd ], dressFileName )
        outputFile.write( '"' + dressFileName + '"\n')
        outputFile.flush()
        textReviewed = linkFile.find( '"', urlEnd + 1)
        count = count + 1


##############
#    RUN     #
##############

parseList( 'ASOS' )
parseList( 'RTR' )
parseList( 'LULUS' )