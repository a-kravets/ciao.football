import seleniumwire
from seleniumwire import webdriver
from seleniumwire.utils import decode as decodesw
import json
import re

# we'll use to to get the end of the link after the '/' sign
# we'll use this piece of text to name our files from links
def use_regex(input_text):
    return re.findall("/([^/]*)$", input_text)

# gettig all links and responses
def show_request_urls(driver, target_url):
  # initializing 
  driver.get(target_url)
  # lists for urls and responses
  urls = []
  resps = []

  # looping through requests
  for request in driver.requests:
    # we want to include only links that include 'api' and 'sofascore'
    # because we already know that the links we need
    if all(value in request.url for value in ('api', 'sofascore')):
        # if we find these keywords, we proceed
        urls.append(request.url)


        try:
            data = decodesw(
                request.response.body,
                request.response.headers.get('Content-Encoding', 'identity')
            )
            resp = json.loads(data.decode('utf-8'))
            resps.append(resp)
        except:
            resps.append('error while appending')
  
  return urls, resps

def main():
  driver = webdriver.Firefox(seleniumwire_options={"disable_encoding": True})

  # our target url
  target_url = "https://www.sofascore.com/italy-ukraine/bUbshUb#10752586"

  # executing out func by passing arguments
  urls, resps = show_request_urls(driver, target_url)

  # combining urls and resps into a single list
  urls_resps = list(zip(urls, resps))
  
  # looping over our list in order to save
  # we'll take end of the url as a name of the file

  for i in urls_resps:
    filename = use_regex(i[0]) # we use [0] because it has the following structure [url, resp]
    filename = filename[0] + '.json' # [0] because filename is a list with 1 element and we need str 
    with open(filename, 'w') as f:
        json.dump(i[1], f) # passing [1] because it's for response, i.e. json
  # closing the driver
  driver.close()

if __name__ == '__main__':
  main()