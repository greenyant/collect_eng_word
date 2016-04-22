#-*- coding: euc-kr -*-
import os, sys
from pyquery import PyQuery as pq
from lxml import etree
import urllib

from .models import *

#echo from engWord import func;func.get_from_file() | python manage.py shell
def get_from_file():
    
    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fn = BASE_DIR+'\\engWord\\dat\\remain.txt'
    
    f_len =  file_len(fn)
    f = open(fn, 'r')
    for k in range(f_len):
        s = f.readline().rstrip()
        w = Word.objects.get_or_create(text = s)
        print s,
    f.close()
    
# write another forms and collins
#echo from engWord import func;func.get_from_collins() | python manage.py shell
def get_from_collins():
    
    #class Encode:
    #    def __init__(self, stdout, enc):
    #        self.stdout = stdout
    #        self.encoding = enc
    #    def write(self, s):
    #        self.stdout.write(s.encode(self.encoding))
    
    #sys.stdout = Encode(sys.stdout, 'utf-8')
    
    collins_url = 'http://www.collinsdictionary.com/dictionary/english-cobuild-learners/'
    words = ['run']
    
    for word in words:
        your_url = collins_url+word
        d = pq(url=your_url)
        print word,
        basic = Word.objects.get(text = word, basic_form=None)
        
        if len(d('.definitions>.hom>.level_0'))==0:
            print 'fail',
        
        for i in range(len(d('.inflected_forms>.infl'))):
            t = d('.inflected_forms>.infl').eq(i).text()
            if t != ',':
                txt = d('.inflected_forms>.infl').eq(i).text()
                transformed = Word()
                transformed.basic_form = basic
                transformed.text = txt
                transformed.save()
                print '('+txt+')',
    
        for i in range(len(d('.definitions>.hom>.level_0'))):
            h = '<ol class="sense_list level_0">' + d('.definitions>.hom>.level_0').eq(i).html() + '</ol>'
            wd = WordDetail()
            wd.word = Word.objects.get(text = word, basic_form=None)
            wd.src = 'collins'
            wd.detail = h
            wd.order = i
            wd.save()
            print '<'+str(i)+'>',
            #print h




