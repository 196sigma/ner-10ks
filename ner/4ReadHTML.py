#!/usr/bin/env python
from __future__ import division
from bs4 import BeautifulSoup, SoupStrainer
from HTMLParser import HTMLParser
import os
import time
import pickle
import re
import sys

# get-item1.py
## CREATED: 22 may 2017
## AUTHOR: Reginald Edwards
## MODIFIED:
## DESCRIPTION: Get ITEM 1 and ITEM 1A from a 10-K filing

DIR = "/home/reggie/Dropbox/Research/Text Analysis of Filings/footnotes/data"
RAW_10K_DIR = DIR + "/raw"
PARSED_HTML_DIR = DIR +  "/parsed-html"
PARSED_NON_HTML_DIR = DIR + "/parsed-non-html"
PARSED_DIR = DIR + "/parsed"

from bs4 import BeautifulSoup  #<---- Need to install this package manually using pip

os.chdir('/Users/alvinzuyinzheng/Dropbox/PythonWorkshop/scripts/')#<===The location of your csv files
htmlSubPath = "./HTML/" #<===The subfolder with the 10-K files in HTML format
txtSubPath = "./txt/" #<===The subfolder with the extracted text files

DownloadLogFile = "10kDownloadLog.csv" #a csv file (output of the 3DownloadHTML.py script) with the download history of 10-K forms
ReadLogFile = "10kReadlog.csv" #a csv file (output of the current script) showing whether item 1 is successfully extracted from 10-K forms

def readHTML(file_name):
    input_path = htmlSubPath+file_name
    output_path = txtSubPath+file_name.replace(".htm",".txt")
    

    input_file = open(input_path,'rb')
    page = input_file.read()  #<===Read the HTML file into Python


    #Pre-processing the html content by removing extra white space and combining then into one line.
    page = page.strip()  #<=== remove white space at the beginning and end
    page = page.replace('\n', ' ') #<===replace the \n (new line) character with space
    page = page.replace('\r', '') #<===replace the \r (carriage returns -if you're on windows) with space
    page = page.replace('&nbsp;', ' ') #<===replace "&nbsp;" (a special character for space in HTML) with space. 
    page = page.replace('&#160;', ' ') #<===replace "&#160;" (a special character for space in HTML) with space.
    while '  ' in page:
        page = page.replace('  ', ' ') #<===remove extra space

    #Using regular expression to extract texts that match a pattern
        
    #Define pattern for regular expression.
        #The following patterns find ITEM 1 and ITEM 1A as diplayed as subtitles
        #(.+?) represents everything between the two subtitles
    #If you want to extract something else, here is what you should change

    #Define a list of potential patterns to find ITEM 1 and ITEM 1A as subtitles   
    regexs = ('bold;\">\s*Item 1\.(.+?)bold;\">\s*Item 1A\.',   #<===pattern 1: with an attribute bold before the item subtitle
              'b>\s*Item 1\.(.+?)b>\s*Item 1A\.',               #<===pattern 2: with a tag <b> before the item subtitle
              'Item 1\.\s*<\/b>(.+?)Item 1A\.\s*<\/b>',         #<===pattern 3: with a tag <\b> after the item subtitle          
              'Item 1\.\s*Business\.\s*<\/b(.+?)Item 1A\.\s*Risk Factors\.\s*<\/b') #<===pattern 4: with a tag <\b> after the item+description subtitle 

    #Now we try to see if a match can be found...
    for regex in regexs:
        match = re.search(regex, page, flags=re.IGNORECASE)  #<===search for the pattern in HTML using re.search from the re package. Ignore cases.

        #If a match exist....
        if match:
            #Now we have the extracted content still in an HTML format
            #We now turn it into a beautiful soup object
            #so that we can remove the html tags and only keep the texts
            
            soup = BeautifulSoup(match.group(1), "html.parser") #<=== match.group(1) returns the texts inside the parentheses (.*?) 
            

            #soup.text removes the html tags and only keep the texts
            rawText = soup.text.encode('utf8') #<=== you have to change the encoding the unicodes

           
            #remove space at the beginning and end and the subtitle "business" at the beginning
            #^ matches the beginning of the text
            outText = re.sub("^business\s*","",rawText.strip(),flags=re.IGNORECASE)
            
            output_file = open(output_path, "w")
            output_file.write(outText)  
            output_file.close()
            
            break  #<=== if a match is found, we break the for loop. Otherwise the for loop continues

    input_file.close()    

    return match

def main():

    if not os.path.isdir(txtSubPath):  ### <=== keep all texts files in this subfolder
        os.makedirs(txtSubPath)
        
    csvFile = open(DownloadLogFile, "rb") #<===A csv file with the list of 10k file names (the file should have no header)
    csvReader = csv.reader(csvFile,delimiter=",")
    csvData = list(csvReader)
    
    logFile = open(ReadLogFile, "a+b") #<===A log file to track which file is successfully extracted
    logWriter = csv.writer(logFile, quoting = csv.QUOTE_NONNUMERIC)
    logWriter.writerow(["filename","extracted"])

    i=1
    for rowData in csvData[1:]:
##        Ticker = rowData[0]
##        DocIndex = rowData[1]
##        IndexLink = rowData[2]
##        Description = rowData[3]
##        FilingDate = rowData[4]
##        NewFilingDate = rowData[5]
##        FormLink = rowData[6]
##        FormName = rowData[7]
        FileName = rowData[8]
        
        if ".htm" in FileName:        
            match=readHTML(FileName)
            if match:
                logWriter.writerow([FileName,"yes"])
            else:
                logWriter.writerow([FileName,"no"])
        i=i+1
        
    csvFile.close()

    logFile.close()
    print "done!"
            

if __name__ == "__main__":
    main()
