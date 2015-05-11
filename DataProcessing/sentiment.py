


from pprint import pprint
import nltk
import yaml
import sys
import os
import re
import csv
import pymongo
from pymongo import MongoClient





class Splitter(object):

    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):

        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):

    def __init__(self):
        pass
        
    def pos_tag(self, sentences):


        pos = [nltk.pos_tag(sentence) for sentence in sentences]

        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

class DictionaryTagger(object):

    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]




    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):

        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N)
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                 
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token: 
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence

def value_of(sentiment):
    if sentiment == 'positive': return 1
    if sentiment == 'negative': return -1
    return 0

def sentence_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)

def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])

def subText(s, t):
    for sub in s:

        if sub in t:
            print sub
            return sub

def main(argv):
    productSet = set([])
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Sentiment']
    productCollection = db['Product']
    sentCollection=db['OverallSentiment']
    count=0
    for row in productCollection.find():
        
        productName = row.get("product_name")
        productSet.add(productName)
    print "In test"
    with open("reviews.csv", "rU") as f:
        print "review"
        reader = csv.reader(f, delimiter="\t")
        
        for row in reader:
            print count
            text= ''.join(row)
            text = text.lower()
            product = subText(productSet, text)

            if product:
                print product
            
                splitter = Splitter()
                postagger = POSTagger()
                dicttagger = DictionaryTagger([ 'positive.yml', 'negative.yml', 
                                    'inc.yml', 'dec.yml', 'inv.yml'])

                splitted_sentences = splitter.split(text)
       

                pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
        

                dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
        
                data={}
                data['name']=product


                    
                print("sentiment loading")
                score = sentiment_score(dict_tagged_sentences)
                res=sentCollection.find_one({'name':product})
                if res:
                    if score<0:
                        sentCollection.update({'_id':res['_id']},{'$set':{'pos': res['pos'], 'neg' : res['neg']+1 , 'neutral': res['neutral']}}, upsert=False, multi=False)
                    if score>0:
                        sentCollection.update({'_id':res['_id']},{'$set':{'pos': res['pos']+1, 'neg' : res['neg'], 'neutral': res['neutral']}}, upsert=False, multi=False)
                    if score==0:
                        sentCollection.update({'_id':res['_id']},{'$set':{'pos': res['pos'], 'neg' : res['neg'], 'neutral': res['neutral']+1}}, upsert=False, multi=False)
                    
                else:
                    if score<0:
                        data['neg']=1
                        data['pos']=0
                        data['neutral']=0
                        sentCollection.insert(data)
                    elif score>0:
                        data['pos']=1
                        data['neg']=0
                        data['neutral']=0
                        sentCollection.insert(data)
                    elif score==0:
                        data['pos']=0
                        data['neg']=0
                        data['neutral']=1

                count+=1
if __name__ == "__main__":
        main(sys.argv)

            


