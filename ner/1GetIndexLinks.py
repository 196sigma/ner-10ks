import os,sys,csv,urllib2,time #"time" helps to break for the url visiting 
from bs4 import BeautifulSoup   #<---- Need to install this package manually using pip
                                                #We only import part of the Beautifulsoup4

os.chdir('/Users/alvinzuyinzheng/Dropbox/PythonWorkshop/scripts/')#<===The location of your file "LongCompanyList.csv
companyListFile = "CompanyList.csv" #a csv file with the list of company ticker symbols and names (the file has a line with headers)
IndexLinksFile = "IndexLinks.csv" #a csv file (output of the current script) with the list of index links for each firm (the file has a line with headers)

def getIndexLink(tickerCode,FormType):
    csvOutput = open(IndexLinksFile,"a+b") # "a+b" indicates that we are adding lines rather than replacing lines
    csvWriter = csv.writer(csvOutput, quoting = csv.QUOTE_NONNUMERIC)
    
    urlLink = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+tickerCode+"&type="+FormType+"&dateb=&owner=exclude&count=100"
    pageRequest = urllib2.Request(urlLink)
    pageOpen = urllib2.urlopen(pageRequest)
    pageRead = pageOpen.read()
    
    soup = BeautifulSoup(pageRead,"html.parser")
    
    #Check if there is a table to extract / code exists in edgar database
    try:
        table = soup.find("table", { "class" : "tableFile2" })
    except:
        print "No tables found or no matching ticker symbol for ticker symbol for"+tickerCode
        return -1

    docIndex = 1
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells)==5:
            if cells[0].text.strip() == FormType:
                link = cells[1].find("a",{"id": "documentsbutton"})
                docLink = "https://www.sec.gov"+link['href']
                description = cells[2].text.encode('utf8').strip() #strip take care of the space in the beginning and the end
                filingDate = cells[3].text.encode('utf8').strip()
                newfilingDate = filingDate.replace("-","_")  ### <=== Change date format from 2012-1-1 to 2012_1_1 so it can be used as part of 10-K file names
                csvWriter.writerow([tickerCode, docIndex, docLink, description, filingDate,newfilingDate])
                docIndex = docIndex + 1
    csvOutput.close()


def main():  
    FormType = "10-K"   ### <=== Type your document type here
    nbDocPause = 10 ### <=== Type your number of documents to download in one batch
    nbSecPause = 0 ### <=== Type your pausing time in seconds between each batch

    csvFile = open(companyListFile,"r") #<===open and read from a csv file with the list of company ticker symbols (the file has a line with headers)
    csvReader = csv.reader(csvFile,delimiter=",")
    csvData = list(csvReader)
    
    csvOutput = open(IndexLinksFile,"a+b") #<===open and write to a csv file which will include the list of index links. New rows will be appended.
    csvWriter = csv.writer(csvOutput, quoting = csv.QUOTE_NONNUMERIC)
    
    csvWriter.writerow(["Ticker", "DocIndex","IndexLink", "Description", "FilingDate","NewFilingDate"])
    csvOutput.close()
    
    i = 1
    for rowData in csvData[1:]:
        ticker = rowData[0]
        getIndexLink(ticker,FormType)
        if i%nbDocPause == 0:
            print i
            print "Pause for "+str(nbSecPause)+" second .... "
            time.sleep(float(nbSecPause))
        i=i+1
       
    csvFile.close()
    print "done!"
    
if __name__ == "__main__":
	main()
