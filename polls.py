import requests
import lxml.html as lh
import pandas as pd

root = 'https://www.wahlrecht.de/umfragen/'
insts = [
  'allensbach',
  'emnid',
  'politbarometer',
  'gms',
  'dimap',
  'insa',
  'yougov'
]

def getUrl(inst):
  return root + inst + '.htm'

def getData(inst):
  # Create a handle, page, to handle the contents of the website
  page = requests.get(getUrl(inst))

  # Store the contents of the website under doc
  doc = lh.fromstring(page.content)

  # Create empty list
  headers=[]
  data=[]
  headers.append('date')

  # Parse headers header
  theader = doc.xpath('/html/body/table/thead/tr')

  # Parse body
  tbody = doc.xpath('/html/body/table/tbody')

  # store headers in an empty list
  for t in theader[0]:
    name=t.text_content()
    if len(name) > 1 and name != 'Datum':
      headers.append(name)

  # loop through rows
  for r in tbody[0]:
    row = []

    # loop through cells
    for t in r:
      name=t.text_content()

      # exclude \ cells but include NaN
      if len(name) > 1 or name in ['?', '–']:
        # print('this is the name: ' + name)
        row.append(name)

    zipbObj = zip(headers, row)
    datadict = dict(zipbObj)
    data.append(datadict)

  # create data frame from dictionaries
  polls = pd.DataFrame(data)
  polls['Institut'] = inst

  # drop last row as its bundestagswahl
  polls = polls.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
  return polls

# print one header
for i in insts:
  results = getData(i)
  results.to_csv(
    r'/Users/henrythierhoff/Desktop/polls/' + i + '.csv',
    index=None, header=True, sep=";")


