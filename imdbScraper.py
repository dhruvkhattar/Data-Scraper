#! /usr/bin/env python

import urllib2
import re
from bs4 import BeautifulSoup as bs
import unicodecsv as csv
import json
import pdb
import re
import sys

PAGES = 50
genres = ['sport', 'action']

class DataCrawler():

    def __init__(self, genre):
        self.genre = genre
        self.names = []
        self.ratings = []
        self.desc = []
        self.directors = []
        self.genres = []

    def scrape(self):

        for page in range(1, PAGES+1):
            print 'Page No:', page
            url = 'http://www.imdb.com/search/title?genres=' + self.genre + '&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2406822102&pf_rd_r=10328PMYFYE70699AW2H&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_1&page=' + str(page) + '&ref_=adv_nxt'
            html = urllib2.urlopen(url)
            soup = bs(html.read())

            tags = soup.find_all('h3', class_ = "lister-item-header")
            for tag in tags:
                self.names.append(tag.a.text.strip())

            tags = soup.find_all('div', class_ = "inline-block ratings-imdb-rating")
            for tag in tags:
                self.ratings.append(tag.strong.text.strip())
            
            tags = soup.find_all('span', class_ = "genre")
            for tag in tags:
                self.genres.append(tag.text.strip())

            tags = soup.find_all('p', class_ = "text-muted")
            ctr = 0
            for tag in tags:
                if ctr % 2 :
                    self.desc.append(tag.text.strip())
                ctr += 1

            tags = soup.find_all(href = re.compile('.*adv_li_dr_0.*'))
            for tag in tags:
                self.directors.append(tag.text.strip())

if __name__ == '__main__':

    for genre in genres:
        d = DataCrawler(genre)
        d.scrape()
