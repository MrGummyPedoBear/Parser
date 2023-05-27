from product_scraper.items import Product
import scrapy
import re

class EducaSpider(scrapy.Spider):
    name = "EducaSpider"
    allowed_domains = ["e-revistes.uji.es"]
    #start_urls = ["https://www.e-revistes.uji.es/index.php/artseduca/issue/archive"]
    start_urls = ['https://www.e-revistes.uji.es/index.php/artseduca/article/view/6885']

    def __init__(self, category=None, *args, **kwargs):
        super(EducaSpider, self).__init__(*args, **kwargs)
        self.issn = '2254-0709'
        self.journal = 'ArtsEduca'

    def parse(self, response):
        item = Product()
        s = response.css('h1.page-header::text').get().replace('  ','').replace('\n','')
        if re.match('editorial',s.lower()) or re.match('arteduca',s.lower()):
            return item
        item['title'] = s
        item['url'] = response.url
        item['publisher'] = self.journal
        s = response.css('div.csl-entry::text').extract()[1]
        item['volume'] = re.search('\((\d+)\)',s).group(1)
        item['page'] = re.search(', (\d+-\d+)\.',s).group(1)
        s = response.css('div.list-group-item.date-published').get().split(',')[1]
        item['year'] = re.findall('\d+',s)
        s = ''.join(response.css('div.author strong').extract())
        item['authors'] = re.findall(r'>(.+?)<',s.replace('><',''))
        s = ';'.join(response.css('div.article-author-affilitation::text').extract())
        item['affiliation'] = s.replace('  ','').replace('\n','').split(';')
        item['doi'] = response.css('div.list-group-item.doi a::attr(href)').get()
        item['issn'] = self.issn
        s = response.css('div.value::text').extract()
        item['references'] = ''.join(s).replace('  ','').replace('\n','').replace('\t','').split('\r')
        item['abstract'] = response.css('div.article-abstract p').get().replace('<p>','').replace('</p>','').replace('<br>',' ').replace('  ',' ')
        return item

class ELibarySpider(scrapy.Spider):
    name = "ELibarySpider"
    allowed_domains = ["elibrary.ru"]
    start_urls = ['https://elibrary.ru/item.asp?id=50121924']

    def __init__(self, category=None, *args, **kwargs):
        super(ELibarySpider, self).__init__(*args, **kwargs)
        self.author = 'Шандра Игорь Георгиевич'

    def parse(self, response):
        item = Product()
        arr  = response.xpath('//table').extract()
        s = response.css('p.bigtext').get()
        try:
            item['title'] = re.search('>(.*)</p>', s).group(1)
        except:
            item['title'] = ""

        try:
            item['authors'] = response.css('span.help.pointer font::text').extract()
        except:
            item['authors'] = ""

        s = response.xpath('//a[@title="Содержание выпусков этого журнала"]').get()
        try:
            item['journal'] = re.search('>(.*)</', s).group(1)
        except:
            item['journal'] = ""


        try:
            s = arr[27]
            item['volume'] = re.search('Том:\\xa0<font color="#00008f">(.*)</font>', s).group(1)
        except:
            item['volume'] = ""

        s = response.xpath('//a[@title="Содержание выпуска"]').get()
        try:
            item['issue'] = re.search('>(.*)</', s).group(1)
        except:
            item['issue'] = ""


        try:
            s = arr[27]
            item['pages'] = re.search('Страницы:\\xa0<font color="#00008f">(.*)</font>', s).group(1)
        except:
            item['pages'] = ""

        s = response.xpath('//a[text()="1"]/following-sibling::font').get()
        try:
            item['year'] = re.search('>(.*)</', s).group(1)
        except:
            item['year'] = ""



        try:
            s = arr[28].replace('eISSN', 'eSSN')
            item['pissn'] = re.search('ISSN:\\xa0<font color="#00008f">(.*)</font><span', s).group(1)
        except:
            item['pissn'] = ""

        try:
            item['eissn'] = re.search('eSSN:\\xa0<font color="#00008f">(.*)</font><span', s).group(1)
        except:
            item['eissn'] = ""

        try:
            item['affiliation'] = response.css('span.help1.pointer font::text').extract()
            item['affiliation'].append(response.css('span.help1.pointer font::text').get())
        except:
            item['affiliation'] = ""

        item['abstract'] = response.css('div#abstract1>p::text').get()
        item['url'] = response.url
        return item
