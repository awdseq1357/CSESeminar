from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from CSESeminar.items import SemesterItem, SeminarItem

class CSESeminarSpider(CrawlSpider):  
    name = "CSESeminar"  
    allowed_domains = ["cse.ust.hk"]  
    start_urls = [  
        "http://www.cse.ust.hk/pg/defenses/pastthesisdef.html"
        #"http://www.cse.ust.hk/pg/defenses/F14"
        #"http://www.cse.ust.hk/pg/defenses/F\d\d"
        #"http://www.cse.ust.hk/pg/defenses/S\d\d"
        #"http://www.cse.ust.hk/pg/defenses/Summer\d\d"
    ]  
    #'[FS(Summer)]\d\d'
    rules = (Rule(LinkExtractor(allow = r'[FS(Summer)]\d\d',restrict_xpaths = ('//div[@id = "maincontent"]'), ), callback = 'parse_item'),)
    

    def parse_item(self, response):
		sel = Selector(response)
		seminarTable = sel.xpath('//div[@id = "maincontent"]//table//tbody')

		seminarRows = seminarTable.xpath('.//tr')
		seminarRows.pop(0)

		items = []
		for row in seminarRows:
			colums = row.xpath('.//td')
			item = SeminarItem()
			item['date'] = colums[0].xpath('text()').extract()
			print colums[0].xpath('text()').extract()
			item['candidate'] = colums[1].xpath('text()').extract()
			item['title'] = colums[2].xpath('text()').extract()
			item['announcement'] = colums[3].xpath('a/text()').extract()
			items.append(item)
			# item[''] 
		return items
    '''
    ## Retrive the links at Thesis archive page
    def parse(self, response):
    	sel = Selector(response)
    	sites = sel.xpath('//div[@id = "maincontent"]//ul/li')

    	items = []
    	for site in sites:
    		colums = site.xpath('a')
    		for colum in colums:
    			item = SemesterItem()
    			item['semester'] = colum.xpath('text()').extract()
    			print item['semester']
    			item['link'] = colum.xpath('@href').extract()
    			items.append(item)
    	return items

   		#filename = response.url.split("/")[-2]
   		#open(filename, 'wb').write(response.body)
	'''

	



