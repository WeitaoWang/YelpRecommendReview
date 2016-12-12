import json
from pprint import pprint
from itertools import *
from sklearn.feature_extraction.text import TfidfVectorizer

def lines_per_n(f, n):
    for line in f:
        yield ''.join(chain([line], islice(f, n - 1)))

def flatten(jfile):
    for k, v in jfile.items():
        if isinstance(v, list):
            jfile[k] = ','.join(v)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                jfile['%s' % (kk)] = vv
            del jfile[k]
            return jfile

business = []
with open('../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json') as f:
    for chunk in lines_per_n(f, 1):
        jfile = json.loads(chunk)
        if (jfile['city'] == "Pittsburgh") :
            business.append(jfile['business_id'])
print("Getting business_id done!")
print("Start getting reviews")
review = {}
with open('../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json') as f:
    for chunk in lines_per_n(f, 1):
        jfile = json.loads(chunk)
        if jfile['business_id'] in business:
            if jfile['business_id'] in review:
                review[jfile['business_id']] += ' ' + jfile['text']
            else:
                review[jfile['business_id']] = jfile['text']
print("Getting reviews done!")
print("Start writing json file")
with open('rawData.json', 'w') as outfile:
    json.dump(business, outfile)
#with open('data.json', 'w') as outfile:
#    json.dump(review, outfile)
print("Writing file done!")
#pprint(review[0])
#pprint(len(review))


#tf = TfidfVectorizer(analyzer='word', ngram_range=(1,2), min_df = 0, stop_words = 'english')
#tfidf_matrix = tf.fit_transform(review)
#feature_names = tf.get_feature_names()
#print(len(feature_name))