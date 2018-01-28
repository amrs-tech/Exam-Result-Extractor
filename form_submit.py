from bs4 import BeautifulSoup
import requests
import urllib.parse as u
import pandas as pd

n = int(input('Enter Number of Students: '))
URL = 'http://gct.ac.in/results'
s = requests.Session()

def fetch(url, data=None):
    if data is None:
        return s.get(url).content
    else:
        return s.post(url, data=data).content

soup = BeautifulSoup(fetch(URL),'lxml')
form = soup.findAll('form')

fields = form[1].findAll('input')

formdata = dict( (field.get('name'), field.get('value')) for field in fields)

sheet = pd.read_csv('/Users/amrs/Desktop/sampel.csv')   #The input CSV file location to read Register Numbers
reg_arr = []
for i in sheet['Register No']:
    reg_arr.append(str(i))

print('\nRegister Numbers submitted. Wait for a while...\n')
print('--------------------------------------------------------------------------------\n')

df = pd.DataFrame()

for regno in reg_arr:      
    formdata['reg_no'] = regno      #register numbers
    formdata['btn'] = 'Submit'

    posturl = u.urljoin(URL, form[1]['action'])

    r = s.post(posturl, data=formdata)

    tempSoup = BeautifulSoup(r.text,'lxml')

    tablediv = tempSoup.find('div', {'class':'result_tbl'})

    tablesoup = BeautifulSoup(str(tablediv),'lxml')
    table = tablesoup.findAll('table')[1:]

    colnames = []
    coldata = []

    for rows in table[1].findAll('tr')[1:]:
        cols = rows.findAll('td')
        for c in cols:
            tempdata = c.find('div')
            coldata.append(tempdata.find(text=True))

    subcode = ['Registration Number','Name']
    for a in range(0,len(coldata),5):
        subcode.append(coldata[a])
    temp = []

    for rows in table[2].findAll('tr'):
        cols = rows.findAll('td')
        for c in cols:
            temp.append(c.find(text=True))
    subcode.append(temp[0])
    
    for rows in table[0].findAll('tr'):
        cols = rows.findAll('td')
        for c in cols:
            colnames.append(c.find(text=True))

    #print('-------------------------------------------------------------------------------')
    reg_name_gradepts = []
    reg_name_gradepts.append(colnames[1])
    reg_name_gradepts.append(colnames[3])
    for a in range(3,len(coldata),5):
        reg_name_gradepts.append(coldata[a])

    #print('-------------------------------------------------------------------------------')
    reg_name_gradepts.append(temp[1])

    df2 = pd.DataFrame([reg_name_gradepts],columns=subcode)
    df = df.append(df2,ignore_index=True)

templist = list(df.columns.values)
colorder = [templist[-1]]+[templist[-2]]+templist[:-2]

df = df[colorder]
df.to_csv('/Users/amrs/Desktop/out.csv')        #The output CSV file location where the Results of Students are stored
print('Successfully created Sheet!\n')
