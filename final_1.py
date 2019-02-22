# -*- coding: cp949 -*-
import requests, re ,sys, os
from optparse import OptionParser
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self,url):
        self.url = url

    def res(self):
        r = requests.get(self.url)
        return r.content

    def soup(self,content):
        s = BeautifulSoup(content,"html.parser")
        return s

    def pins(self,s,m):  ## 노래가사 파일저장
        titles = s.find_all("div",{'id':m})
        for title in titles:
            with open('lyrics.txt','w') as f:
                f.write(title.get_text())  


class My_Option:
    def cnt_str(self,filename):
        with open(filename,'r') as f:
            r_lyrics = f.read().lower()

        r_lyrics = re.sub("[(),']","",r_lyrics)    
        r_lyrics = r_lyrics.split()
        return r_lyrics
    def c_option(self,filename):   ## 노래가사 단어 수를 센다.
        r_lyrics = self.cnt_str(filename) 
        r_dict = dict()
        for r in r_lyrics:
            r_dict[r] = r_lyrics.count(r)
        return r_dict

    def t_option(self,filename):
        r_dict = self.c_option(filename)
        r_dict = sorted(r_dict.items(), key=lambda x: x[1], reverse=True)
        return r_dict[:5]

    def h_option(self,filename):
        r_lyrics = self.cnt_str(filename) 
        r_dict = dict()
        for r in r_lyrics:
            print '{} = {}'.format(r,r_lyrics.count(r)*'*')
          

if __name__ == "__main__":
    url = "https://www.songtexte.com/songtext/freddie-mercury/bohemian-rhapsody-23982857.html"
    lyrics = Crawler(url)
    res = lyrics.res()
    soup = lyrics.soup(res)
    lyrics.pins(soup,"lyrics")

    if len(sys.argv) != 3:
        print 'usage: python [파일이름] {옵션1 | 옵션2 | 옵션3} [대상파일]'
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    my_file = My_Option()

    if option == '-c':
        print my_file.c_option(filename)
    elif option == '-h':
        my_file.h_option(filename)
    elif option == '-t':
    
        print my_file.t_option(filename)
    else:
        print 'unknown option'
        sys.exit(1)

