import re
import unicodedata
import docx2txt
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import datetime
from time import sleep
from itertools import takewhile, count
import multiprocessing






notmatched=[]
searchedlink=""
plagcount=0

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def tokenize_sentence(text):
    sentences = re.split('(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=\\.|\\?|\\!|\\n)\\s', text)
    return sentences

# def oldlink(txt):
#     #global sentancearr
    
#     global searchedlink
#     global plagcount
#     lsearched=requests.get(searchedlink)
#     plagcount=0
#     soupl1 = BeautifulSoup(lsearched.text, 'html.parser')
#     child_soup=soupl1.findAll("div")
        
#     for i in child_soup:
#         websentences = tokenize_sentence(i.text)
#         for y in websentences: 
#             #print(i.text)
#             if txt in y:
#                 plagcount=1
#                 break
#             elif similar(y,txt) >= 0.6:
#                 #print("Plagiarism: 90%")
#                 #print(txt)
#                 plagcount=1
#                 break
            
#     if plagcount== 1:
#         #sentancearr.append(txt)
#         print("Searched Link:",searchedlink)
#         print("Text:",txt)
#         searchedlink=searchedlink
        
#         return 1
        


def rechecking(txt,sentancematch,sentancearr,linksmatch,matchwordcount,sentencelist):
    print("Sentance Remaining:",txt)
    print("Links MAtched from rechecking:",linksmatch)
    for x in linksmatch:
        lsearched=requests.get(x)
        plagcount=0
        soupl1 = BeautifulSoup(lsearched.text, 'html.parser')
        child_soup=soupl1.findAll("div")
        
        for i in child_soup:
            websentences = tokenize_sentence(i.text)
            for y in websentences: 
                #print(i.text)
                if txt in y:
                    plagcount=1
                    break
                elif similar(y,txt) >= 0.6:
                    #print("Plagiarism: 90%")
                    #print(txt)
                    plagcount=1
                    break
            
        if plagcount== 1:
            matchwordcount.append(txt)
            #sentancearr.append(txt)
            print("Searched Link:",searchedlink)
            print("Text from rechecking:",txt)
            sentencelist.append(txt)
            sentancematch.value+=1
            break
    if plagcount==0:
        print("Not Found")
            





def plagiarismchecker(txt,sentancematch,sentancearr,linksmatch,matchwordcount,sentencelist):
    
    print(txt)
    global searchedlink
    global plagcount
    
    global notmatched
    
    Base_string = "https://www.google.com/search?q="
    Google_Search = Base_string + txt
    res = requests.get(Google_Search)
    soup = BeautifulSoup(res.text, 'html5lib')
    
    links_list = []

    links = soup.findAll("a")

    for link in links:
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
            links_list.append(link.get('href').split("?q=")[1].split("&sa=U")[0])

    links = []
    count = 0

    for x in links_list:
        if count == 10:
            break
        if 'youtube' not in x and 'pdf' not in x:
            links.append(x)
            count += 1
    plagcount=0
    count1=0
    
    #endTime = datetime.datetime.now() + datetime.timedelta(seconds=20)
    # for link in takewhile(lambda link:link in links and datetime.datetime.now() <= endTime,links):
    for link in links:
        print(count1," link: ",link)
        try:
            
            lsearch=requests.get(link,timeout=5)
            soup1 = BeautifulSoup(lsearch.text, 'html.parser')
        except requests.exceptions.Timeout:
            print('The request timed out')
            continue
        except requests.ConnectionError as e:
            print("Connection Error....")
            sleep(8)
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            sleep(5)
            continue
        except:
            continue
        # print("Here before soup1")
        
        child_soup=soup1.findAll("div")
        
        for i in child_soup:
            
            
            websentences = tokenize_sentence(i.text)
            for y in websentences: 
            #print(i.text)
                # endTime = datetime.datetime.now() + datetime.timedelta(seconds=7)
                # if datetime.datetime.now() >= endTime:
                #     time=1
                #     break
                if txt in y:
                    plagcount=1
                    
                    break
                elif similar(y,txt) >= 0.6:
                    #print("Plagiarism: 90%")
                    #print(txt)
                    
                    plagcount=1
                    break
            
        if plagcount== 1:
            sentancematch.value+=1
            linksmatch.append(link)
            matchwordcount.append(txt)
            #sentancearr.append(txt)
            print("Link:",link)
            print("Text:",txt)
            searchedlink=link  #only for print
            sentencelist.append(txt)
            
            break
        # else:
            
        #     if searchedlink != "":
        #         if oldlink(txt) == 1:
        #             sentancematch.value+=1
        #             break
            

        
        count1=count1+1  #Dekhane ke liye ke konsi link chl rhi hai.

                
            
            

            
        
        
            
    if plagcount==0:
        print("Not Found")
        sentancearr.append(txt)
        # print("Sentences not found: ",sentancearr)
        #notmatched.append(txt)


def map_func(args):
    func, arg, shared_var,shared_list,shared_link,shared_matchword,shared_sentencelist = args
    return func(arg, shared_var,shared_list,shared_link,shared_matchword,shared_sentencelist)

def main_function(txt):
    global all_length
    #global sentancearr
    
    tokens=[]
    tokenscleaned=[]
    clean_text=tokenize_sentence(txt)
    for token in clean_text:
        token=token.replace('\n','')
        if token == '':
            pass
        else:
            tokens.append(token)
    for tokenclean in tokens:
        if len(tokenclean.split()) > 6:
            tokenscleaned.append(tokenclean)
    # for tokenclean in tokenscleaned:
    #     print(tokenclean)
    all_length=len(tokenscleaned)
    allwords1=' '.join(tokenscleaned)
    allwordsnum=len(allwords1.split())
    print(all_length)
    #print(tokenscleaned)
    with multiprocessing.Manager() as manager:
        sentancematch = manager.Value('i', 0)
        sentancearr=manager.list()
        linksmatch=manager.list()
        matchwordcount=manager.list()
        sentencelist=manager.list()

        pool = multiprocessing.Pool()
        #pool.map(plagiarismchecker, tokenscleaned)
        results=pool.map(map_func,[(plagiarismchecker,arg,sentancematch,sentancearr,linksmatch,matchwordcount,sentencelist) for arg in tokenscleaned])
        results2=pool.map(map_func,[(rechecking,arg,sentancematch,sentancearr,linksmatch,matchwordcount,sentencelist) for arg in sentancearr])
        pool.close()
        pool.join()
        print("All Length:",all_length)

        print("Sentence Match:",sentancematch.value)
        # print("Sentance Array:",sentancearr);
        plagiarismpercent=sentancematch.value/all_length
        plagiarismpercent=plagiarismpercent*100
        print("Plagiarism Percentage:",round(plagiarismpercent))
        #print(linksmatch)
        matchwords=' '.join(matchwordcount)
        matchwords=len(matchwords.split())
        print("Count of match words:",matchwords)
        plagiarismpercentword=matchwords/allwordsnum
        plagiarismpercentword=plagiarismpercentword*100
        print("Plagiarism Percentage in words:",round(plagiarismpercentword),"%")
        # print("Sentence Matched:",sentencelist)
        return round(plagiarismpercentword),list(linksmatch)
        # print("Unmatched Sentences:",sentancearr)
        # print("Links Matched:",linksmatch)
        
    # for x in tokenscleaned:
    #     #print(x)
    #     plagiarismchecker(x)

def plagchecker(filepath):

    
    print(filepath,'Yeh hai file path')
    my_text = docx2txt.process(filepath)
    
    clean_text = unicodedata.normalize("NFKD",my_text)
    print('clean texxttt',clean_text)
    p=main_function(clean_text)
    return p
    
    
    
    # print(sentancearr)
    # print(notmatched)
