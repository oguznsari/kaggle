import os                       # make sure we get all the files
import json
import pandas as pd             # to create a DataFrame
from tqdm import tqdm           # progress bar # make your loops show a smart progress meter - just wrap any iterable with tqdm(iterable)
import re                       # regular expression
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use("ggplot")

# dirs = ["biorxiv_medrxiv"]
# dirs = ["comm_use_subset"]
dirs = ["biorxiv_medrxiv", "comm_use_subset", "custom_license", "noncomm_use_subset"]
docs = []

for d in dirs:
    print(d)
    for file in tqdm(os.listdir(f"{d}/{d}")):
        # print(file)
        file_path = f"{d}/{d}/{file}"
        j = json.load(open(file_path, "rb"))
        # print(j)
        # for key in j:                             # exploring the structure
        #     print(key)
        # # print(j['metadata'])
        # for k in j['metadata']:                   # exploring the structure
        #     print(k)

        title = j['metadata']['title']
        abstract = j['abstract']
        # print(abstract)

        try:                                        # abstract - is empty list
            abstract = j['abstract'][0]             # JSON based database may have same ds for everything ???
        except:
            abstract = ""
            # print(j['abstract'])

        full_text = ""
        for text in j['body_text']:
            # print(text['text'])
            full_text += text['text'] +"\n\n"
        # print(full_text)

        docs.append([title, abstract, full_text])

df = pd.DataFrame(docs, columns=['title', 'abstract', 'full_text'])
# print(df.head())

incubation = df[df['full_text'].str.contains('incubation')]             # 'Series' object has no attribute 'contains' so convert it to "str"
# print(incubation.head())                                                # now we have df only consist of body_text which contains the word incubation


""" I think we can get away with by splitting everything by a period and look in that exact sentence for incubation;
    and if we find incubation in that sentence, look for a duration which is digits """
texts = incubation['full_text'].values
print(len(texts))

incubation_times = []

for t in texts:
    # print(t)
    for sentence in t.split(". "):
        if "incubation" in sentence:
            # print(sentence)
            single_day = re.findall(r" \d{1,2} day", sentence)   # either single or double digits followed by "day"

            if len(single_day) == 1:
                # print(single_day[0])
                # print(sentence)
                num = single_day[0].split(" ")
                incubation_times.append(float(num[1]))
                # print()
                # print()

print(incubation_times)
print(len(incubation_times))

print(f"The mean projected incubation time is {np.mean(incubation_times)} days")
plt.hist(incubation_times, bins= 10)
plt.ylabel("bin counts")
plt.xlabel("incubation time (days)")
plt.show()