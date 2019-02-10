import json
from collections import defaultdict

#Reads in text file for chain

def fb_scrape(filepath):

    json_data = open(filepath).read()

    data = json.loads(json_data)

    fbdict = {}

    for m in data['messages']:
        if "content" in m:
            key = m['sender_name']
            if key in fbdict:
                fbdict[key].append(m['content'])
            else:
                fbdict[key] = [m['content']]

    return fbdict

#Build Chain

def build_chain(fbdict, mchain = defaultdict(dict)):
    for n in fbdict:
        for m in fbdict[n]:
            words = m.split(' ')
            index = 1
            for word in words[index:]:
                key = words[index - 1]
                if n in mchain:
                    if key in mchain[n]:
                        mchain[n][key].append(word)
                    else:
                        mchain[n][key] = [word]
                else:
                    mchain[n][key] = [word]
                index += 1
    
    return mchain

def generate_chain(input,output):
    data = build_chain(fb_scrape(input))
    with open(output + '.json','w') as fp:
        json.dump(data, fp, sort_keys=True, indent=4)
    return
