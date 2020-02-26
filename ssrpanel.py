import requests
import os

url = os.getenv('URL')
userurl = os.getenv('USERURL')
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}
email = os.getenv('EMAIL')
passwd = os.getenv('PASSWD')
data = {'email': email, 'passwd': passwd}
session = requests.session()
respond = session.post(url, headers = headers, data = data)
userrespond = session.get(userurl, headers = headers, cookies = respond.cookies)
checkinurl = os.getenv('CHECKINURL')
checkinrepond = session.post(checkinurl, headers = headers, cookies = respond.cookies)
print(checkinrepond.text)
