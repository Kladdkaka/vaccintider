import scrapy


class VardguidenSpider(scrapy.Spider):
    name = 'vardguiden'
    allowed_domains = ['1177.se']
    start_urls = [
        'https://www.1177.se/api/hjv/search?g=ChIJlRL-UXszRUYRcIsOKXiQAQM&location=Västra Götalands län&caretype=Vaccination mot covid-19&p=0&batchsize=1000']

    def parse(self, response):
        jsonresponse = response.json()

        print('hits amount: ' + str(len(jsonresponse['SearchHits'])))

        for hit in jsonresponse['SearchHits']:
            url = f'https://www.1177.se{hit["Url"]}'
            yield scrapy.Request(url, callback=self.parse_vardcentral)

    def parse_vardcentral(self, response):
        lines = []

        for e in response.css('.c-alert--content ::text'):
            lines.append(e.get())

        yield {
            'title': response.css('.contact-header__heading::text').get(),
            'address': response.css('.contact-header__address::text').get(),
            'url': response.url,
            'lines': '\n'.join([line.strip() for line in lines])
        }
