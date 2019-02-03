import scrapy
import platform
import re
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

ARTICLE = '//div[contains(@class, "thing id-t3")]'
ARTICLE_DATA = '//div[contains(@data-domain, "v.redd.it")]'
ARTICLE_TEXT = '//a[contains(@class, "title may-blank")]/text()'
ARTICLE_LINK = '//a[ contains(@href, "") and \
contains(@class, "title may-blank")]/@href'
NEXT_BTN = '//span[contains(@class, "next-button")]\
//a[contains(@href, "https:")]/@href'


def multi_replace(target_str):
    chars_replace = ['[', ']']
    for char in(chars_replace):
        target_str = target_str.replace(char, '')
    target_str = target_str.replace(':', '-')
    return target_str


def get_score(inp_string):
    score = ''
    pattern = re.compile(r'\d-\d')
    striped_str = multi_replace(inp_string)
    scoreline = pattern.finditer(striped_str)
    for score in scoreline:
        score = score.group(0)
    if score == '':
        score = 'NULL'
    return score


class GoalSpider(scrapy.Spider):
    name = "goal_links"

    def start_requests(self):

        urls = [
            'https://old.reddit.com/r/soccer/?count=0',
        ]

        for url in urls:
            yield SplashRequest(url=url, callback=self.resp_parse)

    def resp_parse(self, response):
        page = response.url.split
        TEAM1 = self.team1
        TEAM2 = self.team2

        if (response.xpath(ARTICLE).extract_first()):

            for idx, selector in enumerate(response.xpath(ARTICLE)):

                link = selector.xpath(ARTICLE_LINK).extract()[idx]
                article_text = multi_replace(
                    selector.xpath(ARTICLE_TEXT).extract()[idx])
                score = get_score(article_text)
                if(score != "NULL" and TEAM1 and TEAM2 in article_text):
                    if('Post' in article_text):
                        pass
                    else:
                        yield{
                            'LINK': link,
                            'TEAM1': TEAM1,
                            'TEAM2': TEAM2,
                            'SCORE': score,
                        }
                else:
                    pass
        else:
            pass

        next_page = response.xpath(NEXT_BTN).extract_first()
        if next_page is None:
            pass
        else:
            yield response.follow(next_page, callback=self.resp_parse)
