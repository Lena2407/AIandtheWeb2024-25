'''
Simple Crawler

A simple crawler that creates an index for a given start url and all
its url references that lead to the ssame server. The index is build 
using the whoosh library.
'''

import os
import sys
import requests
from bs4 import BeautifulSoup
import re

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.query import *

TESTURL = 'https://vm009.rz.uos.de/crawl/index.html'

def find_sentence_with_term(text, term):
 
    term_index = text.lower().find(term.lower())
    if term_index == -1:
        return ""

    # Find start of sentence (go backwards to find previous separator or start of text)
    start = term_index
    sentence_separators = '.!?'
    while start > 0 and text[start-1] not in sentence_separators:
        start -= 1
    # Skip leading whitespace
    while start < len(text) and text[start].isspace():
        start += 1

    # Find end of sentence (next separator or end of text)
    end = term_index
    while end < len(text) and text[end] not in sentence_separators:
        end += 1
    if end < len(text):  # include the separator if we found one
        end += 1

    sentence = text[start:end].strip()
    # Truncate if too long
    if len(sentence) > 150:
        return sentence[:147] + "..."
    
    return sentence

def crawl(start_url, search_term=None):
    '''
    Crawls (gets and parses) all the HTML pages on a certain server. 
    Builds an index with the whoosh library, which can be later used 
    to perform searches on the content of the HTML pages.

    Attributes:
        start_url = a string that is a url, which shall be used to start the search.
        search_term = optional term to find in content for teaser generation
    '''
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True), teaser=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    urls = [start_url]
    visited_urls = []

    split_url = start_url.split('/')
    server = split_url[2]
    base_url = split_url[0] + '//' + server

    url_without_html = ''
    split_url.pop()
    for part in split_url:
        url_without_html += part + '/'

    while len(urls) != 0:
        current_url = urls.pop(0)
        visited_urls.append(current_url)

        try:
            print(f"Processing URL: {current_url}")
            response = requests.get(current_url, timeout=3)
            status = response.status_code
            if status != 200:
                print(f"Skipping URL due to non-200 status code: {status}")
                continue

            soup = BeautifulSoup(response._content, 'html.parser')
            current_title = soup.title.text if soup.title else ""

            # Collect all textual content
            all_text = soup.get_text()
            # Combine content by tags for more granular indexing
            tag_contents = {
                'p': " ".join(p.get_text() for p in soup.find_all('p')),
                'pre': " ".join(pre.get_text() for pre in soup.find_all('pre')),
                'h1': " ".join(h1.get_text() for h1 in soup.find_all('h1')),
                'h2': " ".join(h2.get_text() for h2 in soup.find_all('h2')),
                
            }

            # Default teaser logic
            teaser = None
            if search_term:
                # Search for the term in each tag's content
                for tag, content in tag_contents.items():
                    if search_term.lower() in content.lower():
                        teaser = find_sentence_with_term(content, search_term)
                        if teaser:  # If a teaser is found, break
                            break

                if not teaser:  # Fall back if term not found in any tag
                    teaser = find_sentence_with_term(all_text, search_term)
                    if not teaser:
                        teaser = all_text.split(".")[0].strip()
                        if len(teaser) > 100:
                            teaser = teaser[:97] + "..."
            else:
                # If no search term is provided, prioritize <p> tags for teaser
                teaser = tag_contents.get('p', "").split(".")[0].strip()
                if len(teaser) > 100:
                    teaser = teaser[:97] + "..."

            print(f"Generated teaser: {teaser}\n")
            writer.add_document(title=current_title, path=current_url, content=all_text, teaser=teaser)

            for link in soup.find_all('a'):
                if 'href' not in link.attrs:
                    continue
                    
                url = link['href']
                if 'http' in url:
                    if base_url in url and url not in visited_urls:
                        urls.append(url)
                elif url.startswith('/'):
                    url = base_url + url
                    if url not in visited_urls:
                        urls.append(url)
                elif re.search(r'^[a-z0-9]+\.html$', url):
                    url = url_without_html + url
                    if url not in visited_urls:
                        urls.append(url)
                else:
                    print('Did not understand URL:', url)

        except Exception as e:
            print(f"Error processing {current_url}: {str(e)}")
            continue

    writer.commit()
  


def main():
    crawl(TESTURL)

if __name__ == "__main__":
    main()
