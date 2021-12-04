import re

pairs = [
    ('וּ', 'וּ'),
    ('יִ', 'יִ'),
    ('ײַ', 'ײַ'),
    ('וו', 'װ'),
    ('וי', 'ױ'),
    ('יי', 'ײ'),
    ('אַ', 'אַ'),
    ('אָ', 'אָ'),
    ('בֿ', 'בֿ'),
    ('כּ', 'כּ'),
    ('פּ', 'פּ'),
    ('פֿ', 'פֿ'),
    ('שׂ', 'שׂ'),
    ('תּ', 'תּ'),
]

def replace_with_precombined(string):
    for pair in pairs:
        string = re.sub(pair[0], pair[1], string)
    string = re.sub('בּ', 'ב', string) # diacritic not used in YIVO
    string = re.sub('בּ', 'ב', string)
    return string

def replace_with_decomposed(string):
    for pair in pairs:
        string = re.sub(pair[1], pair[0], string)
    string = re.sub('ייַ', 'ײַ', string)
    string = re.sub('בּ', 'ב', string) # diacritic not used in YIVO
    string = re.sub('בּ', 'ב', string)
    return string

def replace_punctuation(string):
    string = re.sub(r"-", r"־", string) # YIVO-style hyphen
    string = re.sub(r'[′׳]', "'", string)
    string = re.sub(r'[″״]', '"', string)
    return string
