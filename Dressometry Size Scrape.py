#############
#
#
#   Scrape Sizes from: 
#   ASOS
#   LULUS
#   Rent the Runway
#
#   Feb. 22nd 2016
#
#
#############

import time
import os
import urllib2
import re
import contextlib
import selenium.webdriver as webdriver
import csv

################################################################################
# OUTPUT CONFIGURATION DATA
################################################################################

# URL:
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5'

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', agent)]

# Name output file with unique timestamp.


def formatdate(xx):
    if len(str(xx)) == 1:
        xx = '0' + str(xx)
        return xx
    elif len(str(xx)) == 4:
        return str(xx)[2:]
    else:
        return str(xx)


def setfileName(movie_id):
    current = time.localtime()
    #
    YY = formatdate(current.tm_year)
    MM = formatdate(current.tm_mon)
    DD = formatdate(current.tm_mday)
    hh = formatdate(current.tm_hour)
    mm = formatdate(current.tm_min)
    #
    fileName = YY + MM + DD + "_" + hh + 'h' + mm + 'm' + '-' + movie_id + '.txt'
    return fileName

#
#
# Values used that correspond to the location in the sizes[] array:
doublezero = 29  
XXXL = 27
XXL = 25
XL = 23
L = 21
M = 19
S = 17
XS = 15
XXS = 13
na = 'na'

def outPutDressSizes(fileName, link, originalPrice, salePrice, petiteFlag, curveFlag, maternityFlag, tallFlag, extraTallFlag, sizes):
    output = link + delimiter + str(originalPrice) + delimiter + str(salePrice) + delimiter + str(petiteFlag) + delimiter + str(curveFlag) + delimiter + str(maternityFlag) + delimiter + str(tallFlag) + delimiter + str(extraTallFlag) + delimiter + str(sizes[XXS]) + delimiter + str(sizes[XS]) + delimiter + str(sizes[S]) + delimiter + str(sizes[M]) + delimiter + str(sizes[L]) + delimiter + str(sizes[XL]) + delimiter + str(sizes[XXL]) + delimiter + str(sizes[XXXL]) + delimiter + str(sizes[doublezero]) + delimiter + str(sizes[0]) + delimiter + str(sizes[2]) + delimiter + str(sizes[4]) + delimiter + str(sizes[6]) + delimiter + str(sizes[8]) + delimiter + str(sizes[10]) + delimiter + str(sizes[12]) + delimiter + str(sizes[14]) + delimiter + str(sizes[16]) + delimiter + str(sizes[18]) + delimiter + str(sizes[20]) + delimiter + str(sizes[22]) + delimiter + str(sizes[24]) + delimiter + str(sizes[26]) + delimiter + str(sizes[28])
    fileName.write(output + "\n")
    fileName.flush()     
    
# Delimiter used in the output file:
delimiter = ","

def createOutputFile(vendor):
    fileName = vendor + 'WeeklySizes.csv'
    f = open(fileName, 'w')
    f.write("Link" + delimiter + "originalPrice" + delimiter + "salePrice" + delimiter + "petiteFlag" + delimiter + "curveFlag" + delimiter + "maternityFlag" + delimiter + "tallFlag" + delimiter + "extraTallFlag" + delimiter + "XXS" +delimiter + "XS" + delimiter + "S" + delimiter + "M" + delimiter + "L" + delimiter + "XL" + delimiter + "XXL" + delimiter + "XXXL" + delimiter + "Double_Zero" + delimiter + "0" + delimiter + "2" + delimiter + "4" + delimiter + "6" + delimiter + "8" + delimiter + "10" + delimiter + "12" + delimiter + "14" + delimiter + "16" + delimiter + "18" + delimiter + "20" + delimiter + "22" + delimiter + "24" + delimiter + "26" + delimiter + "28"+ "\n")
    f.close()

################################################################################
# Scraping Delegation
################################################################################
  
  
def scrapePageForSize(vendor, link, grab):
    #
    beforeURL = link
    afterURL = ""
    #
    if (vendor == "RTR"):
        rtrSizes(beforeURL, afterURL, grab)
    if (vendor == "ASOS"):
        asosSizes(beforeURL, afterURL, grab)
    if (vendor == "LULUS"):
        lulusSizes(beforeURL, afterURL, grab)
   
        
##############
#  GRAB HTML  #
##############


def grab_html(beforeURL, fileName):
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
        

################################################################################
# SCRAPE RTR SIZES
################################################################################

def rtrSizes(beforeURL, afterURL, grab):
    #
    fileName = 'RTRWeeklySizes.csv'
    file = open(fileName, 'a')
    #
    print "RTR SIZES " + beforeURL
    #
    if ( grab == 0 ):
        filenameHtml = 'htmlContentSizeScrapeRTR.txt'
        htmlFile = open(filenameHtml, 'w')
        #
        # get file from selenium
        url = beforeURL
        fp = webdriver.FirefoxProfile()
        with contextlib.closing(webdriver.Firefox(firefox_profile=fp)) as driver:
            driver.get(url)
            time.sleep(10)
            fullcode = driver.page_source.encode('utf-8')
        htmlFile.truncate(0)
        htmlFile.write(fullcode)
    else:
        fullcode = open(grab, 'r').read()
       #
    # import file
    # textfile = open("htmlContentSizeScrapeSAMPLE.txt", 'r')
    # fullcode = textfile.read()
    #
    textReviewed = 0
    #
    #initalize
    link = beforeURL
    originalPrice = 0
    salePrice = 0
    # Markers for every possible combination of flags
    P = -1
    CP = -1
    R = -1
    CR = -1
    T = -1
    CT = -1
    X = -1
    CX = -1
    sizes = ["N/A" for i in range(240)] 
    #
    # 
    # Original Price
    start = fullcode.find('for $', textReviewed) + 5
    end = fullcode.find(' ', start)
    originalPrice = fullcode[start:end]
    textReviewed = end
    #Sale price
    salePrice = originalPrice
    #
    #Find sizes
    #
    startSizes = fullcode.find('<option value="">Select</option>', textReviewed)
    endSizes = fullcode.find('</select>', startSizes)
    startSizes = fullcode.find('data-canonical-size="', startSizes)
    largestSize = -1
    #
    while (startSizes != -1 and startSizes < endSizes):
        start = fullcode.find('>', startSizes) + 1
        end = fullcode.find('<', start)
        size = fullcode[start:end]
        #
        US = size.find('US')        
        if ( US != -1 ):
            size = size[US + 3:]
        #
        curve = size.find('W')
        comma = size.find(',')
        petite = size.find('Petite')
        regular = size.find('Regular')
        tall = size.find('Long')
        x_tall = size.find('X-Long')
        dubzero = size.find('00')
        #
        if ( curve != -1 ):
            size = size[:curve]
        elif ( comma != -1 ) :
            size = size[:comma]
            
        if ( size.find('3X') != -1  or size.find('XXXL') != -1 ):
            size = XXXL
        elif (size.find('2X') != -1  or size.find('XXL') != -1 ):
            size = XXL          
        elif ( size.find('1X') != -1  or size.find('XL') != -1 ):
            size = XL
        elif ( size.find('0X') != -1  or size.find('L') != -1 ):
            size = L
        elif ( size.find('XXS') != -1 ):
            size = XXS
        elif ( size.find('XS') != -1 ):
            size = XS
        elif ( size.find('S') != -1 ):
            size = S
        elif ( size.find('M') != -1 ):
            size = M
        else:
            size = int(size)
        #
        if ( petite != -1 and curve == -1 ):
            P = 1
            sizes[size + 30] = 'Y'
        elif ( petite != -1 and curve != -1 ):
            CP = 1
            sizes[size + 60] = 'Y'
        elif ( (regular != -1 and curve != -1) or (curve != -1 and petite == -1 and regular == -1 and tall == -1 and x_tall == -1) ):
            CR = 1
            sizes[size + 90] = 'Y'
        elif ( tall != -1 and curve == -1 ):
            T = 1
            sizes[size + 120] = 'Y'
        elif ( tall != -1 and curve != -1 ):
            CT = 1
            sizes[size + 150] = 'Y'
        elif ( x_tall != -1 and curve == -1 ):
            X = 1
            sizes[size + 180] = 'Y'
        elif ( x_tall !=-1 and curve != -1 ):
            CX = 1
            sizes[size + 210] = 'Y'
        elif ( dubzero != -1 and petite != -1 ):
            P = 1
            sizes[doublezero + 30 ] = 'Y'
        elif ( ( dubzero != -1 and regular != -1 ) or (dubzero != -1 and petite == -1 and regular == -1 and tall == -1 and x_tall == -1) ):
            R = 1
            sizes[dubzero] = 'Y'
        elif ( dubzero != -1 and tall != -1 ):
            T = 1
            sizes[doublezero + 120 ] = 'Y'
        elif ( dubzero !=-1 and x_tall != -1 ):
            X = 1
            sizes[doublezero + 180] = 'Y'
        else:
            R = 1
            sizeNum = int(size)
            sizes[sizeNum] = "Y"
            if (largestSize < sizeNum):
                largestSize = sizeNum
        startSizes = fullcode.find('data-canonical-size="', end)

    if ( R == 1 ): outPutDressSizes(file, link, originalPrice, salePrice, 'N', 'N', 'N', 'N', 'N', sizes[:30])
    if ( P == 1 ): outPutDressSizes(file, link, originalPrice, salePrice, 'Y', 'N', 'N', 'N', 'N', sizes[30:60])
    if ( CP == 1 ): outPutDressSizes(file, link, originalPrice, salePrice, 'Y', 'Y', 'N', 'N', 'N', sizes[60:90])
    if ( CR == 1 ): outPutDressSizes(file, link, originalPrice, salePrice, 'N', 'Y', 'N', 'N', 'N', sizes[90:120])
    if ( T == 1 ): outPutDressSizes(file, link, originalPrice, salePrice, 'N', 'N', 'N', 'Y', 'N', sizes[120:150])
    if ( CT == 1 ): outPutDressSizes(file, link, originalPrice, salePrice, 'N', 'Y', 'N', 'Y', 'N', sizes[150:180])
    if ( X == 1 ): outPutDressSizes(file, link, originalPrice, salePrice, 'N', 'N', 'N', 'N', 'Y', sizes[180:210])
    if ( CX == 1 ): outPutDressSizes(file, link, originalPrice, salePrice, 'N', 'Y', 'N', 'N', 'Y', sizes[210:240])
    
    
################################################################################
# SCRAPE LULUS SIZES
################################################################################


def lulusSizes(beforeURL, afterURL, grab):
    #
    fileName = 'LULUSWeeklySizes.csv'
    file = open(fileName, 'a')
    #
    print "LULUS SIZES " + beforeURL
    #
    if ( grab == 0 ):
        filenameHtml = 'htmlContentSizeScrapeLULUStxt'
        htmlFile = open(filenameHtml, 'w')
        #
        # get file from selenium
        url = beforeURL
        fp = webdriver.FirefoxProfile()
        with contextlib.closing(webdriver.Firefox(firefox_profile=fp)) as driver:
            driver.get(url)
            time.sleep(10)
            fullcode = driver.page_source.encode('utf-8')
        htmlFile.truncate(0)
        htmlFile.write(fullcode)
    else:
        fullcode = open(grab, 'r').read()
    #
    # import file
    # textfile = open("htmlContentSizeScrapeSAMPLE.txt", 'r')
    # fullcode = textfile.read()
    #
    textReviewed = 0
    #
    #initalize
    link = beforeURL
    originalPrice = 0
    salePrice = 0
    petiteFlag = "N"
    curveFlag = "N"
    maternityFlag = "N"
    tallFlag = "N"
    extraTallFlag = "N"
    sizes = [na for i in range(30)]
    #
    # petite or curve?
    if ( link.find('PETITE') != -1 or link.find('Petite') != -1 ):
        petiteFlag = "Y"
    if ( link.find('Maternity') != -1 ) :
        maternityFlag = "Y"
    if ( link.find('TALL') != -1 ):
        tallFlag = "Y"
    #na
    # find array with info
    textReviewed = 0
    #
    # FIND ORIGINAL PRICE
    #
    startDollar = fullcode.find('<sup>$</sup>', textReviewed) + 12
    endDollar = fullcode.find('<', startDollar)
    startCents = endDollar + 5
    endCents = fullcode.find('<', startCents)
    originalPrice = fullcode[startDollar:endDollar] + '.' + fullcode[startCents:endCents]
    textReviewed = endCents
    #
    #
    # FIND SALE PRICE
    #
    startDollar = fullcode.find('<sup>$</sup>', textReviewed) + 12
    endDollar = fullcode.find('<', startDollar)
    startCents = endDollar + 5
    endCents = fullcode.find('<', startCents)
    salePrice = fullcode[startDollar:endDollar] + '.' + fullcode[startCents:endCents]
    textReviewed = endCents
    #
    # FIND COLOR
    start = fullcode.find('<span class="value">', textReviewed) + 20
    end = fullcode.find('<', start)
    color = fullcode[start:end]
    textReviewed = start
    #
    # Check stock
    #
    findSize = fullcode.find('>Size<', textReviewed)
    noStock = fullcode.find('no-stock', findSize)
    toofar = fullcode.find('</select>', textReviewed)
    bookmark = fullcode.find('" value="', findSize)
    bookmark = fullcode.find('>', bookmark) + 1
    while (bookmark < toofar):
        start = bookmark
        end = fullcode.find('<', start)
        textReviewed = end
        size = fullcode[start:end]           
        size = '.' + size   
        #
        if ( noStock != -1 and noStock < bookmark ):
            if (size.find('.XXXL') != -1 or size.find('3X') != -1 or size.find('one size') != -1 ):
                sizes[XXXL] = 'N' 
            elif (size.find('.XXL') != -1 or size.find('2X') != -1 or size.find('one size') != -1 ):
                sizes[XXL] = 'N' 
            elif (size.find('.XL') != -1 or size.find('1X') != -1 or size.find('one size') != -1 ):
                sizes[XL] = 'N' 
            elif ( size.find('.L') != -1 or size.find('one size') != -1 or size.find('Large') != -1 ):
                sizes[L] = 'N'
            elif ( size.find('.M') != -1 or size.find('one size') != -1 or size.find('Medium') != -1 ):
                sizes[M] = 'N'
            elif ( size.find('.S') != -1 or size.find('one size') != -1 or size.find('Small') != -1 ):
                sizes[S] = 'N'
            elif ( size.find('.XS') != -1 or size.find('one size') != -1 or size.find('X-Small') != -1 ):
                sizes[XS] = 'N'
            elif ( size.find('.XXS') != -1 or size.find('one size') != -1 ):
                sizes[XXS] = 'N'
            else:
                sizeNum = int(size[1:])
                sizes[sizeNum] = "N"   
        else:
            if (size.find('.XXXL') != -1 or size.find('3X') != -1 or size.find('one size') != -1 ):
                sizes[XXXL] = 'Y' 
            elif (size.find('.XXL') != -1 or size.find('2X') != -1 or size.find('one size') != -1 ):
                sizes[XXL] = 'Y' 
            elif (size.find('.XL') != -1 or size.find('1X') != -1 or size.find('one size') != -1 ):
                sizes[XL] = 'Y' 
            elif ( size.find('.L') != -1 or size.find('one size') != -1 or size.find('Large') != -1 ):
                sizes[L] = 'Y'
            elif ( size.find('.M') != -1 or size.find('one size') != -1 or size.find('Medium') != -1 ):
                sizes[M] = 'Y'
            elif ( size.find('.S') != -1 or size.find('one size') != -1 or size.find('Small') != -1 ):
                sizes[S] = 'Y'
            elif ( size.find('.XS') != -1 or size.find('one size') != -1 or size.find('X-Small') != -1 ):
                sizes[XS] = 'Y'
            elif ( size.find('.XXS') != -1 or size.find('one size') != -1 ):
                sizes[XXS] = 'Y'
            else:
                sizeNum = int(size[1:])
                sizes[sizeNum] = "Y"
        noStock = fullcode.find('no-stock', bookmark)
        bookmark = fullcode.find('" value="', textReviewed)
        bookmark = fullcode.find('>', bookmark) + 1
    # output the dress sizes
    outPutDressSizes(file, link, originalPrice, salePrice, petiteFlag, curveFlag, maternityFlag, tallFlag, extraTallFlag, sizes)

################################################################################
# SCRAPE ASOS SIZES
################################################################################


def asosSizes(beforeURL, afterURL, grab):
    #
    fileName = 'ASOSWeeklySizes.csv'
    file = open(fileName, 'a')
    #
    if (grab != 0):
    	print "ASOS SIZES" + grab
    else:
    	print "ASOS SIZES " + beforeURL
    #
    if ( grab == 0 ):
        filenameHtml = 'htmlContentSizeScrapeASOS.txt'
        htmlFile = open(filenameHtml, 'w')
        #
        # get file from selenium
        url = beforeURL
        fp = webdriver.FirefoxProfile()
        with contextlib.closing(webdriver.Firefox(firefox_profile=fp)) as driver:
            driver.get(url)
            time.sleep(10)
            fullcode = driver.page_source.encode('utf-8')
        htmlFile.truncate(0)
        htmlFile.write(fullcode)
    else:
        fullcode = open(grab, 'r').read()
    # import file
#   textfile = open("htmlContentSizeScrapeSAMPLE.txt", 'r')
#   fullcode = textfile.read()
    #
    textReviewed = 0
    #
    #initalize
    link = beforeURL
    originalPrice = 0
    salePrice = 0
    petiteFlag = "N"
    curveFlag = "N"
    maternityFlag = "N"
    tallFlag = "N"
    extraTallFlag = "N"
    sizes = [na for i in range(30)]
    #
    # petite or curve?
    if ( link.find('PETITE') != -1 or link.find('Petite') != -1 ):
        petiteFlag = "Y"
    if ( link.find('Maternity') != -1 ) :
        maternityFlag = "Y"
    if ( link.find('TALL') != -1 ):
        tallFlag = "Y"
    #
    # find array with info
    textReviewed = 0
    #
    # FIND COLOR
    start = fullcode.find("http://images.asos-media.com/", textReviewed) + 29
    i = 0
    while ( i < 7 ):
        start = fullcode.find('/', start) + 1
        i = i + 1
    end = fullcode.find('/', start)
    color = fullcode[start:end]
    #
    textReviewed = fullcode.find("SeparateProduct = new Array", 0) + 27
    #
    #after all info
    textEnd = fullcode.find("</script>", textReviewed)
    #
    # ALL INFO CAN BE FOUND IN THIS ARRAY
    largestSize = 0;
    while ( textReviewed < textEnd ):
        start = fullcode.find('"', textReviewed) + 1 
        end = fullcode.find('"', start)
        size = fullcode[start:end]
        textReviewed = end
        #
        start = fullcode.find('","', textReviewed) + 3
        end = fullcode.find('"', start)
        colorPrime = fullcode[start:end]
        textReviewed = end
        #
        #make sure it's lowercase
        colorPrime = colorPrime.lower()
        #
        if ( color == colorPrime ):
            #
            if ( size == 'XXXL' or size == '3X' ):
                size = XXXL
            elif ( size == 'XXL' or size == '2X' ):
                size = XXL
            elif ( size == 'XL' or size == '1X' ):
                size = XL
            elif ( size == 'L' or size == 'M/L' or size == 'M / L'):
                size = L
            elif ( size == 'M' or size == 'S/M' or size == 'M/L' or size == 'M / L' ):
                size = M
            elif ( size == 'S' or size == 'XS / S' or size == 'S/M' ):
                size = S
            elif ( size == 'XS' or size == 'XS / S' ):
                size = XS
            elif (size == 'XXS'):
                size = XXS
            elif (size == 'US 00'):
                size = doublezero
            elif (size == 'US Size 0'):
                size = 0
            elif (size == 'Size 0' or size == 'US Size 2' ):
                size = 2
            elif (size == 'Size 1' or size == 'US Size 4' ):
                size = 4
            elif (size == 'Size 2' or size == 'US Size 6' ):
                size = 6
            elif (size == 'Size 3' or size == 'US Size 8' ):
                size = 8
            elif (size == 'Size 4' or size == 'US Size 10' ):
                size = 10
            elif (size == 'Size 5' or size == 'US Size 12' ):
                size = 12
            elif ( size.find('32') != -1 ):
                size = 0
            elif ( size.find('34') != -1 ):
                size = 2
            elif ( size.find('36') != -1 ):
                size = 4
            elif ( size.find('38') != -1 ):
                size = 6
            elif ( size.find('40') != -1 ):
                size = 8
            elif ( size.find('42') != -1 ):
                size = 10
            elif ( size.find('44') != -1 ):
                size = 12
            elif ( size.find('46') != -1 ):
                size = 14
            else: 
                size = size[3:]
            # avail or not?
            start = fullcode.find('","', textReviewed) + 3
            end = fullcode.find('"', start)
            avail = fullcode[start:end]
            textReviewed = end
            #
            # see if alternate sizing
            #
            start = fullcode.find('","', textReviewed) + 3
            end = fullcode.find('"', start)
            altSize = fullcode[start:end]
            if (altSize != '' and altSize.find('-') == -1 and altSize[3:] != ''):
                size = altSize[3:]
            #
            size = int(size)
            largestSize = size
            #
            # is this size available?
            if ( 'True' == avail ):
                sizes[size] = "Y"
            else:
                sizes[size] = "N"
        #
        # move to next size
        textReviewed = fullcode.find("new Array", textReviewed)
    #
    # plus size?
    if ( largestSize > 14 and largestSize % 2 == 0 ):
        curveFlag = "Y"
    if ( largestSize ==27 ):
        curveFlag = "Y"
    #
    sale = fullcode.find('product_price_details discounted-price', end)
    if (sale != -1):
        start = sale
    else:
        start = fullcode.find('product_price_details')
    start = fullcode.find('$', start) + 1
    end = fullcode.find('<', start)
    originalPrice = fullcode[start:end]
    #
    if (sale != -1):
        start = fullcode.find('"previousprice"', end) + 3
        start = fullcode.find('$', start) + 1
        end = fullcode.find('<', start)
        salePrice = fullcode[start:end]
    else:
        salePrice = originalPrice
    #
    # output the dress sizes
    outPutDressSizes(file, link, originalPrice, salePrice, petiteFlag, curveFlag, maternityFlag, tallFlag, extraTallFlag, sizes)
        
        
################################################################################
# parse HTML Delegation - Goes through HTML and grabs all dress page links
################################################################################

def parseHTML(vendor, fileName):
    #
    if (vendor == "RTR"):
        parseRTR(fileName)
    elif (vendor == "ASOS"):
        parseASOS(fileName)
    elif (vendor == "LULUS"):
        parseLULUS(fileName)
    else:
        print "vendor not recognized, cannot parse HTML"
   
######################
#  RTR parse html    #
######################
    
def parseRTR(fileName):
    #
    linkFile = open('RTR_links.txt', 'a')
    htmlFile = open(fileName, 'r')
    fullcode = htmlFile.read()
    textReviewed = 0
    textReviewed = fullcode.find('grid-product-card-heart-click-wrapper', textReviewed)
    #
    while ( textReviewed != -1 ):
        end = textReviewed + 23  
        href_spot = fullcode.find('href="', textReviewed) + 6  
        url_end = fullcode.find('"', href_spot)     
        #
        output = '"http://www.renttherunway.com' + fullcode[href_spot:url_end]  + '"'      
        #
        #
        linkFile.write(output + "\n")
        linkFile.flush()
        #
        textReviewed = fullcode.find('grid-product-card-heart-click-wrapper', end)
    linkFile.close()
    htmlFile.close()

######################
#  LULUS parse html  #
######################

def parseLULUS(fileName):
    #
    linkFile = open('LULUS_links.txt', 'a')
    htmlFile = open(fileName, 'r')
    fullcode = htmlFile.read()
    textReviewed = 0
    textReviewed = fullcode.find('<h3 class="brand">', textReviewed)
    #
    while ( textReviewed != -1 ):
        end = textReviewed + 18  
        href_spot = fullcode.find('href', textReviewed) + 6  
        url_end = fullcode.find('"', href_spot)     
        #
        output = '"http://www.lulus.com' + fullcode[href_spot:url_end]  + '"'      
        #
        #
        linkFile.write(output + "\n")
        linkFile.flush()
        #
        textReviewed = fullcode.find('<h3 class="brand">', end)
    linkFile.close()
    htmlFile.close()
######################
#  ASOS parse html   #
######################

def parseASOS(fileName):
    #
    linkFile = open('ASOS_links.txt', 'a')
    htmlFile = open(fileName, 'r')
    fullcode = htmlFile.read()
    textReviewed = 0
    textReviewed = fullcode.find('class="categoryImageDiv"', textReviewed)
    #
    while ( textReviewed != -1 ):
        start = fullcode.find('href="', textReviewed) + 6          
        end = fullcode.find('"', start)     
        #
        output = '"' + fullcode[start:end]  + '"'      
        #
        #
        linkFile.write(output + "\n")
        linkFile.flush()
        #
        textReviewed = fullcode.find('class="categoryImageDiv"', end)
    linkFile.close()
    htmlFile.close()

################################################
# RTR - get all links from their 'Dress' section
################################################

# 0 if need to pull links and parse
# 1 if just need to parse
# -1 if nothing
def findLinksRTR(i):
    if (i != -1 ):
        linkFile = open('RTR_links.txt', 'w')
        endloop = -1
        count = 1
        print 'Begin gathering all links'
        while(endloop == -1):
            count_s = str(count)
            url = 'https://www.renttherunway.com/products/dress?action=click_all_dresses&nav_location=submenu&object_type=top_nav&page=' + count_s 
            fileName = 'RTR_page_'+ count_s + '.html'
            if (i == 0):
                grab_html(url, fileName)
            parseHTML('RTR', fileName)
            count = count + 1
            endloop = open(fileName).read().find('Sorry, this page is unavailable.')
        linkFile.close()
################################################
# LULUS - get all links from their 'Dress' section
################################################

# 0 if need to pull links and parse
# 1 if just need to parse
# -1 if nothing
def findLinksLULUS(i):
    if (i != -1 ):
        linkFile = open('LULUS_links.txt', 'w')
        endloop = -1
        count = 1
        print 'Begin gathering all links'
        while(endloop == -1):
            count_s = str(count)
            url = 'http://www.lulus.com/categories/page' + count_s + '-60/13/dresses.html?'
            fileName = 'LULUS_page_'+ count_s + '.html'
            if (i == 0):
                grab_html(url, fileName)
            parseHTML('LULUS', fileName)
            count = count + 1
            endloop = open(fileName).read().find('No products were found in stock matching your filters.')
        linkFile.close()
################################################
# ASOS - get all links from their 'Dress' section
################################################

# 0 if need to pull links and parse
# 1 if just need to parse
# -1 if nothing
def findLinksASOS( i ):
    if (i != -1 ):
        linkFile = open('ASOS_links.txt', 'w')
        endloop = 1
        count = 1
        print 'Begin gathering all links'
        if (i == 0): grab_html('http://us.asos.com/Women-En-Womens-Dresses/ycytv/?cid=15801#parentID=-1&pge=0&pgeSize=204&sort=-1', 'ASOS_HTML_0.html')
        parseHTML( 'ASOS', 'ASOS_HTML_0.html')
        while(endloop != -1):
            count_s = str(count)
            url = 'http://us.asos.com/Women-En-Womens-Dresses/ycytv/?cid=15801#parentID=-1&pge=' + count_s + '&pgeSize=204&sort=-1'
            fileName = 'ASOS_page_'+ count_s + '.html'
            if (i == 0):
                grab_html(url, fileName)
            parseHTML('ASOS', fileName)
            endloop = open(fileName).read().find('page-skip')
            endloop = endloop + 9
            endloop = open(fileName).read().find('page-skip', endloop )
            count = count + 1
        linkFile.close()
            
################################################
#  findlinks Delegation
################################################   

def findLinks(vendor, i):
    if ( vendor == 'RTR' ):
        findLinksRTR(i)
    elif ( vendor == 'LULUS' ):
        findLinksLULUS(i)
    elif ( vendor == 'ASOS' ):
        findLinksASOS(i)
    else:
        print 'vendor not recognized, cannot find links'

################################################
#  visit links - opens up each dress page and scrape the page
################################################  

def visitLinks( vendor, grab = 0 ):
    createOutputFile( vendor )
    if ( grab != 0 ):
    	linkListFile = open('pulled/' + vendor + '_pulled_links.txt', 'r')
    else:
    	linkListFile = open( vendor + '_links.txt', 'r')
    linkList = linkListFile.read()
    textReviewed = linkList.find('"', 0)
    count = 0
    while (textReviewed != -1):
        url_start = textReviewed + 1
        url_end = linkList.find('"', url_start)
        if (grab != 0): 
            grab = 'pulled/' + vendor + '_dress_page_' + str(count) + '.html'
        scrapePageForSize( vendor, linkList[url_start:url_end], grab)
        textReviewed = linkList.find('"', url_end + 1)
        count = count + 1
    
###########################################################################################
#  Don't want to gather every dress link? here are a sample of dress pages you can use
################################################ ########################################## 

def lulusSample():
    createOutputFile( 'LULUS' )
    scrapePageForSize("LULUS", "http://www.lulus.com/products/sight-to-behold-ivory-embroidered-long-sleeve-dress/282122.html")
    scrapePageForSize("LULUS", "http://www.lulus.com/products/starring-role-beige-and-black-lace-dress/241170.html")
    scrapePageForSize("LULUS", "https://www.lulus.com/products/bb-dakota-larelle-navy-blue-lace-dress/279922.html")
    scrapePageForSize("LULUS", "http://www.lulus.com/products/picture-perfection-hot-pink-dress/226442.html") 
    scrapePageForSize("LULUS","http://www.lulus.com/products/lulus-exclusive-work-wonders-grey-dress/157642.html") 
    scrapePageForSize("LULUS","http://www.lulus.com/products/air-of-romance-taupe-maxi-dress/264682.html")

def rtrSample():
    createOutputFile( 'RTR' )
    scrapePageForSize("RTR", "http://www.renttherunway.com/pdp/items/MNL42")
    scrapePageForSize("RTR", "http://www.renttherunway.com/pdp/items/BM154")
    scrapePageForSize("RTR", "https://www.renttherunway.com/shop/designers/badgley_mischka/shimmering_blush_gown")
    scrapePageForSize("RTR", "https://www.renttherunway.com/shop/designers/marchesa_notte/precision_gown") 
    scrapePageForSize("RTR", "https://www.renttherunway.com/shop/designers/elizabeth_and_james/such_a_tease_dress")
    scrapePageForSize("RTR", "https://www.renttherunway.com/shop/designers/narciso_rodriguez/jet_cutout_gown")
    

def asosSample():
    createOutputFile( 'ASOS' )
    scrapePageForSize("ASOS", "http://us.asos.com/Little-Mistress-Lace-Waist-Maxi-Dress/1858qm/?iid=5997828&cid=15801&sh=0&pge=0&pgesize=36&sort=-1&clr=Sage+green&totalstyles=5459&gridsize=3&mporgp=L0xpdHRsZS1NaXN0cmVzcy9MaXR0bGUtTWlzdHJlc3MtTGFjZS1XYWlzdC1NYXhpLURyZXNzL1Byb2Qv")
    scrapePageForSize("ASOS", "http://us.asos.com/Warehouse-D-Ring-Wrap-Dress/187teg/?iid=5974425&cid=15801&sh=0&pge=4&pgesize=36&sort=-1&clr=Teal&totalstyles=5467&gridsize=3&mporgp=L1dhcmVob3VzZS9XYXJlaG91c2UtRC1SaW5nLVdyYXAtRHJlc3MvUHJvZC8")
    scrapePageForSize("ASOS", "http://us.asos.com/ASOS-Sheer-and-Solid-Pleated-Mini-Cami-Dress/16hrik/?iid=5072113&cid=15801&sh=0&pge=151&pgesize=36&sort=-1&clr=Baby+blue&totalstyles=5459&gridsize=3&mporgp=L0FTT1MvQVNPUy1TaGVlci1hbmQtU29saWQtUGxlYXRlZC1NaW5pLUNhbWktRHJlc3MvUHJvZC8")
    scrapePageForSize("ASOS", "http://us.asos.com/ASOS-PETITE-Exclusive-Lace-Up-V-Neck-Shift-Dress/16hpxr/?iid=5350402&cid=15801&sh=0&pge=151&pgesize=36&sort=-1&clr=Rust&totalstyles=5459&gridsize=3&mporgp=L0FTT1MtUGV0aXRlL0FTT1MtUEVUSVRFLUxhY2UtVXAtVi1OZWNrLVNoaWZ0LURyZXNzL1Byb2Qv") 
    scrapePageForSize("ASOS","http://us.asos.com/Boohoo-Plus-High-Neck-Ribbed-Swing-Dress-3-4-Sleeve/17wkt9/?iid=5904528&cid=15801&sh=0&pge=0&pgesize=36&sort=3&clr=Rust&totalstyles=6098&gridsize=3&mporgp=L0Jvb2hvby1QbHVzL0Jvb2hvby1QbHVzLUhpZ2gtTmVjay1SaWJiZWQtU3dpbmctRHJlc3MtMy80LVNsZWV2ZS9Qcm9kLw..") 
    scrapePageForSize("ASOS","http://us.asos.com/Carmakoma-Shift-Dress/17o86o/?iid=5712990&amp;cid=15801&amp;sh=0&amp;pge=75&amp;pgesize=36&amp;sort=-1&amp;clr=Red&amp;totalstyles=2722&amp;gridsize=3&amp;mporgp=L0Nhcm1ha29tYS9DYXJtYWtvbWEtU2hpZnQtRHJlc3MvUHJvZC8.")

def scrapeSizes( vendor, i ):
    findLinks( vendor, i )
    visitLinks( vendor )
    
    
################################################
#  Scrape sizes on already pulled html
################################################  
    
def scrapedPulledHTML():
	visitLinks('ASOS', 1)
	visitLinks('RTR', 1)
	visitLinks('LULUS', 1)
    
    
################################################
#  RUN CODE
################################################  


#   1 runs all three     -      goes through each page of the respective website's 'Dress' section
#                               parses through these pages to collect every link to every dress
#                               finally, visits every link and adds that dress' size to a csv output file
#   2 runs only renttherunway
#   3 runs only lulus
#   4 runs only asos
#   5 runs only a few pages from each - just visits the links specified
#   6 runs a few pages from rtr
#   7 runs a few pages from lulus
#   8 runs a few pages from asos

# Set = 0 if you want to run without Selenium on previously pulled files!

set = 0
if ( set == 1 ):
    # second parameter
    # set to 0 if you   need to go through whole process of visiting the website's 'Dress' section and get every dress link
    #                   and then parse through this and gather every possible link
    # set to 1 if you   already have visiting every page of the 'Dress' section
    #                   and just need to parse through these few webpages to gather all links
    # set to -1 if you  already have all the links in a txt file and don't need to do either
    #
    scrapeSizes( 'RTR', 1 )
    scrapeSizes( 'LULUS', 1 )
    scrapeSizes('ASOS', 1 )
if ( set == 2 ):
    scrapeSizes( 'RTR', -1 )
if ( set == 3 ):
    scrapeSizes( 'LULUS', 0 )
if ( set == 4 ):
    scrapeSizes('ASOS', 0 )
if ( set == 5 ):
    rtrSample()
    lulusSample()
    asosSample()
if ( set == 6 ):
    rtrSample()
if ( set == 7 ):
    lulusSample()
if ( set == 8 ):
    asosSample()
    
# If you don't want to have to open up a hundred pages and scrape from there to test, 
# I pulled 100 dress pages from each website and you can run it on those pages
if ( set == 0 ):
    scrapedPulledHTML()
#
# Ouput can be found in ASOSWeeklySizes.csv
#						LULUSWeeklySizes.csv
#						RTRWeeklySizes.csv