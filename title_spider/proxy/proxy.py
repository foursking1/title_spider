import requests

proxies = {
  "http": "http://223.95.74.201:8003"
}

r=requests.get("http://icanhazip.com", proxies=proxies)
print r.text
