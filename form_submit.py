from bs4 import BeautifulSoup
import requests
import urllib.parse as u

regno = input('Enter a Register Number : ')
URL = 'http://gct.ac.in/results'
s = requests.Session()

def fetch(url, data=None):
    if data is None:
        return s.get(url).content
    else:
        return s.post(url, data=data).content

soup = BeautifulSoup(fetch(URL),'lxml')
form = soup.findAll('form')
#print(form[1])
fields = form[1].findAll('input')

formdata = dict( (field.get('name'), field.get('value')) for field in fields)

formdata['reg_no'] = regno
formdata['btn'] = 'Submit'

print('Register Number submitted. Wait for a while...\n')
print('------------------------------------------------------------------\n')
posturl = u.urljoin(URL, form[1]['action'])

r = s.post(posturl, data=formdata)

file1 = open('file1.txt','w')

file1.write(r.text)

file1.close()



