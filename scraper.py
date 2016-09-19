#! /usr/bin/env python

import urllib2
import re
from bs4 import BeautifulSoup as bs
import unicodecsv as csv
import json
import pdb
import sys

PAGES = 50

class DataCrawler():

    def __init__(self, city):
        self.city = sys.argv[1]
        print sys.argv[1]
        self.names = []
        self.areas = []
        self.contacts = []
        self.addresses = []
        self.cuisines = []
        self.costs = []
        self.timings = []
        self.ratings = []
        self.highlights = []


    def scrape(self):

        for page in range(1, PAGES+1):
            print 'Page No:', page
            url = 'https://www.zomato.com/' + self.city + '/restaurants?page=' + str(page)
            try:
                html = urllib2.urlopen(url)
                soup = bs(html.read())
            except:
                print 'City not found.'
                return
	    
            tags = soup.find_all('div', class_ = "col-m-16 search-result-address grey-text nowrap ln22")
            self.addresses = self.addresses + [tag.string.strip() for tag in tags]

            tags = soup.find_all('span', class_ = "col-s-11 col-m-12 nowrap pl0")
            for tag in tags :
                self.cuisines.append(', '.join(map(lambda tag: tag.string.strip(), tag.find_all('a'))))

            tags = soup.find_all('span', class_ = "col-s-11 col-m-12 pl0")
            self.costs = self.costs + [tag.string.strip() for tag in tags]

            tags = soup.find_all('div', class_ = "res-timing clearfix")
            self.timings = self.timings + [tag['title'].strip() for tag in tags]

            tags = soup.find_all('div', class_ = "rating-popup")
            self.ratings = self.ratings + [tag.string.strip() for tag in tags]
                    
	    tags = soup.find_all('a',class_ = "result-title hover_feedback zred bold ln24 fontsize0 ")
            for tag in tags:
                restaurantUrl = tag.get('href')
                self.scrapeRestaurant(restaurantUrl)


    def scrapeRestaurant(self, url):
       
        try:
            html = urllib2.urlopen(url.encode('utf-8'))
        except:
            self.names.append('')
            self.areas.append('')
            self.contacts.append('')
            self.highlights.append('')
            return

        soup = bs(html.read())

        tag = soup.find('a', class_ = "ui large header left")
        self.names.append(unicode(tag.string.strip()).encode('utf-8'))
        print unicode(tag.string.strip()).encode('utf-8')
        tag = soup.find('a', class_ = "left grey-text fontsize3")
        if tag:
            self.areas.append(tag.string.strip())
        else:
            self.areas.append('')

        tag = soup.find_all('span', class_ = "fontsize2 bold zgreen")
        contact = ''
        for t in tag:
            contact = contact + t.text.strip() + ', '
        self.contacts.append(contact.strip().strip(','))

        tag = soup.find_all('div', class_ = "res-info-feature clearfix mb5")
        highlights = ''
        for t in tag:
            highlights = highlights + t.text + ', '
        self.highlights.append(highlights.strip().strip(','))

    
    def saveCSV(self):
        rows = zip(self.names, self.areas, self.addresses, self.costs, self.timings, self.ratings, self.cuisines, self.contacts, self.highlights)
        with open('restaurants.csv', 'w') as f:
            out = csv.writer(f)
            out.writerow(['name', 'area', 'address', 'cost', 'timings', 'rating', 'cuisines', 'contact', 'highlights'])
            for row in rows:
                out.writerow(row)


if __name__ == '__main__':

    d = DataCrawler('hyderabad')
    d.scrape()
    d.saveCSV()
