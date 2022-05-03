import config
import requests

#def my_open_request():
url = config.url_SD + "requests/96203/move_to_trash"
headers = {"authtoken": config.SD_token}
response = requests.delete(url,headers=headers)
print(response.text)

