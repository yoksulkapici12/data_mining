import os, sys, glob, re
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import uuid

from config import LINK_LIST_PATH

# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def save_link(url, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url, str(page)]) + "\n")


def download_links_from_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
        start_page = 1
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 1
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max()
            downloaded_url_list = data["url"].to_list()

   
    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    
    first_page_URL="https://www.fmprc.gov.cn/mfa_eng/wjbxw/index.html"
    root_path="https://www.fmprc.gov.cn/mfa_eng/wjbxw/index_"
    collected_url = ""
    page=""
    for pid in range(0,10):
        if pid!=0:
            
            page_URL='{}{}{}'.format(root_path,str(pid),".html")
        else:
            page_URL=first_page_URL
            
            
        resp=requests.get(page_URL)
        soup= bs(resp.content,'html.parser')
       # print(soup)
        counter=1
        for article in soup.find_all("li"):
            news_link = article.find('a')
            ### type of the first 7 news link is different then the rest
            if counter>7:
                collected_url =  "https://www.fmprc.gov.cn/mfa_eng/wjbxw/" + news_link["href"]

                print(collected_url)
                page=pid+1
                
               
            # The following code block saves the collected url and page
            # Save the collected urls one by one so that if an error occurs
            # you do not have to start all over again
            
                if collected_url not in downloaded_url_list:
                    print("\t", collected_url, flush=True)
                    save_link(collected_url, page)
                #########################################
            counter +=1

if __name__ == "__main__":
    download_links_from_index()



