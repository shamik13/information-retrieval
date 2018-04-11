Introduction
This sowftare is produced to crawl a website and extracting the text data from it on python.

Requirement
This works better with python 2.7 in ubuntu. Some of the libraries might not work well with the other versions of it.
Following libraries are needed to be downloaded first if not present on the test system-
BeautifulSoup, requests, fnmatch, os, glob, time, urllib, threading.

How to use
1) You can change the source url using value present at variable "homeurl".
2) Changing the "directory" for the storing the files is must.
3) You can change the no of words in each document and no of documents to be saved by changing the value of variables "MIN_WORD_IN_DOC" and "DOCS_TO_SAVE" respectively.

Warning
Using some websites for crawling might block your I.P adress for that perticular website for some time. Though delays can be introduced to eliminate the problem