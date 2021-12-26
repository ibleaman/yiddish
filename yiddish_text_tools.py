# Functions for processing Yiddish text, written in the YIVO orthography
# Author: Isaac L. Bleaman (bleaman@berkeley.edu)

import re
from urllib.request import urlopen
import pandas as pd

##########
# encoding
##########

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
    string = re.sub('ייַ', 'ײַ', string) # the double yud char exists ONLY in this context
    string = re.sub('בּ', 'ב', string) # diacritic not used in YIVO
    string = re.sub('בּ', 'ב', string)
    return string

def replace_punctuation(string):
    string = re.sub(r"-", r"־", string) # YIVO-style hyphen
    string = re.sub(r'[′׳]', "'", string) # more common punct for abbreviations
    string = re.sub(r'[″״]', '"', string)
    return string

def strip_diacritics(string): # and replace with decomposed
    string = replace_with_decomposed(string)
    return re.sub(r'[ִַַָּּּּֿֿׂ]', '', string)
    
##########################################
# transliteration/romanization and reverse
##########################################

translit_table = [ # all are precombined
    ('א', ''),
    ('אַ', 'a'),
    ('אָ', 'o'),
    ('ב', 'b'),
    ('בֿ', 'v'),
    ('ג', 'g'),
    ('דזש', 'dzh'),
    # ('דז', 'dz'), # phonemic status doubtful
    ('ד', 'd'),
    ('ה', 'h'),
    ('ו', 'u'),
    ('וּ', 'u'),
    ('װ', 'v'),
    ('ױ', 'oy'),
    ('זש', 'zh'),
    ('ז', 'z'),
    ('ח', 'kh'),
    ('טש', 'tsh'),
    ('ט', 't'),
    ('י', 'j'),
    ('יִ', 'i'),
    ('ײ', 'ey'),
    ('ײַ', 'ay'),
    ('כ', 'kh'),
    ('כּ', 'k'),
    ('ך', 'kh'),
    ('ל', 'l'),
    ('מ', 'm'),
    ('ם', 'm'),
    ('נ', 'n'),
    ('ן', 'n'),
    ('ס', 's'),
    ('ע', 'e'),
    ('פּ', 'p'),
    ('פֿ', 'f'),
    ('ף', 'f'),
    ('צ', 'ts'),
    ('ץ', 'ts'),
    ('ק', 'k'),
    ('ר', 'r'),
    ('ש', 'sh'),
    ('שׂ', 's'),
    ('תּ', 't'),
    ('ת', 's'),
    ('־', '-'),
]

def transliterate(string):
    romanized = replace_with_precombined(string)

    for pair in translit_table:
        romanized = re.sub(pair[0], pair[1], romanized)

    romanized = re.sub(r'j$', 'i', romanized)
    romanized = re.sub(r'j(?![aeiou])', 'i', romanized)
    romanized = re.sub('j', 'y', romanized)
    return romanized

reverse_translit_table = [ # to precombined
    (r'\bay', 'אײַ'),
    (r'\bey', 'אײ'),
    (r'\boy', 'אױ'),
    (r'\bu', 'או'),
    (r'\bi', 'אי'),
    (r'kh\b', 'ך'),
    (r'm\b', 'ם'),
    (r'n\b', 'ן'),
    (r'f\b', 'ף'),
    (r'ts\b', 'ץ'),
    ('ayi', 'ײַיִ'), # מאַלײַיִש
    ('eyi', 'ײיִ'), # פּאַרטײיִש, שנײיִק
    ('oyi', 'ױיִ'), # פֿרױיִש
    ('ay', 'ײַ'),
    ('ey', 'ײ'),
    ('oy', 'ױ'),
    ('zh', 'זש'),
    ('kh', 'כ'),
    ('sh', 'ש'), # דײַטש, *דײַצה
    ('ts', 'צ'),
    ('ia', 'יִאַ'), # ?
    ('ai', 'אַיִ'), # יודאַיִסטיק
    ('ie', 'יִע'), # פֿריִער, בליִען, קיִעװ
    ('ei', 'עיִ'), # העברעיִש, פֿעיִק
    ('ii', 'יִיִ'), # װאַריִיִרן, פֿריִיִק, אַליִיִרט
    ('io', 'יִאָ'), # טריִאָ
    ('oi', 'אָיִ'), # דאָיִק
    ('iu', 'יִו'), # בליִונג, באַציִונג
    ('ui', 'ויִ'), # גראַדויִר
    ('iyi', 'יִייִ'), # ?
    ('yi', 'ייִ'),
    ('iy', 'יִי'), # ?
    ('uvu', 'וּװוּ'), # פּרוּװוּנג, צוּװוּקס
    ('uv', 'וּװ'),
    ('vu', 'װוּ'),
    ('uu', 'וּו'), # טוּונג, דוּומװיראַט
    ('uy', 'וּי'), # בורזשוּי
    ('a', 'אַ'),
    ('b', 'ב'),
    ('d', 'ד'),
    ('e', 'ע'),
    ('f', 'פֿ'),
    ('g', 'ג'),
    ('h', 'ה'),
    ('i', 'י'),
    ('k', 'ק'),
    ('l', 'ל'),
    ('m', 'מ'),
    ('n', 'נ'),
    ('o', 'אָ'),
    ('p', 'פּ'),
    ('r', 'ר'),
    ('s', 'ס'),
    ('t', 'ט'),
    ('u', 'ו'),
    ('v', 'װ'),
    ('y', 'י'),
    ('z', 'ז'),
    (r'ך(\'|")', r'כ\1'), # fix mistakes: for abbreviations/acronyms
    (r'ם(\'|")', r'מ\1'),
    (r'ן(\'|")', r'נ\1'),
    (r'ף(\'|")', r'פֿ\1'),
    (r'ץ(\'|")', r'צ\1'),
]

reverse_translit_exceptions = [
    # unpredicted shtumer alef
    (r'\bfarey', 'פֿאַראײ'), # פֿאַראײניקט, פֿאַראײביקן
    (r'\bantiintel', 'אַנטיאינטעל'), # אַנטיאינטעלעקטואַליזם
    
    # ts != צ
    (r'\beltst', 'עלטסט'),
    (r'\bkeltst', 'קעלטסט'),
    (r'\bbalibtst', 'באַליבטסט'),
    (r'\bgeburts', 'געבורטס'),
    (r'\barbets', 'אַרבעטס'),
    (r'\bgots', 'גאָטס'),
    (r'\bhaltst', 'האַלטסט'),
    
    # kh != כ
    (r'\bpikhol', 'פּיקהאָל'), # פּיקהאָלץ, פּיקהאָלצן
    (r'\btsurikhalt', 'צוריקהאַלט'), # צוריקהאַלטן etc.
    
    # sh != ש
    (r'\boysh(?!ers?\b|vits(er)?\b)', 'אױסה'), # the only exceptions to oysh = אױסה
                                               # עושר, עושרס, אױשװיץ, אױשװיצער
    (r'\baroysh', 'אַרױסה'),
]

# note: output uses precombined Unicode characters
def detransliterate(string):
    for pair in reverse_translit_exceptions:
        string = re.sub(pair[0], pair[1], string)
    for pair in reverse_translit_table:
        string = re.sub(pair[0], pair[1], string)

    return string

# for automatic segmentation using German; code by Samuel Lo
def romanise_german(text):
    rom = {"א": "",    "אַ": "a", "אָ": "o",
           "ב": "b",   "בּ": "b", "בֿ": "w",
           "ג": "g",
           "ד": "d",
           "ה": "h",
           "ו": "u",   "וּ": "u",
           "װ": "w",
           "ױ": "eu",
           "ז": "s",
           "ח": "ch",
           "ט": "t",
           "י": "i",   "יִ": "i",
           "ײ": "ei",  "ײַ": "ei",
           "כּ": "k",   "כ": "ch", "ך": "ch",
           "ל": "l",
           "מ": "m",   "ם": "m",
           "נ": "n",   "ן": "n",
           "ס": "ss",
           "ע": "e",
           "פּ": "p",   "פֿ": "f",  "פ": "f", "ף": "f",
           "צ": "z",   "ץ": "z",
           "ק": "k",
           "ר": "r",
           "ש": "sch", "שׂ": "ss",
           "תּ": "t",   "ת": "ss"
        }

    output = ""
    for c in text:
        if c in rom.keys():
            output += rom[c]
        else:
            output += c

    output = re.sub(r"־", r"-", output)
    output = re.sub(r"schp", r"sp", output)
    output = re.sub(r"scht([aeiour])", r"st\1", output)
    output = re.sub(r"\bpun\b", r"fun", output)
    output = re.sub(r"eup", r"euf", output)
    output = re.sub(r"\bi([aeiou])", r"j\1", output) # Isaac's addition
    output = re.sub(r"([^aeiou])([nl])\b", r"\1e\2", output) # Isaac's addition

    return output

##################################################
# for TTS: respell orthographic words phonetically
##################################################

def respell_loshn_koydesh(text):
    url = 'https://raw.githubusercontent.com/ibleaman/loshn-koydesh-pronunciation/master/orthographic-to-phonetic.txt'
    respellings_list = urlopen(url).read().decode('utf-8')
    respellings_list = respellings_list.split('\n')
    respellings_list = [line for line in respellings_list if line]
    
    lk = {}
    for line in respellings_list:
        key = replace_with_precombined(line.split('\t')[0])
        key = replace_punctuation(key)
        entries = replace_with_precombined(line.split('\t')[1])
        entries = replace_punctuation(entries)
        if key not in lk:
            lk[key] = entries.split(',')
            
    # loop over keys, in reverse order from longest keys to shortest
    for key in sorted(list(lk.keys()), key=len, reverse=True):
        # skip Germanic homographs, which are usually phonetic
        if key not in ["אין", "צום", "בין", "ברי", "מיד", "קין", "שער", "מעגן", "צו", "מאַנס", "טוען", "מערער"]:
            # skip less common LK variants, in favor of more common ones
            if lk[key][0] in ["אַדױשעם", "כאַנוקע", "גדױלע", "כאַװײרע", "מיכיע", "כאָװער", "אָרעװ", "מאָסער", "כיִעס", "זקאָנים", "נעװאָלע", "מאַשלעם", "כפֿאָצים", "כאַכאָמע", "טאַנאָיִם"] and len(lk[key]) > 1:
                replacement = lk[key][1]
            else:
                replacement = lk[key][0]
                
            # replace whole words (separated by spaces & punctuation, but not
            # followed by an apostrophe);
            # also, append a Δ to the respelling so it's not accidentally overwritten
            # (e.g., to avoid סעודה to סודע to סױדע)
            text = re.sub(r'(?<![אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּתΔ])' + key + r'(?![\'אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּת])', 'Δ' + replacement, text)
    
    # missed items
    fixes = {
        "ר'": "רעב",
    }
    for key in fixes:
        text = re.sub(r'(?<![אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּתΔ])' + key + r'(?![\'אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּת])', fixes[key], text)
        
    # remove the added Δ
    text = re.sub('Δ', '', text)
    
    # undo whole-word mistakes
    mistakes = {
        'יוד"שין': "יאַש",
        "יוד״שין": "יאַש",
    }
    for key in mistakes:
        text = re.sub(r'(?<![אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּת])' + key + r'(?![\'אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּת])', mistakes[key], text)
    
    return text
    
#######################################
# convert YIVO orthography into Hasidic

# note: all replacements are based on
# looking for precombined characters
#######################################
hasidifier_lexicon = pd.ExcelFile('https://docs.google.com/spreadsheets/d/1x_KLOaUfnCBVVWEb523QIJZIvk65Pp0ly9MPMVLUVOI/export?format=xlsx')

whole_word_variants = pd.read_excel(hasidifier_lexicon, 'whole_word_variants')
whole_word_variants = dict(zip([replace_with_precombined(word) for word in whole_word_variants['Find']], [replace_with_precombined(word) for word in whole_word_variants['Replace']]))

prefix_variants = pd.read_excel(hasidifier_lexicon, 'prefix_variants')
prefix_variants = dict(zip([replace_with_precombined(word) for word in prefix_variants['Find']], [replace_with_precombined(word) for word in prefix_variants['Replace']]))

suffix_variants = pd.read_excel(hasidifier_lexicon, 'suffix_variants')
suffix_variants = dict(zip([replace_with_precombined(word) for word in suffix_variants['Find']], [replace_with_precombined(word) for word in suffix_variants['Replace']]))

anywhere_variants = pd.read_excel(hasidifier_lexicon, 'anywhere_variants')
anywhere_variants = dict(zip([replace_with_precombined(word) for word in anywhere_variants['Find']], [replace_with_precombined(word) for word in anywhere_variants['Replace']]))

lkizmen = pd.read_excel(hasidifier_lexicon, 'lkizmen')
lkizmen = lkizmen['Words'].tolist()
lkizmen = [replace_with_precombined(word) for word in lkizmen]

word_group_variants = pd.read_excel(hasidifier_lexicon, 'word_group_variants')
word_group_variants = dict(zip([replace_with_precombined(word) for word in word_group_variants['Find']], [replace_with_precombined(word) for word in word_group_variants['Replace']]))

ik_exceptions = pd.read_excel(hasidifier_lexicon, 'ik_exceptions')
ik_exceptions = ik_exceptions['Words'].tolist()
ik_exceptions = [replace_with_precombined(word) for word in ik_exceptions]

lekh_exceptions = pd.read_excel(hasidifier_lexicon, 'lekh_exceptions')
lekh_exceptions = lekh_exceptions['Words'].tolist()
lekh_exceptions = [replace_with_precombined(word) for word in lekh_exceptions]

last_minute_fixes = pd.read_excel(hasidifier_lexicon, 'last_minute_fixes')
last_minute_fixes = dict(zip([replace_with_precombined(word) for word in last_minute_fixes['Find']], [replace_with_precombined(word) for word in last_minute_fixes['Replace']]))

reformatting = [
    ('וּװוּ', 'ואוואו'),
    ('ײיִ', 'ייאי'),
    ('ײַיִ', 'ייאי'), # frier, hebreish - no alef in HY forums AFAIK
    ('וּװ', 'ואוו'),
    ('װוּ', 'וואו'),
    ('װױ', 'וואוי'),
    ('יִו', 'יאו'),
    ('ויִ', 'ואי'),
    ('וּיִ', 'ואי'),
    ('יִוּ', 'יאו'),
    ('יִיִ', 'יאי'),
    ('וּוּ', 'ואו'),
    ('ױ(ו|וּ)', 'ויאו'),
    ('װ', 'וו'),
    ('ױ', 'וי'),
    ('ײ', 'יי'),
    ('ײַ', 'יי'),
    ('־', '-'),
    ('[“״″‟„]', '"'),
    ('׳', "'"),
]
    
def hasidify(text):
    
    text = replace_with_precombined(text)
    text = re.split(r"([^אאַאָבבֿגדהווּװױזחטייִײײַכּכךלמםנןסעפּפֿףצץקרששׂתּתA-Za-z'])", text)
    
    # add 'Γ' as a word/token boundary symbol
    # rationale: the alternative is to iterate over tokens, which takes forever
    text = 'Γ'.join(text)
    text = 'Γ' + text + 'Γ'

    # perform respellings
    for key, value in whole_word_variants.items():
        text = re.sub(f'(?<=Γ){key}(?=Γ)', value, text)
            
    for lkizm in lkizmen:
        text = re.sub(f"(?<![בהל'Γ]){lkizm}", f"'{lkizm}", text)
        text = re.sub(f"{lkizm}(?!ים|ימ|ות|'|Γ)", f"{lkizm}'", text)
            
    for key, value in prefix_variants.items():
        text = re.sub(f'(?<=Γ){key}', value, text)
            
    for key, value in suffix_variants.items():
        text = re.sub(f'{key}(?=Γ)', value, text)
            
    for key, value in anywhere_variants.items():
        text = re.sub(key, value, text)
    
    # add 'Δ' to show that exceptions shouldn't be processed by -ig/-likh rule
    for exception in ik_exceptions:
        text = re.sub(f'{exception}(?!Δ)', f'{exception}Δ', text)
    for exception in lekh_exceptions:
        text = re.sub(f'{exception}(?!Δ)', f'{exception}Δ', text)
    
    # perform -ig and -likh respellings, ignoring the 'Δ'-ed exceptions
    text = re.sub('(?<!Γ)יק(?!Δ)(?=Γ|ער|ע|ן|סט|ס|ט|ערע|ערן|ערס|סטע|סטער|סטן|סטנס|ונג|ונגען)(?!Δ)', 'יג', text)
    text = re.sub('(?<!Γ)לעך(?!Δ)', 'ליך', text)
    text = re.sub('(?<!Γ)לעכ(?!Δ)(?=Γ|ע|ער|ן|ס|ט|סט|ערע|ערן|ערס|סטע|סטער|סטן|סטנס|קײט|קײטן)(?!Δ)', 'ליכ', text)
    
    # remove Greek letters
    text = text.replace('Δ', '')
    text = text.replace('Γ', '')
    
    # perform other replacements involving multiple words
    for key, value in word_group_variants.items():
        text = re.sub(key, value, text)
    
    # final respellings and fixing mistakes
    for pair in reformatting:
        text = re.sub(pair[0], pair[1], text)
    
    for key, value in last_minute_fixes.items():
        text = re.sub(key, value, text)
    
    text = strip_diacritics(text)
    
    return text
    
