import scrapy

from datetime import datetime
from jep_data_collector.items import JepItem


class JepSpider(scrapy.Spider):
    name = 'jep'
    allowed_domains = ['openjdk.java.net']
    jep_base_url = 'https://openjdk.java.net/jeps'
    start_urls = [f'{jep_base_url}/0']
    datetime_keys = ['created','updated']
    string_list_keys = ['endorsed_by','reviewed_by']

    def parse(self, response):
        jep_ids = response.xpath('//table[@class = "jeps"]//a/@href').extract()
        for jep_id in jep_ids:
            yield scrapy.Request(url=f'{self.jep_base_url}/{jep_id}', callback=self.parse_jep, cb_kwargs=dict(jep_id=jep_id))

    def parse_jep(self, response, jep_id):
        jep = JepItem()
        jep['id'] = jep_id
        jep['title'] = self.parse_title(response, jep)
        jep['summary'] = self.parse_summary(response, jep)
        jep['full_jep_link'] = response.url
        self.parse_table_rows(response, jep)
        return jep

    def parse_title(self, response, jep):
        return response.xpath('//h1/text()').extract_first().split(':')[1].strip()

    def parse_summary(self, response, jep):
        summaries = response.xpath('//div[@class = "markdown"]/*').getall()
        summaries = [summary.replace('<div class="markdown">','').replace('</div>','').replace('h2','b') for summary in summaries]
        return ''.join(summaries)

    def parse_table_rows(self, response, jep):
        table_rows = response.css('td')
        pairs = (table_rows[pos:pos + 2] for pos in range(0, len(table_rows), 2))
        for pair in pairs:
            key_str = self.extract_first_text(pair[0])
            if key_str is not None:
                key = self.lower_snakecase_ify(key_str)
                if key in jep.fields:
                    value = self.parse_value(key, pair[1])
                    jep[key] = value

    def parse_value(self, key, value):
        if key == 'issue':
            value = self.parse_issue(value)
        else:
            value = self.extract_first_text(value)
            if key in self.datetime_keys:
                value = self.parse_datetime(value)
            if key in self.string_list_keys:
                value = self.parse_string_list(value)
            if key == 'component':
                value = self.parse_component(value)
            if key == 'discussion':
                value = self.parse_discussion(value)
        return value


    def lower_snakecase_ify(self, str):
        return str.lower().replace(' ','_')

    def extract_first_text(self, selector):
        str = selector.xpath('text()').extract_first()
        if str is not None:
            return str.replace('\u2009','')

    def parse_discussion(self, str):
        return str.replace('dash','-').replace('at','@').replace('dot','.').replace(' ','')

    def parse_string_list(self, str):
        return str.split(', ')

    def parse_datetime(self, str):
        return datetime.strptime(str,'%Y/%m/%d %H:%M')

    def parse_component(self, str):
        return str.split('/')

    def parse_issue(self, selector):
        return selector.xpath('a/@href').extract_first()
