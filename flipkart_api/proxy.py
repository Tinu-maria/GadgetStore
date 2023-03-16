import requests
import logging

proxies = {
    "https": "8.219.97.248:80",
}

url = "http://127.0.0.1:8000/api/product/1"

response = requests.get(url, proxies=proxies)

print(response.text)
print(response.json()['price'])

logging.basicConfig(filename='requests.log', level=logging.DEBUG)

logging.debug(f'Request URL: {response.url}')
logging.debug(f'Request headers: {response.request.headers}')
logging.debug(f'Response status code: {response.status_code}')
logging.debug(f'Response headers: {response.headers}')
logging.debug(f'Response content: {response.content}')

# mitmproxy
