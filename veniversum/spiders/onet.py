import scrapy

class OnetSpider(scrapy.Spider):
	name = "onet"
	start_urls = ['http://poznan.onet.pl/wielkopolskie-20-lat-wiezienia-dla-oprawcy-mlodej-kobiety-z-gniezna/sx76yy9']
	
	def parse(self, response):
		print("PARSE")
		more_comments = response.xpath("//a[@class='k_makeComment']/@href").extract_first()
		if more_comments is not None:
			more_comments = response.urljoin(more_comments)
			yield scrapy.Request(more_comments, callback=self.parse_comments)

	def parse_comments(self, response):
		print("PARSE COMMENTS")
		for post in response.xpath("//span[@class='k_content']"):
			yield {
				'text': ' '.join(post.xpath("text()").extract())
			}
		
		next_page = response.xpath("//a[@class='k_nForum_LinksNext k_makeComment']/@href").extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse_comments)
