import json
import codecs
from copy import deepcopy
from datetime import datetime
import hashlib
# !pip install pycountry
# import pycountry
import requests
import pandas as pd


pep_schema={
        "uid": "",
        "name": "",
        "alias_name": [],
        "gender": "",
        "date_of_birth": [],
        "country": [],
        "family-tree": {},
        "designation": "",
        "last_updated": "",
        "address": [
            {
                "complete_address": "",
                "state": "",
                "city": "",
                "country": ""
            }
        ],
        "nns_status": "False",
        "organisation": "",
        "documents": {},
        "source": {
            "Authority": "Peppercat World Leaders list",
            "host_country": "United States",
            "name": "Peppercat World Leaders list",
            "description": "Politically Exposed Persons",
            "type": "PEP",
            "url": "https://raw.githubusercontent.com/peppercatorg/site-build/main/everywhere-legislators.csv",
            "other_urls": []
        },
        "comment": ""
    }


def unsorted_to_sorted(data):
    data=data.tolist()[0].split(',')
    sort_format={'DOB': data[7],
                'DOD': "",
                'catalog': data[0],
                'end': "",
                'enwiki': "",
                'gender': data[6],
                'image': "",
                'person': data[2],
                'personID': "",
                'position': data[1],
                'start': ""}
    return sort_format
    
# def countryname(code):
#     try:
#         pyc = pycountry.countries.get(alpha_2=code)

#         return pyc.name
#     except:
#         return code

def get_hash(n):
    return hashlib.sha256(((n).lower()).encode()).hexdigest()
def alias_name(name):
    alias_list = []
    subname = name.split(' ')
    l = len(subname)
    if l >= 3:
        name1 = subname[l-1] + " " + subname[0]
        name2 = subname[l-2] + " " + subname[0]
        alias_list.append(name1)
        alias_list.append(name2)
    if l == 2:
        name1 = subname[1] + " " + subname[0]
        alias_list.append(name1)

    return alias_list


last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


df = pd.read_csv('https://raw.githubusercontent.com/peppercatorg/site-build/main/everywhere-legislators.csv', sep=';', header=None, error_bad_lines=False)
countt=df.shape[0]
list_=[]
for i in range(1,countt):
    list_.append(df.iloc[i])

final_list=[]
for i in list_:
    sorted_data=unsorted_to_sorted(i)
    if sorted_data['person']!='':
        pep_schema['name'] = sorted_data['person'].capitalize() 
        pep_schema["alias_name"] = alias_name(pep_schema['name'])
        if sorted_data['catalog']!="":
            pep_schema['country']=[]
            pep_schema['country'].append(sorted_data['catalog'])
            pep_schema["address"][0]['country']=sorted_data['catalog']
            pep_schema["address"][0]['complete_address']=sorted_data['catalog']
            pep_schema["source"]["host_country"]=sorted_data['catalog']
        else:
            pass
        if sorted_data['DOB']!="":
            pep_schema['date_of_birth']=[]
            pep_schema['date_of_birth'].append(sorted_data['DOB'])
        else:
            pass
        
        pep_schema['gender']=sorted_data['gender']
        pep_schema['designation']=sorted_data['position']
        pep_schema['uid'] = get_hash(str(pep_schema['name']))
        cc = deepcopy(pep_schema)
        final_list.append(cc)
print(final_list[:10])

with open('peppercatorg.json', 'w', encoding="utf-8") as file:
    json.dump(final_list, file, ensure_ascii=False, indent=4)
