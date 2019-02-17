"""
This modules crawls through 'https://old.reddit.com/r/soccer/?count=0'
and extracts structured data from the web pages.
"""


import scrapy
import platform
import re
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

# Constants declare the HTML layout for data to be extracted
# USER_POST - User submitted post
# USER_POST_TEXT - caption for the post
# USER_POST_LINK - external link included in the post
USER_POST = '//div[contains(@class, "thing id-t3")]'
USER_POST_TEXT = '//a[contains(@class, "title may-blank")]/text()'
USER_POST_LINK = '//a[ contains(@href, "") and \
    contains(@class, "title may-blank")]/@href'
NEXT_PAGE_BTN = '//span[contains(@class, "next-button")]\
    //a[contains(@href, "https:")]/@href'


# Formats text to make it easier to work with
# as users post scorlines in various ways
def multi_replace(target_str):
    chars_replace = ['[', ']', ':']
    for char in(chars_replace):
        target_str = target_str.replace(char, '')
        if char == ':':
            target_str = target_str.replace(char, '-')
    return target_str


# Returns scoreline extracted from text
def get_score(inp_string):
    score = ''
    pattern = re.compile(r'\d-\d')
    scoreline = pattern.finditer(inp_string)
    for score in scoreline:
        score = score.group(0)
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

        # TEAM1 and TEAM2 are user input defined
        TEAM1 = self.team1
        TEAM2 = self.team2

        # Check if there is data in response
        if (response.xpath(USER_POST).extract_first()):

            # Iterate through each user post
            for idx, selector in enumerate(response.xpath(USER_POST)):

                link = selector.xpath(USER_POST_LINK).extract()[idx]
                article_text = multi_replace(
                    selector.xpath(USER_POST_TEXT).extract()[idx])
                score = get_score(article_text)

                if(score
                    and (TEAM1 in article_text)
                    and (TEAM2 in article_text)
                   ):

                    # Check if it is a 'Post' Match thread
                    # which will not contain link to goal highlight
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

        next_page = response.xpath(NEXT_PAGE_BTN).extract_first()
        if next_page is None:
            pass
        else:
            yield response.follow(next_page, callback=self.resp_parse)
