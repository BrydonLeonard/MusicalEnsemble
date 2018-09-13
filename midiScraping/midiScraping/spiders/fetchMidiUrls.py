import scrapy
import os
import re


class MidiSpider(scrapy.Spider):
    name = 'midi'

    def start_requests(self):
        urls = [
            'https://freemidi.org/genre-rock',
            'https://freemidi.org/genre-pop',
            'https://freemidi.org/genre-hip-hop-rap',
            'https://freemidi.org/genre-rnb-soul',
            'https://freemidi.org/genre-classical',
            'https://freemidi.org/genre-country',
            'https://freemidi.org/genre-folk',
            'https://freemidi.org/genre-jazz',
            'https://freemidi.org/genre-blues',
            'https://freemidi.org/genre-dance-eletric',
            'https://freemidi.org/genre-folk',
            'https://freemidi.org/genre-punk',
            'https://freemidi.org/genre-newage'
        ]

        if os.path.exists('dl_urls.csv'):
            os.remove('dl_urls.csv')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_genre_page)

    def parse_genre_page(self, response):
        for item in response.css('div.genre-link-text'):
            yield scrapy.Request(url='https://freemidi.org/' + item.css('a::attr(href)').extract_first(), callback=self.parse_band_page)

    def parse_band_page(self, response):
        genres = []
        for a in response.css('div.container-fluid > div.row > div.col-md-12 span > a'):
            link = a.css('a::attr(href)').extract_first()
            if 'genre' in link:
                genres.append(link.replace('genre-', '').lower())

        f = open('dl_urls.csv', 'a', encoding='utf-8')
        for track_div in response.css('div[itemprop=tracks]'):
            pattern = re.compile('download.*?-(.*?)-')
            url = 'https://freemidi.org/getter-' + pattern.findall(track_div.css('a::attr(href)').extract_first().replace('\n', ''))[0]
            title = track_div.css('a::text').extract_first().replace(',', '').replace(' ', '_')

            f.write(title + ',' + '-'.join(genres) + ',' + url)
        f.close()

