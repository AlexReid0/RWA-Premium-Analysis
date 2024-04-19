import pandas as pd
import re

df = pd.read_csv('yamInfoNew.csv')

def replace_with_dash(text):
    o= re.sub(r'[-\s]+', '-', text).lower()
    if o[0:2] == "d-" or o[0:2]=="s-":
        o = o[2:]
        print(o)
    return o

df['name_new'] = df['name'].apply(replace_with_dash)

df.to_csv('yamInfo_modified.csv', index=False)