"""
twitter bot for scraping web content and retweeting to twitter profile @DonFrog7
"""
import random,time,sys

from lxml.html import fromstring
import nltk
nltk.download('punkt')
import requests
from twitter import OAuth, Twitter
import credentials

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
oauth = OAuth(
        credentials.ACCESS_TOKEN,
        credentials.ACCESS_SECRET,
        credentials.CONSUMER_KEY,
        credentials.CONSUMER_SECRET
    )
t = Twitter(auth=oauth)
#stat = Twitter(stat=statuses)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'
    }

def extract_paratext(paras):
    """Extract text from <p> elemenets and returns a clean, tokenized random
    paragraph."""
    paras = [para.text_content() for para in paras if para.text_content()]
    para = random.choice(paras)
    return tokenizer.tokenize(para)

def extract_text(para):
    """Returns a sufficiently-large random text from a tokenized paragraph,
    if such text exists. Otherwise, returns None."""
    for _ in range(10):
        text = random.choice(para)
        if text and 60 < len(text) < 210:
            return text

    return None

def scrape_coursera():
    """ Scrapes content from coursea blog."""
    url = 'https://blog.coursera.org'
    r = requests.get(url, headers=HEADERS)
    tree = fromstring(r.content)
    links = tree.xpath('//div[@class="recent"]//div[@class="title"]/a/@href')

    for link in links:
        r = requests.get(link, headers=HEADERS)
        blog_tree = fromstring(r.content)
        paras = blog_tree.xpath('//div[@class="entry-content"]/p')
        para = extract_paratext(paras)
        text = extract_text(para)
        if not text:
            continue

        yield '"%s"%s' % (text,link)

def scrape_thenewstack():
    """Scrapes news from thenewstack.io"""
    url = 'https://thenewstack.io/'
    r = requests.get(url, verify=False)
    tree = fromstring(r.content)
    links = tree.xpath('//div[@class="normalstory-box"]/header/h2/a/@href')
    for link in links:
        r = request.get(link,verify=False)
        tree=fromstring(r.content)
        paras=tree.xpath('//div[@class="post-content"]/p')
        para = extract_paratext(paras)
        text = extract_text(para)
        if not text:
            continue
        yield '"%s"%s' % (text,link)

def scrape_wiki():
    url = ""
    r = requests.get(url, headers=HEADER)
    tree = fromstring(r.content)
    links = tree.xpath('//div[@class=""]/header/h2/a/@href')
    para = extract_paratest(paras)
    text = extract_text(para)
    if not text:
        continue
    yield '"%s"s%' %(text,link)


def main():
    """Encompass the main loop of the bot"""
    print('---Bot Started---\n')
    news_funcs = ['scrape_coursera','scrape_thenewstack']
    news_iterators = []
    for func in news_funcs:
        news_iterators.append(globals()[func]())
    for i, iterator in enumerate(news_iterators):
        try:
            tweet = next(iterator)
            t.statuses.update(status=tweet)
            print(tweet, end = '\n\n')
            time.sleep(300)
        except StopIteration:
            news_iterators[i] = globals()[news_funcs[i]]()

if __name__ == "__main__":
    main()
