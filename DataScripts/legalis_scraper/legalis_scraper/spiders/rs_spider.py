import scrapy

class IndianKanoonSpider(scrapy.Spider):
    name = "rs_spider"
    custom_settings = {
        'COOKIES_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    start_urls = ['https://indiankanoon.org/search/?formInput=Maharashtra%20Real%20estate%20%20%20%20%20%20doctypes%3A%20judgments&pagenum=5']  # Adjust the query as needed

    def parse(self, response):
        # Extract case summaries from the search results
        citations = []
        cntr = 0
        
        for case in response.css('div.result'):  # Extracting citation links
            cntr += 1
            citation_link = case.css('div.hlbottom a.cite_tag::attr(href)').get()
            if citation_link:
                citations.append({
                    'link': response.urljoin(citation_link),
                    'citation_num': cntr
                })
            
            # Extract case details
            title = case.css('div.result_title a::text').getall()  # Title as a list of strings
            link = response.urljoin(case.css('div.result_title a::attr(href)').get())
            summary = case.css('div.headline::text').getall()  # Summary as a list of strings
            source = case.css('div.hlbottom span.docsource::text').get()  # Get the source as a string
            
            yield { #schema
                'title': title,  # Title is a list of strings
                'link': link,  # Absolute URL
                'summary': summary,  # Summary is a list of strings
                'source': source if source else '',  # Ensure source is a string
                'citation_links': citations  # List of citation dictionaries
            }

        # Pagination: follow the link to the next page
        next_page = response.css('a.next::attr(href)').get()  # Adjust for the next page link
        if next_page:
            yield response.follow(next_page, self.parse)
