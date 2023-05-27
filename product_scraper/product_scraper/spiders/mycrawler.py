import scrapy
#from product_scraper.product_scraper.items import Product
from product_scraper.items import Product
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class EducaCrawlSpider(CrawlSpider):
    name = "EducaCrawler"
    allowed_domains = ["e-revistes.uji.es"]
    start_urls = ["https://www.e-revistes.uji.es/index.php/artseduca/issue/archive",
                  "https://www.e-revistes.uji.es/index.php/artseduca/issue/archive/2"
                 ]
    #start_urls = ['https://www.e-revistes.uji.es/index.php/artseduca/article/view/6509']

    def __init__(self, category=None, *args, **kwargs):
        super(EducaCrawlSpider, self).__init__(*args, **kwargs)
        self.issn = '2254-0709'
        self.journal = 'ArtsEduca'

    rules = (
        Rule(LinkExtractor(allow=('issue/view',)),),
        Rule(LinkExtractor(allow=('article',),deny=('article/view/\d+/\d+',)), callback='parse_article',),
    )
#,restrict_css=('a.galley-link.mybtn.btn-primary.pdf',)
    def parse_article(self, response):
        item = Product()
        s = response.css('h1.page-header::text').get().replace('  ','').replace('\n','')
        if re.match('editorial',s.lower()) or re.match('arteduca',s.lower()):
            return item
        item['title'] = s
        item['url'] = response.url
        item['publisher'] = self.journal
        s = response.css('div.csl-entry::text').extract()[1]
        item['volume'] = re.search('\((\d+)\)',s).group(1)
        try:
            item['page'] = re.search(', (\d+-\d+)\.',s).group(1)
        except:
            item['page'] = ''
        s = response.css('div.list-group-item.date-published').get().split(',')[1]
        item['year'] = re.findall('\d+',s)[0]
        s = ''.join(response.css('div.author strong').extract())
        item['authors'] = re.findall(r'>(.+?)<',s.replace('><',''))
        s = ';'.join(response.css('div.article-author-affilitation::text').extract())
        item['affiliation'] = s.replace('  ','').replace('\r','').replace('\n','').split(';')
        item['doi'] = response.css('div.list-group-item.doi a::attr(href)').get()
        item['issn'] = self.issn
        s = response.css('div.value::text').extract()
        item['references'] = ''.join(s).replace('  ','').replace('\n','').replace('\t','').split('\r')
        try:
            item['abstract'] = response.css('div.article-abstract p').get().replace('<p>','').replace('</p>','').replace('<br>',' ').replace('  ',' ')
        except:
            item['abstract'] = ''
        return item

class WestCrawlSpider(CrawlSpider): #недоделана т.к. есть shadow-root, а scrapy c этим не работает
    name = "WestCrawler"
    allowed_domains = ["e-revistes.uji.es"]
    start_urls = ["https://www.jstor.org/journal/jinsuissu",
                  "https://www.jstor.org/journal/jinsuissuprac"
                 ]

    def __init__(self, category=None, *args, **kwargs):
        super(EducaCrawlSpider, self).__init__(*args, **kwargs)
        self.issn = '07388934'
        self.eissn = '23324236'
        self.journal = 'Western Risk and Insurance Association'

    rules = (
        Rule(LinkExtractor(allow=('/stable/10.2307',)),),
        Rule(LinkExtractor(allow=('/stable/\d+',),deny=('article/view/\d+/\d+',)), callback='parse_article',),
    )
#,restrict_css=('a.galley-link.mybtn.btn-primary.pdf',)
    def parse_article(self, response):
        item = Product()
        s = response.css('h1.page-header::text').get().replace('  ','').replace('\n','')
        if re.match('editorial',s.lower()) or re.match('arteduca',s.lower()):
            return item
        item['title'] = s
        item['url'] = response.url
        item['publisher'] = self.journal
        s = response.css('div.csl-entry::text').extract()[1]
        item['volume'] = re.search('\((\d+)\)',s).group(1)
        try:
            item['page'] = re.search(', (\d+-\d+)\.',s).group(1)
        except:
            item['page'] = ''
        s = response.css('div.list-group-item.date-published').get().split(',')[1]
        item['year'] = re.findall('\d+',s)[0]
        s = ''.join(response.css('div.author strong').extract())
        item['authors'] = re.findall(r'>(.+?)<',s.replace('><',''))
        s = ';'.join(response.css('div.article-author-affilitation::text').extract())
        item['affiliation'] = s.replace('  ','').replace('\r','').replace('\n','').split(';')
        item['doi'] = response.css('div.list-group-item.doi a::attr(href)').get()
        item['issn'] = self.issn
        s = response.css('div.value::text').extract()
        item['references'] = ''.join(s).replace('  ','').replace('\n','').replace('\t','').split('\r')
        try:
            item['abstract'] = response.css('div.article-abstract p').get().replace('<p>','').replace('</p>','').replace('<br>',' ').replace('  ',' ')
        except:
            item['abstract'] = ''
        return item

class ELibaryCrawlSpider(CrawlSpider):
    name = "ELibaryCrawler"
    allowed_domains = ["elibrary.ru"]
    start_urls = ['https://elibrary.ru/itembox_items.asp?id=1389708']
    #start_urls = ['https://www.e-revistes.uji.es/index.php/artseduca/article/view/6509']

    def __init__(self, category=None, *args, **kwargs):
        super(ELibaryCrawlSpider, self).__init__(*args, **kwargs)

    rules = (
        Rule(LinkExtractor(allow=('elibrary.ru/item.asp?id=',)), callback='print',),
    )

    def print(self,response):
        item = Product()
        item['url'] = response.url
        return item

#,restrict_css=('a.galley-link.mybtn.btn-primary.pdf',)
    def parse_article(self, response):
        item = Product()
        s = response.css('h1.page-header::text').get().replace('  ','').replace('\n','')
        if re.match('editorial',s.lower()) or re.match('arteduca',s.lower()):
            return item
        item['title'] = s
        item['url'] = response.url
        item['publisher'] = self.journal
        s = response.css('div.csl-entry::text').extract()[1]
        item['volume'] = re.search('\((\d+)\)',s).group(1)
        try:
            item['page'] = re.search(', (\d+-\d+)\.',s).group(1)
        except:
            item['page'] = ''
        s = response.css('div.list-group-item.date-published').get().split(',')[1]
        item['year'] = re.findall('\d+',s)[0]
        s = ''.join(response.css('div.author strong').extract())
        item['authors'] = re.findall(r'>(.+?)<',s.replace('><',''))
        s = ';'.join(response.css('div.article-author-affilitation::text').extract())
        item['affiliation'] = s.replace('  ','').replace('\r','').replace('\n','').split(';')
        item['doi'] = response.css('div.list-group-item.doi a::attr(href)').get()
        item['issn'] = self.issn
        s = response.css('div.value::text').extract()
        item['references'] = ''.join(s).replace('  ','').replace('\n','').replace('\t','').split('\r')
        try:
            item['abstract'] = response.css('div.article-abstract p').get().replace('<p>','').replace('</p>','').replace('<br>',' ').replace('  ',' ')
        except:
            item['abstract'] = ''
        return item