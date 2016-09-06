"""
Version 1.0 - 5 of september 2016.

This script extracts plasmids sequences from DNASU. Takes a CSV file with a plasmid ID
in each row, and returns a new file with each plasmid sequence in the same position.

The script is far from error-proof. It considers blank spaces in the csv, but other than that,
it doesn't consider the possibility of various results in the DNASU Search, for example.

By default the input file name is "DNASU_IDS.csv" (Place it in the Python working directory before
exceuting the script). 
In line 77 you can modify the input file name. The output file name is DNASU_out.csv, again,you can 
modify it in line 79.

"""

import urllib2
import requests
from BeautifulSoup import BeautifulSoup
import csv

def getURL(page):
    """
    Credit to user Shankar of Stackoverflow for this chunk of code.
    :param page: html of web page
    :return: urls in that page
    """
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote


def getSequence(DNASUID):
    """
    Takes ID as an argument and return the full sequence of the vector as a string without linebreaks or whitespaces
    :param DNASUID:
    :return:
    """
    ID = str(DNASUID)
    DNASU_search_URL = 'https://dnasu.org/DNASU/SearchTemplate.do?searchString='
    DNASU_ID_URL = 'http://dnasu.org/DNASU/'
    Search_url = DNASU_search_URL + ID
    Search_response = requests.get(Search_url)
    Search_HTML = str(BeautifulSoup(Search_response.content))
    Search_URL_list = []

    while True:
        url, n = getURL(Search_HTML)
        Search_HTML = Search_HTML[n:]
        if url:
            Search_URL_list.append(url)
        else:
            break

    ID2 = None

    for urls in Search_URL_list:
        if urls.startswith("GetCloneDetail"):
            ID2 = urls

    Result_URL = DNASU_ID_URL + ID2
    Result_response = requests.get(Result_URL)
    Result_HTML = str(BeautifulSoup(Result_response.content))
    start_marker = Result_HTML.find("Open reading frame")
    start_seq = Result_HTML.find('">', start_marker)
    end_seq = Result_HTML.find("</span>", start_seq)
    Sequence = Result_HTML[start_seq +2: end_seq]
    Sequence = Sequence.replace('\n', '').replace('\r', '')
    return Sequence



with open('DNASU_IDS.csv', 'rb') as f:
    ####Makes file, deleting the previous one if any with the same name.
    f_out = open('DNASU_out.csv', 'w')

    for line in f:
        if line.startswith("ScC"):
            newsearch = getSequence(line)
            #new_rows.append(newsearch)
            ####
            f_out.write(newsearch + "\n") #append + linebreak for csv.
        else:
            ###
            f_out.write("-\n")
            #pass
    ###
    f_out.close()
