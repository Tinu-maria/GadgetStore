from django.test import TestCase

# Create your tests here.

import requests

url = "http://127.0.0.1:8000/"
response = requests.get(url)

response_size = len(response.content)
print("Response size: ", response_size)
print(response.content)

request_size = len(response.request.headers)
print("Request size: ", request_size)
print(response.request.headers)


url = "http://127.0.0.1:8000/"
data = {"name": "sayone"}
response = requests.get(url, data=data)

request_size = len(response.request.body)
print("Request size: ", request_size)
print(response.request.body)


