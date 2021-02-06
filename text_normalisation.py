from pymorphy2 import MorphAnalyzer


def filtr_by_word_form(value, good):
    #print('что зашло', value)
    morph = MorphAnalyzer()
    new_str = str()
    value = str.strip(str(value))
    #print('что  после стрип', value)
    value = value.replace('.', '').replace(',', '').replace('!', '').replace(':', ''). \
        replace(';', '').replace(')', '').replace('(', '') \
        .replace('«', '').replace('»', '').replace('"', '').split()
    #print('посде удаления спецсимволов', value)
    #print(type(value))
    for word in value:
        #print('ворд', word)
        word = str.strip(word)
        word = morph.parse(word)[0].normal_form

        if morph.parse(word)[0].tag.POS == 'NOUN' or morph.parse(word)[0].tag.POS == 'ADJF':
            #print(morph.parse(word)[0].inflect({'sing', 'nomn'}))
            if morph.parse(word)[0].inflect({'sing', 'nomn'})== None:
                #print('none', word)
                word = morph.parse(word)[0].normal_form
                new_str = ''.join(word)
            else:
                word = morph.parse(word)[0].inflect({'sing', 'nomn'}).word
                new_str = ''.join(word)
                #print('нормальная форма', word)

        #new_str = ''.join(word)
        #word = morph.parse(word)[0].normal_form

        #print('что получилось', new_str)
        # if morph.parse(word)[0].tag.POS == 'NOUN':
        #   word = morph.parse(word)[0].normal_form
        #  new_str = ''.join(word)
    #print('return', good + ' ' + new_str)
    return good + ' ' + new_str
