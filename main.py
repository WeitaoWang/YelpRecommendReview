import json
from sklearn.feature_extraction.text import TfidfVectorizer


with open('./rawData.json', 'r') as f:
	review = json.load(f)
business_group = {}
rating_group = {}
rating = {}

#initial data
for i in range(0, len(review)) :
    #get reviews divided by business_group
    if review[i]['business_id'] in business_group:
        business_group[review[i]['business_id']] += ' ' + review[i]['text']
    else:
        business_group[review[i]['business_id']] = review[i]['text']
    #get reviews grouped by business_group and rating
    if review[i]['business_id'] in rating_group:
        if review[i]['stars'] in rating_group[review[i]['business_id']]:
            rating_group[review[i]['business_id']][review[i]['stars']] += ' ' + review[i]['text']
        else:
            rating_group[review[i]['business_id']][review[i]['stars']] = review[i]['text']
    else:
        rating_group[review[i]['business_id']] = {}
    #get reviews by rating stars
    if review[i]['stars'] in rating:
        rating[review[i]['stars']] += ' ' + review[i]['text']
    else:
        rating[review[i]['stars']] = review[i]['text']
print('divide review done')

def process_prase_score(dense):
    episode = dense.tolist()[0]
    phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
    sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
    return sorted_phrase_scores
#Step1
print('Step1')
#get Recommended words by business_id
sdata = []        
for key, value in business_group.items():
    sdata.append(value)

print('get reviews group by business_id done')
#analyze tfidf of reviews
tf2 = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
tfidf_matrix2 = tf2.fit_transform(sdata)
feature_names2 = tf2.get_feature_names()
dense2 = tfidf_matrix2.todense()
print('dense2 len' + str(len(dense2)))
#sort result by tfidf and output sorted result
sorted_phrase_scores2 = process_prase_score(dense2[12])
print(len(sorted_phrase_scores2))
#Set the number of words to show up
for phrase2, score2 in [(feature_names2[word_id], score2) for (word_id, score2) in sorted_phrase_scores2][:50]:
    #Filter single words out
    if len(phrase2.split()) > 1:
        print('{0: <20} {1}'.format(phrase2, score2))
print('-----------------------------')
#Step2
print('Step2')
#get recommended words by rating
data = []
for key, value in rating.items():
    data.append(value)

#analyze tfidf of reviews
tf3 = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
tfidf_matrix3 = tf3.fit_transform(data)
feature_names3 = tf3.get_feature_names()

dense3 = tfidf_matrix3.todense()
print(len(dense3))

#Filter words which appear in three different rating group out
tmp_data_rating = {}
for i in range(len(dense3)):
    episode_tmp = dense3[i].tolist()[0]
    phrase_scores_tmp = [pair3 for pair3 in zip(range(0, len(episode_tmp)), episode_tmp) if pair3[1] > 0]

    sorted_phrase_scores_tmp = sorted(phrase_scores_tmp, key=lambda t: t[1] * -1)
    print(len(sorted_phrase_scores_tmp))
    for phrase3, score3 in [(feature_names3[word_id], score3) for (word_id, score3) in sorted_phrase_scores_tmp][:300]:
        if phrase3 in tmp_data_rating:
            tmp_data_rating[phrase3] += 1
        else:
            tmp_data_rating[phrase3] = 1

data_rating = []
for i in range(len(dense3)):
    episode_tmp = dense3[i].tolist()[0]
    phrase_scores_tmp = [pair3 for pair3 in zip(range(0, len(episode_tmp)), episode_tmp) if pair3[1] > 0]
    tmp = []
    sorted_phrase_scores_tmp = sorted(phrase_scores_tmp, key=lambda t: t[1] * -1)
    print(len(sorted_phrase_scores_tmp))
    for phrase3, score3 in [(feature_names3[word_id], score3) for (word_id, score3) in sorted_phrase_scores_tmp][:300]:
        if tmp_data_rating[phrase3] <= 2:
            tmp.append(phrase3)
    data_rating.append(tmp)
#0: worst rating; 4:best rating
for i in range(len(data_rating)):
    print('####star_rating' + str(i + 1) + '####')
    index = 0
    for data_r in data_rating[i]:
        index += 1
        print(data_r)
        if index == 20:
            break

#Step 3
print('Step3')
#Let's specific on certain business_id, for example, 'diVJtnXItoMymDfJkSAV1w'
index = 0
for key, value in business_group.items():
    if index == 12:
        print(key)
    index += 1
#get reviews of the business_id grouped by rating
certain_business_review = []
for key, value in rating_group.items():
    if key == 'diVJtnXItoMymDfJkSAV1w':
        for k,v in value.items():
            certain_business_review.append(v)
print('done')
print('certain_business_review len' + str(len(certain_business_review)))
#analyze tfidf of reviews based on specific business_id
tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
tfidf_matrix = tf.fit_transform(certain_business_review)
feature_names = tf.get_feature_names()

dense = tfidf_matrix.todense()
print('dense len' + str(len(dense)))
#Filter words which appear in three different rating group out
tmp_freq_word_rating_businessid = {}
for i in range(len(dense)):
    sorted_phrase_scores = process_prase_score(dense[i])
    for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:300]:
        if phrase in tmp_freq_word_rating_businessid:
            tmp_freq_word_rating_businessid[phrase] += 1
        else:
            tmp_freq_word_rating_businessid[phrase] = 1
tmp_distinct_word_rating_businessid = []
for i in range(len(dense)):
    sorted_phrase_scores = process_prase_score(dense[i])
    tmp_data = []
    for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:300]:
        if tmp_freq_word_rating_businessid[phrase] <= 2:
            tmp_data.append(phrase)
    tmp_distinct_word_rating_businessid.append(tmp_data)
#0: worst rating; 4:best rating
for i in range(len(tmp_distinct_word_rating_businessid)):
    print('####star_rating' + str(i + 1) + '####')
    index = 0
    for d in tmp_distinct_word_rating_businessid[i]:
        index += 1
        print(d)
        if index == 20:
            break