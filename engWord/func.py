#-*- coding: euc-kr -*-
import os, sys
from pyquery import PyQuery as pq
from lxml import etree
import urllib
import urllib2,cookielib

from .models import *

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#echo from engWord import func;func.get_from_file() | python manage.py shell
def get_from_file():
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
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fn = BASE_DIR+'\\engWord\\dat\\remain.txt'
    
    f_len =  file_len(fn)
    f = open(fn, 'r')
    
    collins_url = 'http://www.collinsdictionary.com/dictionary/english-cobuild-learners/'
    
    for k in range(f_len):
        word = f.readline().rstrip()
    
        your_url = collins_url+word
        try:
            d = pq(url=your_url)
        except:
            try:
                d = pq(url=your_url)
            except:
                d = pq(url=your_url)
        print word,
        basic = Word.objects.get(text = word, basic_form=None)
        
        if len(d('.definitions>.hom>.level_0'))==0:
            print 'fail',
        
        for i in range(len(d('.inflected_forms>.infl'))):
            txt = d('.inflected_forms>.infl').eq(i).text()
            if txt != ',' and not "'" in txt:
                try:
                    print '('+txt+')',
                    transformed = Word()
                    transformed.basic_form = basic
                    transformed.text = txt
                    transformed.save()
                except:
                    pass
    
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
    f.close()

#echo from engWord import func;func.get_from_wikidicten() | python manage.py shell
def get_from_wikidicten():
    
    wiki_url = 'https://en.wiktionary.org/wiki/'
    
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    
    #words = ['labile','labium','labors','labrum','lacers','laches','lacier','lacing','lacked','lackey','lactic','lactim']
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fn = BASE_DIR+'\\engWord\\dat\\remain_wiki.txt'
    
    f_len =  file_len(fn)
    f = open(fn, 'r')
    
    #for word in words:
    #for k in range(f_len):
    #for k in range(2):
    while True:
        word = f.readline().rstrip()
        if not word: break
        
        your_url = wiki_url+word
        
        fail_flag = False
        print word,
        
        req = urllib2.Request(your_url, headers=hdr)
        try:
            page = urllib2.urlopen(req)
        except:
            try:
                page = urllib2.urlopen(req)
            except:
                try:
                    page = urllib2.urlopen(req)
                except:
                    print 'fail'
                    fail_flag = True
        
        if not fail_flag:
            
            basic = Word.objects.get(text = word, basic_form=None)
            
            html = page.read()
            english_id_index = html.find('id="English"')
            english_start_index = html.rfind('<h2>', 0, english_id_index)
            english_end_index = html.find('<h2>', english_id_index)
            d = pq(html[english_start_index:english_end_index])
            for i in range(len(d('ol'))):
                if d('ol').eq(i).html() == None:
                    print '<'+str(i)+ ', None>'
                else:
                    h = '<ol>'+d('ol').eq(i).html()+'</ol>'
                    
                    wd = WordDetail()
                    wd.word = Word.objects.get(text = word, basic_form=None)
                    wd.src = 'wikidicten'
                    wd.detail = h
                    wd.order = i
                    wd.save()
                    print '<'+str(i)+'>',
        
    f.close()

#echo from engWord import func;func.get_from_wikidictko() | python manage.py shell
def get_from_wikidictko():
    wiki_url = 'https://ko.wiktionary.org/wiki/'
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fn = BASE_DIR+'\\engWord\\dat\\remain_wikiko.txt'
    
    #words = ['I', 'a', 'as', 'to', 'run']
    #words = ['apple']
    
    f = open(fn, 'r')
    
    #for word in words:
        
    while True:
        word = f.readline().rstrip()
        if not word: break
        
        your_url = wiki_url+word
        print word,
    
        try:
            page = urllib.urlopen(your_url)
        except:
            try:
                page = urllib.urlopen(your_url)
            except:
                try:
                    page = urllib.urlopen(your_url)
                except:
                    print 'fail(404)',
                    continue
                    
        basic = Word.objects.get(text = word, basic_form=None)
        html = page.read()
    
        english_id_index = html.find('id=".EC.98.81.EC.96.B4"')
    
        if english_id_index == -1:
            print 'fail',
            continue
    
        english_start_index = html.rfind('<h2>', 0, english_id_index)
        english_end_index = html.find('<h2>', english_id_index)
        eng_html = html[english_start_index:english_end_index]
    
        li_next = 0
        i = 0
        while True:
            li_start = eng_html.find('<li><b>', li_next)
            li_end = eng_html.find('</li>', li_start)
    
            def_str = eng_html[li_start+13:li_end].strip()
            href_next_index = 0
            while True:
                href_start_index = def_str.find('<a', href_next_index)
                if href_start_index == -1:
                    break
                href_end_index = def_str.find('>', href_start_index)
                def_str = def_str[0:href_start_index] + def_str[href_end_index+1:]
                href_next_index+=1
    
            def_str = def_str.replace('</a>','')
            
            wd = WordDetail()
            wd.word = Word.objects.get(text = word, basic_form=None)
            wd.src = 'wikidictko'
            wd.detail = def_str
            wd.order = i
            wd.save()
            print '<'+str(i)+'>',

            li_next = eng_html.find('<li><b>', li_start + 1)
            if li_next == -1:
                break
            i+=1
    
    