from __future__ import division, unicode_literals 
import codecs
import csv
import string
from bs4 import BeautifulSoup

def get_pages(file_name):

    # Open all the file, and get all top level tags in html file
    f = codecs.open(file_name, 'r', 'utf-8')
    document = BeautifulSoup(f.read(), 'html.parser')
    tags = document.find().find_next_siblings()

    # Column header for csv file
    pages = [["Page", "Category"]]

    # Extract all the liked page's names, and the category of the liked page
    for tag in tags:
        sibling = tag.find_next_sibling()
        if sibling:
            div = sibling.find('div')
            if div:
                text = div.find('div').string
                
                # Includes Arabic or any other language 
                page = [tag.string, text]
                pages.append(page)

                ''' ENGLISH ONLY
                if tag.string.isascii():
                    page = [tag.string, text]
                    pages.append(page)
                '''
    return pages

def write_to_csv(file_name, pages):
    # Take in the file name and the pages column 
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(pages)

# Hardcoded file names for now
pages = get_pages("likePage.html")
write_to_csv('likePages.csv', pages)