from pymorphy2 import MorphAnalyzer

def filtr_by_word_form(value ,good):
    morph = MorphAnalyzer()
    new_str = str()
    value = str.strip(value)
    value = value.replace('.', '').replace(',', '').replace('!', '').replace(':', ''). \
        replace(';', '').replace('-', '').split(' ')
    for word in value:
        if morph.parse(word)[0].tag.POS == 'NOUN':
            word = morph.parse(word)[0].normal_form
            new_str = ''.join(word)
    return good + ' ' + new_str