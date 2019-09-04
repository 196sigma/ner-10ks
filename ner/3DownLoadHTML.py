import os,sys,csv,urllib2,time


os.chdir('/Users/alvinzuyinzheng/Dropbox/PythonWorkshop/scripts/')#<===The location of your file "LongCompanyList.csv
htmlSubPath = "./HTML/" #<===The subfolder with the 10-K files in HTML format

Form10kListFile = "10kList.csv" #a csv file (output of the 2Get10kLinks.py script) with the list of 10-K links
logFile = "10kDownloadLog.csv" #a csv file (output of the current script) with the download history of 10-K forms

def dowmload10k(tickerCode, docIndex, docLink, description, filingDate, newFilingDate, formLink,formName):
    csvOutput = open(logFile,"a+b")
    csvWriter = csv.writer(csvOutput, quoting = csv.QUOTE_NONNUMERIC)

    try:
        pageRequest = urllib2.Request(formLink)
        pageOpen = urllib2.urlopen(pageRequest)
        pageRead = pageOpen.read()

        htmlname = tickerCode+"_"+docIndex+"_"+newFilingDate+".htm"
        htmlpath = htmlSubPath+htmlname
        htmlfile = open(htmlpath,'wb')
        htmlfile.write(pageRead)
        htmlfile.close()
        csvWriter.writerow([tickerCode, docIndex, docLink, description, filingDate, newFilingDate, formLink,formName, htmlname, ""])
    except:
        csvWriter.writerow([tickerCode, docIndex, docLink, description, filingDate, newFilingDate, formLink,formName, "","not downloaded"])

    csvOutput.close()

def main():
    if not os.path.isdir(htmlSubPath):  ### <=== keep all HTML files in this subfolder
        os.makedirs(htmlSubPath)
    
    FormType = "10-K"   ### <=== Type your document type here
    nbDocPause = 5 ### <=== Type your number of documents to download in one batch
    nbSecPause = 1 ### <=== Type your pausing time in seconds between each batch

    FormYears = ['2014','2015'] ### <=== Type the years of documents to download here

    csvFile = open(Form10kListFile,"r") #<===A csv file with the list of company ticker symbols (the file has a line with headers)
    csvReader = csv.reader(csvFile,delimiter=",")
    csvData = list(csvReader)

    csvOutput = open(logFile,"a+b")
    csvWriter = csv.writer(csvOutput, quoting = csv.QUOTE_NONNUMERIC)

    csvWriter.writerow(["Ticker", "DocIndex", "IndexLink", "Description", "FilingDate", "NewFilingDate", "Form10KLink","Form10KName", "FileName","Note"])
    csvOutput.close()
    
    i = 1
    for rowData in csvData[1:]:
        Ticker = rowData[0]
        DocIndex = rowData[1]
        IndexLink = rowData[2]
        Description = rowData[3]
        FilingDate = rowData[4]
        NewFilingDate = rowData[5]
        FormLink = rowData[6]
        FormName = rowData[7]
        for year in FormYears:
            if year in FilingDate:
                if ".htm" in FormName:
                    dowmload10k(Ticker, DocIndex, IndexLink, Description, FilingDate, NewFilingDate, FormLink,FormName)
                elif ".txt" in FormName:
                    csvOutput = open(logFile,"a+b")
                    csvWriter = csv.writer(csvOutput, quoting = csv.QUOTE_NONNUMERIC)
                    csvWriter.writerow([Ticker, DocIndex, IndexLink, Description, FilingDate, NewFilingDate, FormLink,FormName, "","Text format"])
                    csvOutput.close()
                else:
                    csvOutput = open(logFile,"a+b")
                    csvWriter = csv.writer(csvOutput, quoting = csv.QUOTE_NONNUMERIC)
                    csvWriter.writerow([Ticker, DocIndex, IndexLink, Description, FilingDate, NewFilingDate, FormLink,FormName,"", "No form"])
                    csvOutput.close()
            
        if i%nbDocPause == 0:
            print i
            print "Pause for "+str(nbSecPause)+" second .... "
            time.sleep(float(nbSecPause))
        i=i+1
       
    csvFile.close()
    print "done!"
    
if __name__ == "__main__":
	main()
