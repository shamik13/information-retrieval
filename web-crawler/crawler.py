from Queue import Queue
from bs4 import BeautifulSoup
from goose import Goose
import requests, fnmatch, os, glob, time, urllib, threading

#Initialization
 # Threads and Semaphores
semaphore = threading.Semaphore(5)
lock_doc_id = threading.Lock()
lock_all_queues = threading.Lock()

toCrawl = Queue().queue
crawled = Queue().queue

homeurl = 'http://www.thehindu.com/'
website = 'www.thehindu.com'

directory  = "/home/vaibhav/python/crawlDir/"
doc_id = 1
DOCS_TO_SAVE = 750
MIN_WORD_IN_DOC = 150

# Create Directory
if not os.path.exists(directory):
    os.makedirs(directory)
all_files_in_dir = glob.glob(directory + '*')
for i in all_files_in_dir:
    os.remove(i)

def createDoc(url, title, meta_keywords, date, content):
    global doc_id, directory
    lock_doc_id.acquire()
    this_doc_id = doc_id
    doc_id = doc_id + 1
    lock_doc_id.release()
    doc_name = directory + str(this_doc_id) + '.txt'
    doc = open(doc_name, 'w')
    print "Entered Director to print : " + doc_name + "\n"
    doc.write("URL: " + url + '\n')
    doc.write("TITLE: " + str(title) + '\n')
    doc.write("META-KEYWORDS: " + str(meta_keywords) + '\n')
    doc.write("DATE: " + str(date) + '\n')
    doc.write("DOC ID: " + str(this_doc_id) + '\n')
    doc.write("CONTENT: " + content.encode('utf8', 'ignore') + '\n')
    doc.close()
    print("Please check whether doc is created or not\n")

def CheckForContent(raw_html,soup):
    # Goose package used to extract Articles from News Websites only
    g= Goose()
    try:
        article=g.extract(raw_html=raw_html.content)
    except:
        return
    content= article.cleaned_text
    if len(content.split()) < MIN_WORD_IN_DOC :
        return
    page_title=soup.title.string.replace("\n","").encode('utf-8')
    keywords = soup.findAll(attrs={"name":"keywords"})
    keywords = keywords[0]['content'].encode('utf-8').replace(',','') if keywords else ""
    date = soup.findAll(attrs={"name":"DC.date.issued"})
    date = date[0]['content'].encode('utf-8') if date else ""
    createDoc(link, page_title, keywords, date, content)

def threads_work(link,thread_number):
        global homeurl, website, DOCS_TO_SAVE, MIN_WORD_IN_DOC 
        print " Thread #" + str(thread_number) + " : Link : " + str(link)
        raw_html = requests.get(link)
        # Extract only html/text links
        if "text/html" not in raw_html.headers["content-type"]:
            semaphore.release()
            print " Thread #" + str(thread_number) + " : REJECTED as Non-HTML Page"
            return
        time.sleep(0.5)
        soup = BeautifulSoup(raw_html.content, "html.parser")
        CheckForContent(raw_html,soup)

        for a_set in soup.find_all('a'):
            try:
                next_link = str(a_set.get('href'))
            except:
                continue
            # Relative Link and External Link
            if homeurl not in next_link:
               mod_link = homeurl + next_link
               lock_all_queues.acquire()
               if mod_link not in crawled and mod_link not in toCrawl and not fnmatch.fnmatch(mod_link, '*http*http*'):
                   toCrawl.append(mod_link)
                   print "To be Visited: " + mod_link
               lock_all_queues.release()
            # Internal Link
            else:
                lock_all_queues.acquire()
                if next_link not in crawled and next_link not in toCrawl:
                    toCrawl.append(next_link)
                    print "To be Visited: " + next_link
                lock_all_queues.release()
        print " Thread #" + str(thread_number) + " : Finished"
        semaphore.release()


# Procedure Init
if __name__ == "__main__":
    toCrawl.append(homeurl)
    i = 0
    while 1:
        semaphore.acquire()

        # Check for Number of Docs created
        lock_doc_id.acquire()
        if doc_id > DOCS_TO_SAVE:
            print("Required number (%d) of Documents created. Hence Exiting.", DOCS_TO_SAVE)
            break
        lock_doc_id.release()

        lock_all_queues.acquire()
        if toCrawl:
            link  = toCrawl.pop()
            crawled.append(link)
            lock_all_queues.release()
            i = i + 1
            t = threading.Thread(target=threads_work, args=(link,i))
            t.start()
            print "Started Thread #" + str(i) + "\n"
        
        else:
            semaphore.release()
            lock_all_queues.release()
