#-*-coding:utf8-*-

from fb2 import PyFb2
from body import MainTag

import sys

import re

# lang detection
from langdetect import detect, detect_langs

# split into sentences
import nltk

reload(sys)
sys.setdefaultencoding("utf-8")


b = PyFb2("fb2-sources/110119.fb2")
root = b.root
mt = MainTag(root)
text = mt.to_text()

text = text.lower()

#print text

text_language = detect(text)

print detect_langs(text)



