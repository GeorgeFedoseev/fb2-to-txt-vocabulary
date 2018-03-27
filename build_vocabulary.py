#-*-coding:utf8-*-

from fb2 import PyFb2
from body import MainTag

import sys
import os

import re

# lang detection
from langdetect import detect

# split into sentences
import nltk 

from multiprocessing.pool import ThreadPool
from tqdm import tqdm # progressbar

reload(sys)
sys.setdefaultencoding("utf-8")


curr_dir_path = os.path.dirname(os.path.realpath(__file__))
FB2_DIR_PATH = os.path.join(curr_dir_path, "fb2-sources")
NUM_THREADS = 1


def build_vocabulary(output_path='vocabulary.txt'):

    # init lang detetor
    detect('test')
    

    stats_total_books = 0

        

    pbar = tqdm(total=len(os.listdir(FB2_DIR_PATH)))

    sent_detector = nltk.data.load('russian.pickle') 

    def process_book(b):
        sentences = []

        item_path = os.path.join(FB2_DIR_PATH, b)

        pbar.update(1)

        if item_path.split(".")[-1] != "fb2":
            return []



        try:
            b = PyFb2(item_path)
            root = b.root
            mt = MainTag(root)
        except:
            print 'failed to read book %s' % item_path
            return []

        text = mt.to_text()               

        #print text

        text_language = detect(text[0:1500])
        if text_language != "ru":
            print 'skip not russian text (%s)' % text_language
            return []

        
        for sent in sent_detector.tokenize(text):

            # convert linebreaks to spaces                    
            sent = sent.replace("\n", " ")
            # strip double spaces
            sent = re.sub(' +', ' ', sent)
            sent = sent.lower()
            sent = re.sub(u'[^а-яё ]', '', sent)
            sent = sent.strip()
            #print sent
            sentences.append(sent)

        
        return sentences

    
    pool = ThreadPool(NUM_THREADS)
    texts = pool.map(process_book, os.listdir(FB2_DIR_PATH))

    sentences = []

    for text in texts:
        for sentence in text:
            sentences.append(sentence)

    print 'Wrote %i sentences to %s' % (len(sentences), output_path)

    f = open(output_path, 'w+')
    f.write('\n'.join(sentences))    
    f.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        build_vocabulary()
    else:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print('USAGE: python build_vocabulary.py <vocabulary_output_file>')
        else:
            build_vocabulary(sys.argv[1])
        

