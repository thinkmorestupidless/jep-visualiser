import scrapy
import re


from jep_data_collector.items import JdkItem


class JdkSpider(scrapy.Spider):
    name = 'jdk'
    allowed_domains = ['openjdk.java.net']
    jdk_base_url = 'https://openjdk.java.net/projects/jdk'
    start_urls = [jdk_base_url]
    release_date_pattern = r'\((.*?)\)'
    in_development_string = '(in development)'

    def parse(self, response):
        jdks = response.xpath('//li')
        for jdk in jdks:
            release_date = self.parse_release_date(jdk)
            if release_date is not None:
                version = jdk.xpath('a/@href').extract_first().split('/')[0].strip()
                yield scrapy.Request(url=f'{self.jdk_base_url}/{version}', callback=self.parse_jdk, cb_kwargs=dict(version=version,release_date=release_date))

    def parse_jdk(self, response, version, release_date):
        jdk = JdkItem()
        jdk['version'] = version
        jdk['release_date'] = release_date
        jdk['summary'] = self.parse_summary(response)
        jdk['jeps'] = self.parse_jeps_from_blockquote(response) + self.parse_jeps_from_table(response)
        return jdk

    def parse_summary(self, response):
        paragraphs = response.xpath('//div[@id = "main"]/p').extract()
        paragraphs = [paragraph.replace('\n',' ').replace(u'\xa0',' ') for paragraph in paragraphs]
        return ''.join(paragraphs)
    
    def parse_jeps_from_blockquote(self, response):
        jep_strings = response.xpath('//blockquote/text()').extract()
        return self.clean_jep_strings(jep_strings)

    def parse_jeps_from_table(self, response):
        jep_strings = response.xpath('//table[@class = "jeps"]').css('td:nth-child(1)::text').extract()
        return self.clean_jep_strings(jep_strings)

    def clean_jep_strings(self, jep_strings):
        jeps = [jep_string.split(':')[0].strip() for jep_string in jep_strings]
        jeps = list(filter(len, jeps))
        return jeps

    def parse_release_date(self, version_selector):
        release_date_string = version_selector.xpath('text()').extract_first().strip()
        if re.match(self.release_date_pattern, release_date_string) is not None:
            if release_date_string == self.in_development_string:
                return self.in_development_string
            else:
                return re.search(self.release_date_pattern, release_date_string).group(1)
        else:
            return None
