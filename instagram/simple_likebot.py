import selenium
from selenium import webdriver
from ClientSecrets import Secrets
from time import sleep
from random import randint
from bs4 import BeautifulSoup

# Web service with analytics page?
# Track # raw num followers, ratio of stuff

# workon insta
# (insta)Brians-MacBook-Pro:~ brianb$ python ~/Dropbox/Instagram/simple_likebot.py

# only add < 2000 followers?
# only like if < 10 tags? (real people and not biz promotiion)
# go and slowly add all the 1m who follow magic_fox? or slected? or Samsoe et Samsoe?
# how about you graph the numbers of followers the people who follow magic_fox have.
# bet there is a bunch of bots at the high end, but the vast majority have < 2000 follows.
# These are the real people to target. 


# Look at the people who like the #menswear posts --- follow them and like a photo
# Look at the people who follow the menswear bloggers --- follow them and like a photo



TagList = ['mensfashion', 'menswear', 'menstyle', 'mensstyle', 'menwithclass', 'menwithstyle']

Posts = []

driver = webdriver.Chrome('/Users/brianb/Dropbox/Instagram/chromedriver')

def RandomSleep(low,high):
    sleep(randint(low,high))

def RandomLike(percent):
    NumForUse = 100 - percent
    RanNum = randint(0,100)
    if RanNum > NumForUse:
        return True
    else:
        return False

def Login():
    driver.get('https://www.instagram.com/')
    User = Secrets.get('User')
    Pass = Secrets.get('Pass')
    LoginBut = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')
    LoginBut.click()
    RandomSleep(5,15)
    Username = driver.find_element_by_name('username')
    Password = driver.find_element_by_name('password')
    Username.send_keys(User)
    Password.send_keys(Pass)
    RandomSleep(2,5)
    LoginBut2 = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button')
    LoginBut2.click()

def Tags():
    for Tag in TagList:
        link_count = 0
        tagPage = 'https://www.instagram.com/explore/tags/{}/'.format(Tag)
        driver.get(tagPage)
        try:
            More = driver.find_element_by_class_name('_oidfu')
            More.click()
            RandomSleep(1,5)
        except:
            print('Could not click')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        links = soup.find_all('a',href=True)
        for link in links:
            link = link['href']
            if link.startswith('/p/'):
                Posts.append(link)
                link_count += 1
        print 'Adding {} posts for tag {}'.format(link_count,Tag)
        RandomSleep(10,20)


def PostLike():
    total = len(Posts)
    print '{} posts to like'.format(total)
    count = 1
    for Post in Posts:
        print '{} out of {}'.format(count, total)
        postPage = 'https://www.instagram.com{}'.format(Post)
        driver.get(postPage)
        try:
            Like = driver.find_element_by_class_name('coreSpriteHeartOpen')
        except selenium.common.exceptions.NoSuchElementException as e:
            print 'Already liked this photo'
            count += 1
            continue
        x = RandomLike(50)
        if x == True:
            Like.click()
        count += 1
        RandomSleep(5,10)

Login()
Tags()
PostLike()
print(Posts)

# How many posts?

# Need a try catch block incase you get the same post again ---
# no 'coreSpriteHeartOpen' in that case
# Traceback (most recent call last):
#   File "/Users/brianb/Dropbox/Instagram/simple_likebot.py", line 71, in <module>
#     PostLike()
#   File "/Users/brianb/Dropbox/Instagram/simple_likebot.py", line 63, in PostLike
#     Like = driver.find_element_by_class_name('coreSpriteHeartOpen')
#   File "/Users/brianb/.virtualenvs/insta/lib/python2.7/site-packages/selenium/webdriver/remote/webdriver.py", line 413, in find_element_by_class_name
#     return self.find_element(by=By.CLASS_NAME, value=name)
#   File "/Users/brianb/.virtualenvs/insta/lib/python2.7/site-packages/selenium/webdriver/remote/webdriver.py", line 752, in find_element
#     'value': value})['value']
#   File "/Users/brianb/.virtualenvs/insta/lib/python2.7/site-packages/selenium/webdriver/remote/webdriver.py", line 236, in execute
#     self.error_handler.check_response(response)
#   File "/Users/brianb/.virtualenvs/insta/lib/python2.7/site-packages/selenium/webdriver/remote/errorhandler.py", line 192, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"class name","selector":"coreSpriteHeartOpen"}
#   (Session info: chrome=54.0.2840.98)
#   (Driver info: chromedriver=2.25.426935 (820a95b0b81d33e42712f9198c215f703412e1a1),platform=Mac OS X 10.11.6 x86_64)
