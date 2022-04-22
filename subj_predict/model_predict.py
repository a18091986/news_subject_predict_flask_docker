from single_link_parce import scraper
import re
import dill
import pymorphy2
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from razdel import tokenize
import numpy as np


def model_predict(link=None, text=None):

    print(f'Из функции predict: link:{link}\ntext:{text}')

    cache = {}
    morph = pymorphy2.MorphAnalyzer()

    with open('files/for_save', 'rb') as f:
        data = dill.load(f)

    lda = data["model"]
    common_dictionary = data["common_dictionary"]

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

    stopword_ru = stopwords.words('russian')
    with open('files/stopwords.txt') as f:
        additional_stopwords = [w.strip() for w in f.readlines() if w]

    stopword_ru += additional_stopwords

    if link:
        print('link')
        test_text = scraper(link)
        print(test_text)
    else:
        print('text')
        test_text = [text]
        print(test_text)

    N_topic = 3

    test_text = list(map(clean_text, test_text))
    test_text = list(map(lemmatization, test_text))[0]
    test_text_vector = get_lda_vector(lda, test_text)

    subject = {'0': 'спорт', '1': 'экономика', '2': 'путешествия'}

    # print(test_text_vector)
    # print(np.argmax(test_text_vector))
    # print(subject[str(np.argmax(test_text_vector))])

    # print(f'\n{"*"*100}\nМодель считает, что данная новость:\nна {round(test_text_vector[0]*100)}% про спорт\n'
    #     #       f'на {round(test_text_vector[1]*100)}% про экономику\n'
    #     #       f'на {round(test_text_vector[2]*100)}% про путешествия\n'
    #     #       f'{"*"*100}')

    return test_text_vector

# #4 - экономика(1), 8 - спорт(0), 48 - путешествия(2)
#
# x = lda.show_topics(num_topics=N_topic, num_words=50, formatted=False)
# topics_words = [(tp[0], [wd[0] for wd in tp[1]]) for tp in x]
#
# # Печатаем только слова
# for topic, words in topics_words:
#     print(f"topic_{topic}: " + " ".join(words))
