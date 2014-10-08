import requests
from bs4 import BeautifulSoup
import webbrowser
import re
import argparse
import sys

parser = argparse.ArgumentParser(description='Spider & Go by SteveL', epilog="Example: %s www.example.com" % sys.argv[0])
parser.add_argument('url', help="URL to Spider")
parser.add_argument('-f', '--firefox', help="All links returned open in Firefox", required=False, action='store_true')
parser.add_argument('-c', '--chrome', help="All links returned open in Chrome", required=False, action='store_true')
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()


def scraper(url, depth=0):
    if not re.search("http.*", url) and re.search("/$", url):
        url = 'http://' + re.sub("/$", "", url)
    elif re.search("/$", url):
        url = re.sub("/$", "", url)
    elif not re.search("http.*", url):
        url = 'http://' + url

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0'}
    verify = requests.head(url, headers=headers, allow_redirects=True)
    if verify.status_code != requests.codes.ok:
        sys.exit("Invalid URL Provided!")

    check = requests.get(url, headers=headers, allow_redirects=True)
    content = check.text
    soup = BeautifulSoup(content)
    links_array = []
    output = []

    for links in soup.find_all('a'):
        links_array.append(links.get('href'))

    url2 = re.sub('www.', '', url)
    url3 = re.sub('http.*?\.', '', url)

    for x in links_array:
        if x is None:
            continue
        if x is not None and not x.startswith('#') and not re.search("^/$", x) and x.startswith('/') or x.startswith('?'):
            output.append(url + x)
        if x is not None and not x.startswith('#') and x.startswith(url) or x.startswith(url2) or x.startswith(url3):
            output.append(x)

    values = set(output)
    openinbrowser = []

    for value in values:
        request = requests.head(value)
        if request.status_code == requests.codes.ok and depth == 0:
            print value
            openinbrowser.append(value)

    if args.firefox:
        browser = 'firefox'
        for go in openinbrowser:
            webbrowser.get(browser).open(go, new=2)

    if args.chrome:
        browser = 'google-chrome'
        for go in openinbrowser:
            webbrowser.get(browser).open(go, new=2)

if __name__ == "__main__":
    scraper(args.url)
