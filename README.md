## Scrapy Web crawler
### Overview
This is a spider I created using the Scrapy framework to crawl https://old.reddit.com/r/soccer/ to automate the task of manually searching through the website for external links to certain football matches. r/soccer/ itself lets users submit content such as links, text posts, and images. The spider filters through all of this content looking for the input provided by the user which are two team names, team1 and team2. Team1 represents the home team and team2 the away team. It then checks for any text submitted by users containing both the team names and an expression representing a scoreline eg; 'team1 X-X team2'.

### Requirements
- Scrapy installation https://doc.scrapy.org/en/latest/intro/install.html#installing-scrapy
- Splash installation https://splash.readthedocs.io/en/stable/install.html

### Execute Spider
scrapy crawl goal_links -a team1=[home team] -a team2=[away team] -o [output name].json
    
For example if you want any goal links posted by a user belonging to the match of Manchester United v Fulham:
- scrapy crawl goal_links -a team1=Man -a team2=Ful -o Man_Ful_Links.json




