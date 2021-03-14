#!/usr/bin/env python3.7
# main.py

import argparse
import re
import sys
from typing import List
import requests

from bs4 import BeautifulSoup
from english_words import english_words_set

def download_page_from_url(website_url: str, output_filename: str):
    """ Download a page from URL into the output file """
    site_response = requests.get(website_url)
    with open(output_filename, 'w') as f:
        f.write(site_response.text)

def keep_words(main_list: set, words_to_keep: set):
    """ Remove all items not in `words_to_keep` from `main_list` """
    for word in main_list:
        if word not in words_to_keep:
            words.remove(word)


def remove_words(main_list: set, words_to_remove: set):
    """ Remove all items in `words_to_remove` from `main_list` """
    for word in words_to_remove:
        main_list.remove(word)
    return main_list


def parse_file_to_skribbl(filename: str, denylist: str, min_characters: int, max_characters: int):
    """ Take any text file and return a list of words suitable for a Skribbl.io game """
    with open(filename, 'r') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')

    if denylist is None:
        denied_words = []
    else:
        with open(denylist, 'r') as f:
            denied_words = denylist.readlines()

    # Do some logic on the file contents
    # Separate the file into "words"
    document_text = soup.get_text()
    # Remove all non-letters (Skribbl will not like this)
    document_text = re.sub(r'[^a-z]+', ' ', document_text, flags=re.IGNORECASE)
    # print("Extracted text:")
    # print(document_text)

    words = set(document_text.split())

    words = set(word for word in words
        # Remove all words whose length is outside of [min_characters, max_characters]
        if len(word) >= min_characters and len(word) <= max_characters
        # Remove non-English words
        and word in english_words_set
    )

    # Remove words that are in a denylist
    words = remove_words(words, denied_words)

    return words


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse any word list into Scribble.io words')
    parser.add_argument('file', help='File to parse')
    parser.add_argument('--min-characters', '-l', default=4, type=int, help='Remove words with fewer than this number of characters')
    parser.add_argument('--max-characters', '-u', default=11, type=int, help='Remove words with greater than this number of characters')
    parser.add_argument('--denylist-file', '-d', help='Remove any words that are in this file')

    args = parser.parse_args()

    result = parse_file_to_skribbl(args.file, args.denylist_file, args.min_characters, args.max_characters)

    print(', '.join(result))
