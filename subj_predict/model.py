import re
import numpy as np
import pandas as pd
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
from razdel import tokenize  # сегментация русскоязычного текста на токены и предложения https://github.com/natasha/razdel
import pymorphy2  # Морфологический анализатор
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from tqdm import tqdm
tqdm.pandas()
import dill

cache = {}
morph = pymorphy2.MorphAnalyzer()

def clean_text(text):
    '''
    очистка текста

    на выходе очищеный текст
    '''
    if not isinstance(text, str):
        text = str(text)

    text = text.lower()
    text = text.strip('\n').strip('\r').strip('\t')
    text = re.sub("-\s\r\n\|-\s\r\n|\r\n", '', str(text))

    text = re.sub("[0-9]|[-—.,:;_%©«»?*!@#№$^•·&()]|[+=]|[[]|[]]|[/]|", '', text)
    text = re.sub(r"\r\n\t|\n|\\s|\r\t|\\n", ' ', text)
    text = re.sub(r'[\xad]|[\s+]', ' ', text.strip())
    text = re.sub('n', ' ', text)

    return text

def lemmatization(text):
    '''
    лемматизация
        [0] если зашел тип не `str` делаем его `str`
        [1] токенизация предложения через razdel
        [2] проверка есть ли в начале слова '-'
        [3] проверка токена с одного символа
        [4] проверка есть ли данное слово в кэше
        [5] лемматизация слова
        [6] проверка на стоп-слова

    на выходе лист лемматизированых токенов
    '''

    # [0]
    if not isinstance(text, str):
        text = str(text)

    # [1]
    tokens = list(tokenize(text))
    words = [_.text for _ in tokens]

    words_lem = []
    for w in words:
        if w[0] == '-':  # [2]
            w = w[1:]
        if len(w) > 1:  # [3]
            if w in cache:  # [4]
                words_lem.append(cache[w])
            else:  # [5]
                temp_cach = cache[w] = morph.parse(w)[0].normal_form
                words_lem.append(temp_cach)

    words_lem_without_stopwords = [i for i in words_lem if not i in stopword_ru]  # [6]

    return words_lem_without_stopwords

def get_lda_vector(lda, text):
    unseen_doc = common_dictionary.doc2bow(text)
    lda_tuple = lda[unseen_doc]

    not_null_topics = dict(zip([i[0] for i in lda_tuple], [i[1] for i in lda_tuple]))

    output_vector = []
    for i in range(N_topic):
        if i not in not_null_topics:
            output_vector.append(0)
        else:
            output_vector.append(not_null_topics[i])
    return np.array(output_vector)

if __name__ == '__main__':

    news = pd.read_csv('files/train.csv')
    news = news[['bloc', 'text']]

    stopword_ru = stopwords.words('russian')

    with open('files/stopwords.txt') as f:
        additional_stopwords = [w.strip() for w in f.readlines() if w]

    stopword_ru += additional_stopwords

    news['text'] = news['text'].progress_apply(lambda x: clean_text(x))
    news['text'] = news['text'].progress_apply(lambda x: lemmatization(x))

    texts = list(news['text'].values)
    common_dictionary = Dictionary(texts)
    common_corpus = [common_dictionary.doc2bow(text) for text in texts]

    N_topic = 3

    lda = LdaModel(common_corpus, num_topics=N_topic, id2word=common_dictionary, passes=10)

    data = {'model': lda, 'common_dictionary': common_dictionary}
    with open('files/for_save', 'wb') as f:
      dill.dump(data, f)


#     with open('files/test.txt', 'r') as f:
#         test_text = [f.read()]
#
#     N_topic = 5
#
#     test_text = list(map(clean_text, test_text))
#     test_text = list(map(lemmatization, test_text))[0]
#     test_text_vector = get_lda_vector(lda, test_text)
#
#     print(test_text_vector)
#
# 100%|██████████| 6023/6023 [00:02<00:00, 2617.33it/s]
# 100%|██████████| 6023/6023 [00:20<00:00, 295.41it/s]
# [0.0432088  0.43587944 0.04034419 0.04035233 0.44021523]


