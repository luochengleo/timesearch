#coding=utf8
__author__ = 'luocheng'

from bs4 import BeautifulSoup


class SearchResultPageParser:
    def __init__(self):
        pass

    def cleanResultDiv(self, result):
        return result

    def parse(self, webpage):
        soup = BeautifulSoup(webpage)
        return [str(self.cleanResultDiv(item)) for item in soup.find_all('div', class_='rb')]


    def cleanWebpage(self, input):
        soup = BeautifulSoup(input)
        for item in soup.find_all('script'):
            item.decompose()
        output = str(soup)
        return output


if __name__ == '__main__':
    serpp = SearchResultPageParser()
    serp = open('../temp/yangtuo.html').read()
    fout = open('../temp/yangtuo_extract.html', 'w')
    for item in serpp.parse(serp):
        fout.write(item)
    filter = open('../temp/yangtuo_pure.html', 'w')
    filter.write(serpp.cleanWebpage(serp))
    filter.close()
