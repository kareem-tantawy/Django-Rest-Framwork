import requests

endpoint = "https://httpbin.org/anything"
get_response = requests.get(endpoint)
print(get_response.json())

# {
#   "args": {},
#   "data": "",
#   "files": {},
#   "form": {},
#   "headers": {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate",
#     "Host": "httpbin.org",
#     "User-Agent": "python-requests/2.32.3",
#     "X-Amzn-Trace-Id": "Root=1-67d8958d-3ec0b0020411dee544b5588e"
#   },
#   "json": null,
#   "method": "GET",
#   "origin": "45.241.167.48",
#   "url": "https://httpbin.org/anything"
# }