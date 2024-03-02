import requests
import json
import pandas as pd
import time
import urllib.parse
import os.path

import sqlite3
import re


def load_data(filepath):
    """
    Cleans returned trials data.
    filepath = 'data/fda.json'
    """

    # Load as a series to handle nested data
    with open(filepath) as json_file:
        data = json.load(json_file)
    results_list_of_dct = []
    for i in range(len(data)):
        #data[i]['results'] is a list of dictionaries
        page_i_result = data[i]['results']
        for dct in page_i_result:
            submission_status_date = dct.get('submissions',{})
            if submission_status_date:
                submission_status_date = submission_status_date[0].get('submission_status_date',{})
            submission_status = dct.get('submissions',{})
            if submission_status:
                submission_status = submission_status[0].get('submission_status',{})
            application_number = dct.get('application_number',{})
            print("DCT IS",dct)
            print("app number",application_number)
            if 'products' in dct:
                brand_name =  dct.get('products',{})[0].get('brand_name',{})
            sponsor_name = dct.get('sponsor_name',{})
            generic_name = None
            substance_name = None
            manufacturer_name = None
            generic_name = dct.get('openfda',{}).get('generic_name',{})
            if generic_name:
                generic_name = generic_name[0]
            substance_name = dct.get('openfda',{}).get('substance_name',{})
            if substance_name:
                substance_name = substance_name[0]
            manufacturer_name = dct.get('openfda',{}).get('manufacturer_name',{})
            if manufacturer_name:
                manufacturer_name = manufacturer_name[0]
            openfda_brand_name = dct.get('openfda',{}).get('brand_name',{})


            drug_dct = {}
            var_lst = ['submission_status_date','submission_status','application_number',\
                   'brand_name','sponsor_name','generic_name','substance_name','manufacturer_name']
            for var in var_lst:
                drug_dct[var] = locals()[var]
            for key in dct:
                if dct[key] == {}:
                    dct[key] == None
            results_list_of_dct.append(drug_dct)
    return results_list_of_dct
    

def get_to_csv(filepath,filename):
    data = load_data(filepath)
    df = pd.DataFrame.from_dict(data)
    df.to_csv(filename, sep=',', index=False, encoding='utf-8')