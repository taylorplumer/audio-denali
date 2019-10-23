# Import required modules
import requests
from bs4 import BeautifulSoup
import urllib.request


def convert_to_soup(url):
    # Use requests to get the contents
    r = requests.get(url)

    # Get the text of the contents
    html_content = r.text

    # Convert the html content into a beautiful soup object
    soup = BeautifulSoup(html_content, 'lxml')
    
    return soup


def parse_addresses(soup):
    # Find all of the spans with the class of "playlist"
    spans = soup.find_all('span', {'class': 'playlist'})

    # Parse spans to pull out addresses for mp3
    addresses = []
    for span in spans:
        links = span.find_all('a')
        for link in links:
            addresses.append(str(link['href']).replace(' ', '%20')) # %20 instead of a space
    
    return addresses

def download_audio(addresses):
    for address in addresses:
        name = 'Audio/' + address[37:]
        urllib.request.urlretrieve(address, name)


if __name__ == '__main__':
    try:
        os.makedirs('Audio')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
            
    url = 'http://www.alaska.org/guide/denali-park-guide'
    
    soup = convert_to_soup(url)
    
    addresses = parse_addresses(soup)
    
    download_audio(addresses)

