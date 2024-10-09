import scrapy

class CasemineSpider(scrapy.Spider):
    name = "rs_spider"
    custom_settings = {
        'COOKIES_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    start_urls = ['https://www.casemine.com/judgement/in/6114cfc94653d0031f62ff8c']  # Target URL (Make changes here)

    def parse(self, response):
        # Extract judgment details
        title = response.css('h1.judgement-title::text').get()  # Adjusted selector for the title
        date = response.css('span.judgment-date::text').get()  # Date of the judgment
        summary = response.css('div.judgement-content p::text').getall()  # Extract all paragraphs under judgment content
        
        # Clean up summary by joining the list into a string
        summary_cleaned = ' '.join(summary).strip()

        yield {
            'title': title,
            'date': date,
            'summary': summary_cleaned,
        }
