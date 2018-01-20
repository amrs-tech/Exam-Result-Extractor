from bs4 import BeautifulSoup
import requests
import urllib.parse as u

#regno = input('Enter a Register Number : ')
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

formdata['reg_no'] = '1517101'#regno
formdata['btn'] = 'Submit'

print('Register Number submitted. Wait for a while...\n')
print('--------------------------------------------------------------------------------\n')
posturl = u.urljoin(URL, form[1]['action'])

r = s.post(posturl, data=formdata)

'''file1 = open('file1.txt','w')

file1.write(r.text)

file1.close()'''

temp = BeautifulSoup(r.text,'lxml')

tablediv = temp.find('div', {'class':'result_tbl'})
#print(temp)
tablesoup = BeautifulSoup(str(tablediv),'lxml')
table = tablesoup.findAll('table')[1:]

for rows in table[0].findAll('tr'):
    cols = rows.findAll('td')
    for c in cols:
        print(c.find(text=True), end='\t')
    print('')
print('-------------------------------------------------------------------------------')

row1 = table[1].find('tr')

for c in row1.findAll('td'):
    print(c.find(text=True),end='\t')
print('')
print('-------------------------------------------------------------------------------')

for rows in table[1].findAll('tr')[1:]:
    cols = rows.findAll('td')
    for c in cols:
        tempdata = c.find('div')
        print(tempdata.find(text=True), end='\t\t')
    print('')
print('')

for rows in table[2].findAll('tr'):
    cols = rows.findAll('td')
    for c in cols:
        print(c.find(text=True),end='\t')
print('\n')
