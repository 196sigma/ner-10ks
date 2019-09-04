import os,sys,csv,urllib2,time
from bs4 import BeautifulSoup   #<---- Need to install this package manually using pip

os.chdir('/Users/alvinzuyinzheng/Dropbox/PythonWorkshop/scripts/')#<===The location of your file "LongCompanyList.csv
IndexLinksFile = "IndexLinks.csv"  #a csv file (output of the 1GetIndexLinks.py script) with the list of index links for each firm (the file has a line with headers)
Form10kListFile = "10kList.csv"    #a csv file (output of the current script) with the list of 10-K links for each firm (the file has a line with headers)

def get10kLink(tickerCode, docIndex, docLink, description, filingDate, newFilingDate, FormType):
    csvOutput = open(Form10kListFile,"a+b")
    csvWriter = csv.writer(csvOutput, quoting = csv.QUOTE_NONNUMERIC)
    
    pageRequest = urllib2.Request(docLink)
    pageOpen = urllib2.urlopen(pageRequest)
    pageRead = pageOpen.read()
    
    soup = BeautifulSoup(pageRead,"html.parser")

    #Check if there is a table to extract / code exists in edgar database
    try:
        table = soup.find("table", { "summary" : "Document Format Files" })
    except:
        print "No tables found for link "+docLink
        
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells)==5:
            if cells[3].text.strip() == FormType:
                link = cells[2].find("a")
                formLink = "https://www.sec.gov"+link['href']
                formName = link.text.encode('utf8').strip()
                csvWriter.writerow([tickerCode, docIndex, docLink, description, filingDate, newFilingDate, formLink,formName])
    csvOutput.close()


def main():  
    FormType = "10-K"   ### <=== Type your document type here
    nbDocPause = 10 ### <=== Type your number of documents to download in one batch
    nbSecPause = 1 ### <=== Type your pausing time in seconds between each batch

    csvFile = open(IndexLinksFile,"r") #<===Open and read from a csv file with the list of index links for each firm (the file has a line with headers)
    csvReader = csv.reader(csvFile,delimiter=",")
    csvData = list(csvReader)
    
    csvOutput = open(Form10kListFile,"a+b") #<===open and write to a csv file which will include the list of 10-K links. New rows will be appended.
    csvWriter = csv.writer(csvOutput, quoting = csv.QUOTE_NONNUMERIC)
    
    csvWriter.writerow(["Ticker", "DocIndex", "IndexLink", "Description", "FilingDate", "NewFilingDate", "Form10KLink","Form10KName"])
    csvOutput.close()
    
    i = 1
    for rowData in csvData[1:]:
        Ticker = rowData[0]
        DocIndex = rowData[1]
        DocLink = rowData[2]
        Description = rowData[3]
        FileDate = rowData[4]
        NewFileDate = rowData[5]
        
        get10kLink(Ticker,DocIndex,DocLink,Description,FileDate,NewFileDate,FormType)
        if i%nbDocPause == 0:
            print i
            print "Pause for "+str(nbSecPause)+" second .... "
            time.sleep(float(nbSecPause))
        i=i+1
       
    csvFile.close()
    print "done!"
    
if __name__ == "__main__":
	main()
