#!/usr/bin/env python
import socket as skt
import os
import sys
from urlparse import urlparse
import cStringIO

class Downloader(object):
    def __init__(self, url, path, filename, port):
        self.filename =filename
        NL = "\r\n"
        self.cContent = cStringIO.StringIO()
        self.url = url
        self.path = path
        self.filename = open(self.filename, "w+")
        self.port = port
        self.header = ""
        self.headerLength = 0
        self.content = ""
        self.contentLength = ""
        self.contentExist = False

        # self.file = open(self.filename, "w+")
        self.clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.checkResume = False
        self.headByte = 0
        self.tailByte = 0
        self.etagStatus = False
        self.modifiedStatus = False
        self.etag = ""
        self.lastModified = ""

        # self.filePair = open(self.filename+NL+self.lastModified+NL, "wb")

        self.main()

    def urlVerification(self):
        if self.url[:7] != "http://":
            return "http://" + self.url
        return self.url

    def makeGet(self):
        return ("GET {n} HTTP/1.1\r\n"+ "Host: {s}\r\n"+"Connection: close\r\n\r\n").format(n=self.path,s=self.url)

    def makeResumeGet(self):
        return ("GET {n} HTTP/1.1\r\n"+ "Host: {s}\r\n"+"Connection: close\r\n"+"Range: {b}\r\n").format(n=self.path,s=self.url,b=self.headByte)



    def Openconnection(self):
        self.clientSocket.connect((self.url, self.port))
        if self.checkResume == True:

            self.clientSocket.send(self.makeResumeGet())
        if self.checkResume == False:
            self.clientSocket.send(self.makeGet())

    def closeConnection(self):
        self.clientSocket.close()
        self.content = ""

    def makeHeader(self):
        self.Openconnection()
        while "\r\n\r\n" not in self.header:
            data = self.clientSocket.recv(1)
            self.header += data
            if "\r\n\r\n" in self.header:
                self.extractHeader()
                self.extractETAG()
                self.extractLastModified()
        print self.header
        print "etag:", self.etag , "end"
        print "lastmo:", self.lastModified
        print "contentLength", self.contentLength


    def extractHeader(self):
        for x in self.header[self.header.find("Content-Length")+16:]:
            if x =="\r":
                self.contentExist = True
                break
            self.contentLength += x
        self.headerLength = len(self.header)

    def extractETAG(self):
        if "\r\n\r\n" in self.header:
            for x in self.header[self.header.find("ETag")+5:]:
                if x =="\r" :
                    break
                self.etag +=x

    def extractLastModified(self):
        if "\r\n\r\n" in self.header:
            for x in self.header[self.header.find("Last-Modified")+14:]:
                if x=="\r":
                    break
                self.lastModified += x

    def downloadWithContent(self):

        while len(self.content) < int(self.contentLength):
            self.content = self.clientSocket.recv(1024)
            # self.headByte , self.contentLength
            # self.headByte += len(self.content)
            if len(self.content) == 0 :
                break

            self.file.write(self.content)

        self.closeConnection()

    def downloadWithoutContent(self):

        while True:
            self.content = self.clientSocket.recv(1024)

            if not len(self.content) == 0:
                break

            self.file.write(self.content)
        self.closeConnection()

    def handleError(self):
        pass


    def checkResumeCondition(self):

        if os.path.isfile(self.file):
            print "-------", self.file
            print "file exist"
            print "os.path:", os.path.getsize(self.file)
            self.headByte = os.path.getsize(self.file)
            print "BYETE START""""""",self.headByte
            if self.headByte > 0 :
                print "eayyyyyyyyyyyyyy"*10
                self.checkResume = True



    def resumeDownload(self):
        self.closeConnection()
        self.Openconnection()
        print "ohlaa tttttttttttttttttttttttt"
        pass


    def checkPort(self):
        if self.port == None:
            self.port = 80

    def main(self):


        self.checkResumeCondition()
        print  "CHECK RESUME" ,self.checkResume
        self.urlVerification()
        self.checkPort()
        self.makeHeader()
        # print self.header


        if self.checkResume == True:
            if self.contentExist:
                print "REEEESUMMMEE"
                self.resumeDownload()
        #
            if self.contentExist == False:
                self.downloadWithoutContent()
        #
        if self.checkResume == False:
            if self.contentExist:
                self.downloadWithContent()
        #
            if self.contentExist == False:
                self.downloadWithoutContent()





link = sys.argv[-1]
FILENAME = sys.argv[-2]
parseStr = urlparse(link)
URL = parseStr.hostname
PATH = parseStr.path
PORT = parseStr.port

a = Downloader(URL, PATH, FILENAME, PORT)
