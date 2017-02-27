import scrapy

class WPSpider(scrapy.Spider):
	name = "wp"
	start_urls = ['http://wiadomosci.wp.pl/kat,140556,title,Marcin-Dubieniecki-Jaroslaw-Kaczynski-nie-interweniowal-w-mojej-sprawie,wid,18713063,wiadomosc.html']
	

	
	def parse(self, response):
		
		print("PARSE")
		more_comments = response.xpath("//a[@class='opAllCom']/@href").extract_first()
		if more_comments is not None:
			print("MORE COMMENTS")
			more_comments = response.urljoin(more_comments)
			yield scrapy.Request(more_comments, callback=self.parse_commies)
		
		if more_comments is None:
			print("NO MORE COMMENTS")
			self.parse_comments(self, response)
		
		next_page = response.xpath("//a[@class='opNext']/@href").extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)

	def parse_commies(self, response):
		print("PARSE COMMENTS")
		print(response.css('.opTresc').extract())
		for text in response.xpath("//div[@class='opTresc']/p/text()").extract():
			yield {
				'text': text.encode('utf-8')
			}
		
