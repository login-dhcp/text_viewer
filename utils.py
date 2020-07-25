import numpy as np

NAME = {
    'JP': np.array([]), #TODO
    'KR': np.array(['마노', '히오리', '메구루',
                    '코가네', '마미미', '사쿠야', '유이카', '키리코',
                    '카호', '치요코', '린제', '나츠하', '쥬리',
                    '아마나', '텐카', '치유키',
                    '아사히', '후유코', '메이',
                    '토오루', '마도카', '코이토', '히나나',
                    ]),
    'EN': np.array(['mano', 'hiori', 'meguru',
                    'kogane', 'mamimi', 'sakyua', 'yuika', 'kiriko',
                    'kaho', 'chiyoko', 'rinze', 'natsuha', 'juri',
                    'amana', 'tenka', 'chiyuki',
                    'asahi', 'fuyuko', 'mei',
                    'toru', 'madoka', 'koito', 'hinana', ])
}


# TODO: later use textblob
# -1: ValueError, -2:name not found
def name_text_to_num(name, lang=None):
    if lang is not None:
        if not isinstance(lang, str):
            # raise Warning('inappropriate lang') # TODO find for all langs
            # return -1
            raise ValueError('inappropriate lang')
        lang = lang[:2].upper()
        if not lang in NAME:
            # raise Warning('inappropriate lang') # TODO find for all langs
            # return -1
            raise ValueError('inappropriate lang')
    target = NAME[lang]
    if not isinstance(name, str):
        # return -2
        raise ValueError('inappropriate name')
    name = name.lower()
    if np.isin(name, target):
        return np.argmax(target == name)
    else:
        return -2


def main():
    name = 'Meguru'
    lang = 'en'
    a = name_text_to_num(name, lang)
    print(a)


if __name__ == '__main__':
    main()
