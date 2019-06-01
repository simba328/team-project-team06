import math
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import numpy as np
from collections import Counter
from nltk.tag import pos_tag

class keywordfunction:
    def __init__(self, StringBox):
        self._StringBox = StringBox
        nltk.download('averaged_perceptron_tagger')

    def MakeKeyword(self):
        # corpus 전체 말뭉치
        corpus = []
        text_num = []
        number = 0
        for i in self._StringBox:
            corpus.append(i.replace("\n", " "))
            text_num.append(number)
            number += 1

        num_docs = len(corpus)

        v = CountVectorizer(ngram_range=(1, 2), binary=True, stop_words='english', min_df=1)
        vf = v.fit_transform(corpus)

        terms = v.get_feature_names()
        freqs = np.asarray(vf.sum(axis=0).ravel())[0]
        idfs = [math.log10(num_docs / f) for f in freqs]
        custom_weight1 = np.array([1 + math.log10(f) for f in freqs])

        keywords1 = []

        v = CountVectorizer(ngram_range=(1, 2), stop_words='english', vocabulary=terms, min_df=1)
        vf = v.fit_transform(corpus[0:num_docs])
        a = vf.toarray()

        for data in a:
            word_weight = np.copy((np.log10(data + 1) * idfs * custom_weight1))
            # TOP20만 출력
            x = word_weight.argsort()[-20:][::-1]
            keywords1.append(x)

        x1 = np.array(keywords1).flatten()

        # 중복 없애기->집합생성
        dummy = x1.copy().tolist()

        # 중복된거지워주기

        occ = Counter(dummy)
        # 동일한 값의 자료가 몇개인지 파악

        for wid in list(occ.keys()):
            if occ[wid] < 1:
                del occ[wid]
        # 15개 이하로 나온건 다 제거

        # survived 최종 남은 키워드
        survived = {}
        for word in list(occ.keys()):
            for i, k in enumerate(keywords1):
                # 열거해서 정렬
                if word in k:
                    if text_num[i] not in survived:
                        survived[text_num[i]] = [word]
                    else:
                        survived[text_num[i]].append(word)

        finalkeyword = []
        for s in text_num:
            output = [terms[x] for x in survived[s]]
            finalkeyword.append(output)
        # print(finalkeyword)

        tagged_list = []
        for i in finalkeyword:
            tagged_list.append(pos_tag(i))
        # print(tagged_list)

        checkbox = []
        for i in tagged_list:
            wordbox2 = [t[0] for t in i if t[1] == "NN" or t[1] == "NNS"]
            checkbox.append(wordbox2)

        # 중복값 및 의미없는 단어
        finalbox = []
        for i in checkbox:
            resultbox = i
            for k in i:
                for word in resultbox:
                    if k == word:
                        continue
                    elif word in k:
                        i.remove(word)
                    else:
                        continue
            finalbox.append(i)

        return finalbox
