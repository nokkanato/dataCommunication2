# dataCommunication2

function has been increased from first version

def main(self):
        self.checkPort()    check the port of the url if there is none, defualt port = 80
        self.urlVerification() check url whether it comes with http or not
        self.checkResumeCondition() check REsume condition
                                    it will look at the directory if there is the file downloaded 
        if self.checkResume == True:


            self.resumeDownload()  again itwill open the socket and send the request in byte if it should resume 
                                  then send header for resumation , if it is not supported , download again
                                  then check old file whether it has etag and lastmodified then compared with new one
                                  if download succeed delete pair file
                    

        if self.checkResume == False:
            self.makeHeader()
            if self.contentExist:
                self.downloadWithContent()

            if self.contentExist == False:
                self.downloadWithoutContent()
