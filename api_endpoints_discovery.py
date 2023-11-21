import seleniumwire
from seleniumwire import webdriver
from seleniumwire.utils import decode as decodesw
import json

def show_request_urls(driver, target_url):
  driver.get(target_url)
  urls = []

  for request in driver.requests:
    urls.append({"url": request.url})
  return urls

def show_response(driver, target_url):
  driver.get(target_url)
  resps = []

  for request in driver.requests:
    try:
      data = decodesw(
        request.response.body,
        request.response.headers.get('Content-Encoding', 'identity')
      )
      resp = json.loads(data.decode('utf-8'))
      resps.append(resp)
    except:
      pass
  return resps

def main():
  driver = webdriver.Firefox(seleniumwire_options={"disable_encoding": True})
  target_url = "https://www.sofascore.com/italy-ukraine/bUbshUb#10752586"

  urls = show_request_urls(driver, target_url)
  resps = show_response(driver, target_url)

  keywords = ["api"]

  for url in urls:
    for kw in keywords:
      if all(value in url['url'] for value in ('api', 'sofascore')): # keywords
      #if kw in url['url']:
        if not any(value in url['url'] for value in ('image', 'jpg', 'logo')): # stop words
          print(url)

  with open('match_data.json', 'w') as f:
    json.dump(resps, f)

  driver.close()

if __name__ == '__main__':
  main()