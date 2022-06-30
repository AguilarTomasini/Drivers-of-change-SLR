# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 18:23:48 2022
 
@author: mtomasin
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from time import sleep
 
# this function for the getting inforamtion of the web page
def get_paperinfo(url, headers):
 
    #download the page
    response=requests.get(url,headers=headers)
    
    # check successful response
    if response.status_code != 200:
      print('Status code:', response.status_code)
      raise Exception('Failed to fetch web page ')
 
    #parse using beautiful soup
    paper_doc = BeautifulSoup(response.text,'html.parser')
    
    return paper_doc
 
# this function for the extracting information of the tags
def get_tags(doc):
  paper_tag = doc.select('[data-lid]')
  cite_tag = doc.find_all('div', {'class' : 'gs_fl'})#doc.select('[title=Cite] + a')
  link_tag = doc.find_all('h3',{"class" : "gs_rt"})
  author_tag = doc.find_all("div", {"class": "gs_a"})
  results_tag = doc.find_all("div", {"class": "gs_ab_mdw"})  
 
  return paper_tag,cite_tag,link_tag,author_tag, results_tag
 
# it will return the title of the paper
def get_papertitle(paper_tag):
  
  paper_names = []
  
  for tag in paper_tag:
    try:
        paper_names.append(tag.select('h3')[0].get_text())
    except:
        print('No title to retrieve')    
        #paper_names.append('N/A')
  return paper_names
 
# it will return the number of citation of the paper
def get_citecount(cite_tag):
  cite_count = []
  for i in cite_tag:
    cite = i.text
    
    if i is None or cite is None:  # if paper has no citatation then consider 0
        cite_count.append(0)
    else:
        if cite[0] != '[':
            tmp = re.search(r'\d+', cite) # its handle the None type object error and re use to remove the string " cited by " and return only integer value
            if tmp is None :
                cite_count.append(0)
            else:
                cite_count.append(int(tmp.group()))
 
  return cite_count
 
def get_result_count(results_tag):
    for i in results_tag:
        results_count = i.text.split()
        if len(results_count)>1:
            if results_count[0] == 'About':
                return results_count[1]
            if results_count[1] == 'results':
                 return results_count[0]
    return None
    
 
# function for the getting link information
def get_link(link_tag):
 
    links = []
    
    for i in range(len(link_tag)):
        try:
            links.append(link_tag[i].a['href'])
        except:
            links.append('N/A')
    
    return links 
 
# function for the getting author , year and publication information
def get_author_year_publi_info(authors_tag):
    years = []
    publication = []
    authors = []
    for i in range(len(authors_tag)):
        authortag_text = (authors_tag[i].text).split()
        year = re.search(r'\d+', authors_tag[i].text)
        if year == None:
            year = 'N/A'
        else:
            year = int(year.group())
      
        years.append(year)
        publication.append(authortag_text[-1])
        author = authortag_text[0] + ' ' + re.sub(',','', authortag_text[1])
        authors.append(author)
  
    return years , publication, authors
 
 
# creating final repository
paper_repos_dict = {
                    'Paper Title' : [],
                    'Year' : [],
                    'Author' : [],
                    'Citation' : [],
                    'Publication' : [],
                    'Url of paper' : [],
                    'Search words':[]}
 
# adding information in repository
def add_in_paper_repo(papername,year,author,cite,publi,link,search_words):
    paper_repos_dict['Paper Title'].extend(papername)
    paper_repos_dict['Year'].extend(year)
    paper_repos_dict['Author'].extend(author)
    paper_repos_dict['Citation'].extend(cite)
    paper_repos_dict['Publication'].extend(publi)
    paper_repos_dict['Url of paper'].extend(link)
    paper_repos_dict['Search words'].extend(search_words)
    return pd.DataFrame(paper_repos_dict)
 
search_word_hits_dict = {
    'Search word combination': [],
    'Search hits': []
    }
 
def add_in_search_word_hits_repo(swc,hits):
    search_word_hits_dict['Search word combination'].extend(swc)
    search_word_hits_dict['Search hits'].extend(hits)
    return pd.DataFrame(search_word_hits_dict)
 
def wordFrequencies(titles):
    ''' Works for both gsearch and gscholar modules. Creates word frequencies from TITLES object. Creates dictionary (ref. to termmat - term matrix)
        titles: titles [retrieved from gsearch and gscholar modules] '''
 
    import re
    
    text = ''
 
    for t in titles:
        text += t
 
    wordlist = text.split()
    
    wordlist1 = []
    for i in wordlist:
        wordlist1.append(re.sub('[^A-Za-z0-9]', ' ', i.lower()))
 
    wordfreq = []
    for w in wordlist:
        wordfreq.append(wordlist1.count(w))
    
    return {'words': wordlist1, 'freq': wordfreq}
 
 
def makeDistinctWords(title, termmat, length=7):
 
    ''' Creates words and their respective frequenceis for termmat (compares titles to its search string)
        Makes disctinct words matrix - (disctinctwords)
 
        params: title [search query]
                termmat [produced by listOfWordsWithFreqs() method] '''
 
    hv = ['am', 'is', 'are', 'was', 'and', 'were', 'being', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should',
          'may', 'might', 'must', 'can', 'could', 'of', 'for', 'about', 'with', 'on', 'inside', 'under', 'lower', 'upper', 'a', 'an', 'the', 'in', 'new',
          'old', 'through', 'suitable', 'suiit']
 
    words = []
    freq = []
    titlewords = title.split()
 
    idx = []
 
    idx.append(list(termmat.keys())[0])
    idx.append(list(termmat.keys())[1])
    
    for i, j in zip(termmat[idx[0]], termmat[idx[1]]):
        if i in hv:
            next
        elif i in titlewords:
            next
        elif len(i) < length:
            next
        else:
            words.append(i)
            freq.append(j)
 
    if words:
        words_new = []
        freq_new = []
        for i, j in zip(words, freq):
            if i not in words_new:
                words_new.append(i)
                freq_new.append(j)
                            
    return {'words': words_new, 'freq': freq_new}
 
 
 
if __name__ == "__main__":
    from my_fake_useragent import UserAgent
    from datetime import datetime
    from time import time
    import numpy as np
    
    sleep_time = 30
    pages = 5 
    list_of_search_combinations = pd.read_csv('output/drivers_dry_forest_reserachpapers.csv')#.apply(lambda x: x.str.split('+'))
    stop = 0
    
    resume = 1 # if crash, resume from where we stopped
    if resume:
        for key in paper_repos_dict.keys():
            paper_repos_dict[key].extend(pd.read_csv("output/temp_paper_repo.csv", index_col=0)[key].to_list())
        for key in search_word_hits_dict.keys():
            search_word_hits_dict[key].extend(pd.read_csv("output/temp_search_word_hits_repo.csv", index_col=0)[key].to_list())
            
        with open('output/temp_info.txt', 'r') as f:
            f.readline()
            page_lines = int(f.readline().strip().split(':')[1])
            idx_lswc = int(f.readline().strip().split(':')[1])
            if page_lines == list(range(0,5*10,10))[-1]:
                idx_lswc += 1
            f.close()       
    else:
        idx_lswc = 0  
    
    print(f'Conducting paper scraping using {len(list_of_search_combinations[idx_lswc:])} search word combinations.')
    print(f'ETA: {len(list_of_search_combinations[idx_lswc:])*pages*sleep_time/60/60:.2f} hours')
    start = time()
    for j, search_words in enumerate(list_of_search_combinations.values[idx_lswc:]):
        j = j+idx_lswc # only used for keeping track of swc's used
        for i in range(0, pages*10, 10):
            #i=pages
            # get url for the each page
            #url = https://scholar.google.com/scholar?start={}&q=object+detection+in+aerial+image+&hl=en&as_sdt=0,5.format(i)
            url = f'https://scholar.google.com/scholar?start={i}&as_q={search_words[0]}&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=&as_publication=&as_ylo=&as_yhi=&hl=en&as_sdt=0%2C5'
            
            ua = UserAgent()
            header = {'user-agent': ua.random().strip()}
            
            # function for the get content of each page
            doc = get_paperinfo(url, header)
        
            # function for the collecting tags
            paper_tag,cite_tag,link_tag,author_tag, results_tag = get_tags(doc)
            if len(paper_tag) == 0:
                print('Google see you..')
                stop = 1
                break
            # paper title from each page
            papername = get_papertitle(paper_tag)
        
            # year , author , publication of the paper
            year , publication , author = get_author_year_publi_info(author_tag)
        
            # cite count of the paper 
            cite = get_citecount(cite_tag)
        
            # url of the paper
            link = get_link(link_tag)
        
            if i == 0: # only store once
                # results count
                results_count = get_result_count(results_tag)
                # add search word hits and combinations in repo
                if ',' in results_count:
                    results_count = int(results_count.replace(',',''))                  
                results_search_words = add_in_search_word_hits_repo(search_words, [int(results_count)])
                page_max = results_search_words.iloc[-1][1]
            
            
            # add in paper repo dict
            final = add_in_paper_repo(papername,year,author,cite,publication,link,[search_words]*len(link))
        
            
            # Temporary storage of results
            final.to_csv("output/temp_paper_repo.csv") # remove 1 when sure of functionality
            results_search_words.to_csv("output/temp_search_word_hits_repo.csv") # remove 1 when sure of functionality
            
            with open('output/temp_info.txt', 'w') as f: # remove 1 when sure of functionality
                f.write('parameters')
                f.write('\n')
                f.write(f'pages: {i}')
                f.write('\n')
                f.write(f'search_words:{j}')
                f.write('\n')
                f.write(f'Stored {i+10} papers from search word combination {j+1}. Time used: {(time()-start)/60:.2f} min')
            
            # use sleep to avoid status code 429
            if i == 0:
                print(f'Found {results_count} hits using swc {j+1}') # TODO: fix so it dont print None
                print(f'Done scraping page {i+1} with search word combination {j+1}.')
            else:
                print(f'Done scraping page {int((i+10)/10)} with search word combination {j+1}.')
            sleep_time = (60-20)*np.random.random()+20    
            print(f'Sleep for {sleep_time:.2f} seconds... zzZZZZzzZZzzzZZZZ')
            sleep(sleep_time)
            if page_max < i :
                break
        if stop:
            break
        
        print(f'Done using search word combination {j+1}.')
        #print(f'Found {results_count} hits using swc {j+1}') # TODO: fix so it dont print None
        print(f'Time used: {(time()-start)/60:.2f} min') 
        print('######################################')
        print(' ')
    
    if stop == 0:
        print('Done scraping all the papers.')
        print(f'Time used {(time()-start)/60/60} hours')
        
        date = datetime.strftime(datetime.now(), '%d%M%Y_%H%M%S')
        final.to_csv(f"output/{date}_paper_repo.csv")
        results_search_words.to_csv(f"output/{date}_search_word_hits_repo.csv")
    else:
        print('Retreving stopped because of ...')

