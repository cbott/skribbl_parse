#!/usr/bin/env python3.7
# main.py
import argparse
import re
import requests
import sys

from typing import List

from bs4 import BeautifulSoup
from english_words import english_words_lower_set


def download_page_from_url(website_url: str, output_filename: str):
    """ Download a page from URL into the output file """
    site_response = requests.get(website_url)
    with open(output_filename, 'w') as f:
        f.write(site_response.text)


def remove_denylist_words(word_set: set, denylist_file: str):
    """ Remove any word from the word_set that appears in the denylist file

        denylist_file should be formatted as plaintext
        with each word separated by whitespace/newlines
    """
    with open(denylist_file, 'r') as f:
        words_to_remove = set(f.read().lower().split())
    # print(f'Deny list:\n{words_to_remove}')
    return word_set - words_to_remove


def parse_file_to_skribbl(filename: str, denylist: str, min_characters: int, max_characters: int):
    """ Take any text file and return a list of words suitable for a Skribbl.io game """
    with open(filename, 'r') as f:
        contents = f.read()

    # Separate the file into "words"
    soup = BeautifulSoup(contents, 'html.parser')
    document_text = soup.get_text()

    # Remove all non-letters (Skribbl will not like this) and convert to lowercase
    document_text = re.sub(r'[^a-z]+', ' ', document_text, flags=re.IGNORECASE).lower()
    # print("Extracted text:")
    # print(document_text)

    words = set(document_text.split())

    words = set(word for word in words
        # Remove all words whose length is outside of [min_characters, max_characters]
        if len(word) >= min_characters and len(word) <= max_characters
        # Remove non-English words
        and word in english_words_lower_set
    )

    # Remove words that are in a denylist, if specified
    if denylist:
        words = remove_denylist_words(words, denylist)

    return words


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse any plaintext file into a Scribble.io word list')
    parser.add_argument('file', help='File to parse')
    parser.add_argument('--min-characters', '-l', default=4, type=int, help='Remove words with fewer than this number of characters')
    parser.add_argument('--max-characters', '-u', default=12, type=int, help='Remove words with greater than this number of characters')
    parser.add_argument('--denylist-file', '-d', help='Remove any words that are in this file')
    parser.add_argument('--output-file', '-o', help='If specified, write resulting word list to this file instead of printing')
    # TODO: allow for specifying a URL to pull from

    args = parser.parse_args()

    result = parse_file_to_skribbl(args.file, args.denylist_file, args.min_characters, args.max_characters)

    print(f'Identified {len(result)} words')

    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(', '.join(result))
        print(f'Wrote word list to "{args.output_file}"')
    else:
        print('-- Skribbl word list --')
        print(', '.join(result))
