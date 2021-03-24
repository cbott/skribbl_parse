# skribbl_parse

Parse any plaintext file or website into a [skribbl.io](https://skribbl.io/) word list


### Basic usage
```
(venv) skribbl_parse> python main.py README.md
Identified 12 words
-- Skribbl word list --
file, basic, example, usage, main, into, python, wrote, word, parse, list, common
```

### Advanced usage
```
(venv) skribbl_parse> python main.py http://example.com -l 4 -u 12 -d denylists\common_web_words.txt -o words.txt
Identified 7 words
Wrote word list to "words.txt"
```
