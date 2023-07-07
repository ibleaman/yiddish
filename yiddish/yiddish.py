# yiddish
# A Python library for processing Yiddish text
# Author: Isaac L. Bleaman (bleaman@berkeley.edu)

import re
from urllib.request import urlopen
import csv

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

# When vov_yud==True, these will be preserved as precombined chars:
#      װ, ײ, ױ
def replace_with_decomposed(string, vov_yud=False):
    for pair in pairs:
        if vov_yud and pair[1] in ['װ', 'ױ', 'ײ']:
            pass
        else:
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


#########################################
# import loshn-koydesh pronunciation list
#########################################

respellings_url = 'https://raw.githubusercontent.com/ibleaman/loshn-koydesh-pronunciation/master/orthographic-to-phonetic.txt'
respellings_list = urlopen(respellings_url).read().decode('utf-8')
respellings_list = respellings_list.split('\n')
respellings_list = [line for line in respellings_list if line]

lk = {} # orthographic to phonetic
reverse_lk = {} # phonetic to orthographic

for line in respellings_list:
    key = replace_with_precombined(line.split('\t')[0])
    key = replace_punctuation(key)
    entries = replace_with_precombined(line.split('\t')[1])
    entries = replace_punctuation(entries)
    if key not in lk:
        lk[key] = entries.split(',')
    for entry in entries.split(','):
        if entry not in reverse_lk:
            reverse_lk[entry] = key

germanic_semitic_homographs = ["אין", "צום", "בין", "ברי", "מיד", "קין", "שער", "מעגן", "צו", "מאַנס", "טוען", "מערער"]

less_common_lk_pronunciations = ["אַדױשעם", "כאַנוקע", "גדױלע", "כאַװײרע", "מיכיע", "כאָװער", "אָרעװ", "מאָסער", "כיִעס", "זקאָנים", "נעװאָלע", "מאַשלעם", "כפֿאָצים", "כאַכאָמע", "טאַנאָיִם", "יאָסעף", "יאָסעפֿס", "יאָסעפֿן"]
            
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
    ('פ', 'f'),
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

# if loshn_koydesh, look up string in LK dictionary
def transliterate(string, loshn_koydesh=False):
    romanized = replace_with_precombined(string)
    
    if loshn_koydesh:
        tokens = re.findall(r"[אאַאָבבֿגדהוװוּױזחטייִײײַככּךלמםנןסעפּפֿףצץקרששׂתּת\-־']+|[^אאַאָבבֿגדהוװוּױזחטייִײײַככּךלמםנןסעפּפֿףצץקרששׂתּת\-־']", romanized)
        new_tokens = []
        for token in tokens:
            if token in lk and token not in germanic_semitic_homographs:
                if lk[token][0] in less_common_lk_pronunciations and len(lk[token]) > 1:
                    new_tokens.append(lk[token][1].replace('־', '-'))
                else:
                    new_tokens.append(lk[token][0].replace('־', '-'))
            else:
                new_tokens.append(token)
            
        romanized = ''.join(new_tokens)

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
    (r'\bך', 'כ'), # no word-initial final letters
    (r'\bם', 'מ'),
    (r'\bן', 'נ'),
    (r'\bף', 'פֿ'),
    (r'\bץ', 'צ'),
]

reverse_translit_exceptions = [

    # unpredicted shtumer alef
    (r'\bfarey', 'פֿאַראײ'), # פֿאַראײניקט, פֿאַראײביקן
    (r'\bantiintel', 'אַנטיאינטעל'), # אַנטיאינטעלעקטואַליזם
    (r'\bbizitst', 'ביזאיצט'), # ביזאיצטיקער
    (r'\boybnoy', 'אױבנאױ'), # אױבנאױף
    (r'\boysib', 'אױסאיב'), # אױסאיבן
    (r'geibt', 'געאיבט'),
    (r'geiblt', 'געאיבלט'),
    (r'tsuibn\b', 'צואיבן'),
    (r'\boyseydl', 'אױסאײדל'), # אױסאײדלען
    (r'geeydl', 'געאײדל'),
    (r'tsueydl', 'צואײדל'),
    (r'\bayneyg', 'אײַנאײג'), # אײַנאײגענען
    (r'geey', 'געאײ'),
    (r'tsuey', 'צואײ'),
    (r'geindlt', 'געאינדלט'), # surfing
    (r'\bumoys', 'אומאױס'), # אומאױסשעפּלעך
    (r'\bumayn', 'אומאײַנ'), # אומאײַנגענעם
    (r'\bumeydl', 'אומאײדל'), # אומאײדל
    (r'\bumeydel', 'אומאײדעל'), # אומאײדעלע
    (r'\bureynikl', 'אוראײניקל'),
    (r'\bbaayn', 'באַאײַנ'), # באַאײַנדרוקן, באַאײַנפֿלוסן
    (r'geayn', 'געאײַנ'), # געאײַנפֿלוסט
    (r'tsuayn', 'צואײַנ'),
    (r'durkhayl', 'דורכאײַל'), # דורכאײַלן
    (r'farbayayl', 'פֿאַרבײַאײַל'), # דורכאײַלן
    (r'geay', 'געאײַ'),
    (r'tsuayl', 'צואײַל'), # געאײַנפֿלוסט
    (r'geirtst', 'געאירצט'),
    (r'tsuirtsn\b', 'צואירצן'),
    (r'grobayz', 'גראָבאײַז'), # גראָבאײַזנס
    (r'presayz', 'פּרעסאײַז'),
    (r'halbindzl', 'האַלבאינדזל'),
    (r'hinteroyg', 'הינטעראױג'), # הינטעראױגיק
    (r'zunoyfgang', 'זונאױפֿגאַנג'),
    (r'moyleyzl', 'מױלאײזל'),
    (r'\bfarum', 'פֿאַראומ'), # פֿאַראומװערדיקן, פֿאַראומעטיקטע, פֿאַראומרײניקן
    (r'\bfarur', 'פֿאַראור'), # פֿאַראַורטײל
    (r'\bforur', 'פֿאָראור'), # פֿאָראורטל
    (r'\bfaribl', 'פֿאַראיבל'),
    (r'\bfarinteres', 'פֿאַראינטערעס'), # פֿאַראינטערעסירן
    
    # ay != ײַ
    (r'\brayon\b', 'ראַיאָן'),
    (r'\brayonen\b', 'ראַיאָנען'),
    (r'bayornt', 'באַיאָרנט'),
    (r'bayort', 'באַיאָרט'),
    (r'mayontik', 'מאַיאָנטיק'),
    (r'mayontkes', 'מאַיאָנטקעס'),
    (r'mayonez', 'מאַיאָנעז'),
    (r'mayestet', 'מאַיעסטעט'),
    (r'payats\b', 'פּאַיאַץ'),
    (r'payatsn\b', 'פּאַיאַצן'),
    (r'payatseve', 'פּאַיאַצעװע'),
    (r'farayorik', 'פֿאַראַיאָריק'),
    (r'\bkayor', 'קאַיאָר'),
    (r'\bayed', 'אַיעד'), # אַיעדער
    (r'\bayo\b', 'אַיאָ'),
    
    # ey != ײ
    (r'geyogt', 'געיאָגט'),
    (r'geyeg', 'געיעג'),
    (r'\bgeyog\b', 'געיאָג'),
    (r'geyavet', 'געיאַװעט'),
    (r'geyadet', 'געיאַדעט'),
    (r'geyopet', 'געיאָפּעט'),
    (r'geyabede', 'געיאַבעדע'), # געיאַבעדע(װע)ט
    (r'geyakhmert', 'געיאַכמערט'),    
    (r'tseyakhmert', 'צעיאַכמערט'),    
    (r'tseyakhmet', 'צעיאַכמעט'),    
    (r'geyodlt', 'געיאָדלט'),
    (r'geyomer', 'געיאָמער'),
    (r'tseyomer', 'צעיאָמער'),
    (r'geyutshet', 'געיוטשעט'),
    (r'geyoyr', 'געיױר'), # געיױרענע
    (r'\bgeyet(\b|er|e|n|s|ns)', r'געיעט\1'),
    (r'geyentst', 'געיענצט'),
    (r'geyenket', 'געיענקעט'),
    (r'geyekt', 'געיעקט'),
    (r'\bgeyert\b', 'געיערט'),
    (r'pleyade', 'פּלעיאַדע'),
    
    # oy != ױ
    (r'proyekt', 'פּראָיעקט'), # פּראָיעקטאָר
    (r'umloyal', 'אומלאָיאַל'),
    (r'loyal', 'לאָיאַל'),
    (r'paranoye', 'פּאַראַנאָיע'),
    
    # ts != צ
    (r'tstu\b', 'טסטו'),
    (r'\beltst', 'עלטסט'),
    (r'\bkeltst', 'קעלטסט'),
    (r'\bbalibtst', 'באַליבטסט'),
    (r'\bgeburts', 'געבורטס'),
    (r'\barbets', 'אַרבעטס'),
    (r'\barbayts', 'אַרבײַטס'),
    (r'\bdemolts', 'דעמאָלטס'),
    (r'\bgots', 'גאָטס'),
    (r'\bguts', 'גוטס'),
    (r'\bgeshefts', 'געשעפֿטס'),
    (r'(\b|ba|far|der)haltst', r'\1האַלטסט'),
    (r'\bshlekhts\b', 'שלעכטס'),
    (r'(\b|tse)shpaltst', r'\1שפּאַלטסט'),
    (r'(\b|tse|far)shpreytst', r'\1שפּרײטסט'),
    (r'shpetst', 'שפּעטסט'),
    (r'\brekhts\b', 'רעכטס'),
    (r'du shatst', 'דו שאַטסט'), # cf. ער שאַצט
    (r'\bforverts\b', 'פֿאָרװערטס'),
    
    # kh != כ
    (r'\bpikhol', 'פּיקהאָל'), # פּיקהאָלץ, פּיקהאָלצן
    (r'\btsurikhalt', 'צוריקהאַלט'), # צוריקהאַלטן etc.
    (r'\bkrikhalt', 'קריקהאַלט'),
    
    # sh != ש
    (r'\boysh(?!ers?\b|vits(er)?\b)', 'אױסה'), # the only exceptions to oysh = אױסה
                                               # עושר, עושרס, אױשװיץ, אױשװיצער
    (r'\baroysh', 'אַרױסה'),
]

semitic_germanic_homophones = [
    'אָדער',
    'אױפֿן',
    'איבער',
    'אײן',
    'אים',
    'בױ',
    'דאַן',
    'װײס',
    'װעסט',
    'זאָל',
    'טאָמער',
    'טו',
    'לײען',
    'מאָגן',
    'מאַן',
    'מוטער',
    'מײַנע',
    'מע',
    'נעמען',
    'עמער',
    'פּױלן',
    'קעלער',
    'קעץ',
    'שװאַך',
    'שיִער',
    'שנײ',
]

# note: output uses precombined Unicode characters
# if loshn_koydesh, look up string in LK dictionary
def detransliterate(string, loshn_koydesh=False):
    string = string.lower()
    for pair in reverse_translit_exceptions:
        string = re.sub(pair[0], pair[1], string)
    for pair in reverse_translit_table:
        string = re.sub(pair[0], pair[1], string)
                
    if loshn_koydesh:
        tokens = re.findall(r"[\w\-־]+|[^\w\-־]", string)
        new_tokens = []
        for token in tokens:
            if token.replace('-', '־') in reverse_lk and token not in semitic_germanic_homophones:
                new_tokens.append(reverse_lk[token.replace('-', '־')].replace('־', '-'))
            else:
                new_tokens.append(token)
            
        string = ''.join(new_tokens)
            
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

# Note: input text WILL become precombined
def respell_loshn_koydesh(text):
    text = replace_with_precombined(text)
    # loop over keys, in reverse order from longest keys to shortest
    for key in sorted(list(lk.keys()), key=len, reverse=True):
        # skip Germanic homographs, which are usually phonetic
        if key not in germanic_semitic_homographs:
            # skip less common LK pronunciations, in favor of more common ones
            if lk[key][0] in less_common_lk_pronunciations and len(lk[key]) > 1:
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

#######################################################
# convert phonetic spellings to loshn-koydesh spellings
#######################################################

# Note: input text WILL become precombined
def spell_loshn_koydesh(text):
    text = replace_with_precombined(text)
    # loop over keys, in reverse order from longest keys to shortest
    for key in sorted(list(reverse_lk.keys()), key=len, reverse=True):
        # skip Germanic homophones
        if key not in semitic_germanic_homophones:
            replacement = reverse_lk[key]
                
            # replace whole words (separated by spaces & punctuation, but not
            # followed by an apostrophe);
            # also, append a Δ to the respelling so it's not accidentally overwritten
            # (e.g., to avoid סעודה to סודע to סױדע)
            text = re.sub(r'(?<![אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּתΔ])' + key + r'(?![\'אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּת])', 'Δ' + replacement, text)
    
    # remove the added Δ
    text = re.sub('Δ', '', text)

    return text

#######################################
# convert YIVO orthography into Hasidic

# note: all replacements are based on
# looking for precombined characters
#######################################
hasidify_lexicon = 'https://raw.githubusercontent.com/ibleaman/hasidify_lexicon/master/'

whole_word_variants = list(csv.reader(urlopen(hasidify_lexicon + 'whole_word_variants.csv').read().decode('utf-8').replace('\r', '').splitlines()))
whole_word_variants = dict(zip([replace_with_precombined(row[0]) for row in whole_word_variants if row[0] != 'Find'], [replace_with_precombined(row[1]) for row in whole_word_variants if row[1] != 'Replace']))

prefix_variants = list(csv.reader(urlopen(hasidify_lexicon + 'prefix_variants.csv').read().decode('utf-8').replace('\r', '').splitlines()))
prefix_variants = dict(zip([replace_with_precombined(row[0]) for row in prefix_variants if row[0] != 'Find'], [replace_with_precombined(row[1]) for row in prefix_variants if row[1] != 'Replace']))

suffix_variants = list(csv.reader(urlopen(hasidify_lexicon + 'suffix_variants.csv').read().decode('utf-8').replace('\r', '').splitlines()))
suffix_variants = dict(zip([replace_with_precombined(row[0]) for row in suffix_variants if row[0] != 'Find'], [replace_with_precombined(row[1]) for row in suffix_variants if row[1] != 'Replace']))

anywhere_variants = list(csv.reader(urlopen(hasidify_lexicon + 'anywhere_variants.csv').read().decode('utf-8').replace('\r', '').splitlines()))
anywhere_variants = dict(zip([replace_with_precombined(row[0]) for row in anywhere_variants if row[0] != 'Find'], [replace_with_precombined(row[1]) for row in anywhere_variants if row[1] != 'Replace']))

lkizmen = list(csv.reader(urlopen(hasidify_lexicon + 'lkizmen.csv').read().decode('utf-8').replace('\r', '').splitlines()))
lkizmen = [replace_with_precombined(row[0]) for row in lkizmen if row[0] != 'Words']

word_group_variants = list(csv.reader(urlopen(hasidify_lexicon + 'word_group_variants.csv').read().decode('utf-8').replace('\r', '').splitlines()))
word_group_variants = dict(zip([replace_with_precombined(row[0]) for row in word_group_variants if row[0] != 'Find'], [replace_with_precombined(row[1]) for row in word_group_variants if row[1] != 'Replace']))

ik_exceptions = list(csv.reader(urlopen(hasidify_lexicon + 'ik_exceptions.csv').read().decode('utf-8').replace('\r', '').splitlines()))
ik_exceptions = [replace_with_precombined(row[0]) for row in ik_exceptions if row[0] != 'Words']

lekh_exceptions = list(csv.reader(urlopen(hasidify_lexicon + 'lekh_exceptions.csv').read().decode('utf-8').replace('\r', '').splitlines()))
lekh_exceptions = [replace_with_precombined(row[0]) for row in lekh_exceptions if row[0] != 'Words']

last_minute_fixes = list(csv.reader(urlopen(hasidify_lexicon + 'last_minute_fixes.csv').read().decode('utf-8').replace('\r', '').splitlines()))
last_minute_fixes = dict(zip([replace_with_precombined(row[0]) for row in last_minute_fixes if row[0] != 'Find'], [replace_with_precombined(row[1]) for row in last_minute_fixes if row[1] != 'Replace']))

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
    # ('־', '-'),
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
    text = re.sub('(?<![ΓΔ])יק(?!Δ)(?=Γ|ערΓ|עΓ|ןΓ|סטΓ|סΓ|טΓ|ערעΓ|ערןΓ|ערסΓ|סטעΓ|סטערΓ|סטןΓ|סטנסΓ|ונגΓ|ונגען)(?!Δ)', 'יג', text)
    text = re.sub('(?<![ΓΔ])לעך(?!Δ)', 'ליך', text)
    text = re.sub('(?<![ΓΔ])לעכ(?!Δ)(?=Γ|עΓ|ערΓ|ןΓ|סΓ|טΓ|סטΓ|ערעΓ|ערןΓ|ערסΓ|סטעΓ|סטערΓ|סטןΓ|סטנסΓ|קײטΓ|קײטן)(?!Δ)', 'ליכ', text)

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
    
def desovietify(text):
    text = replace_with_precombined(text)
    text = re.split(r"([^אאַאָבבֿגדהווּװױזחטייִײײַכּכךלמםנןסעפפּפֿףצץקרששׂתּתA-Za-z'])", text)
    
    # add 'Γ' as a word/token boundary symbol
    text = 'Γ'.join(text)
    text = 'Γ' + text + 'Γ'

    # replace unpointed alef with pasekh alef when not followed by vowels. 
    # (unpointed alef, if not followed by a vov/yud-based vowel, is alway pasekh alef in Soviet orthography)
    text = re.sub('א(?![י|יִ|ײ|ײַ|וּ|ױ|ו])', 'אַ', text)

    # replace unpointed pey with fey
    text = re.sub('פ', 'פֿ', text)

    # replace final kof, mem, nun, tsadek, fey with long forms
    text = re.sub('כ(?=Γ)', 'ך', text)
    text = re.sub('מ(?=Γ)', 'ם', text)
    text = re.sub('נ(?=Γ)', 'ן', text)
    text = re.sub('צ(?=Γ)', 'ץ', text)
    text = re.sub('פֿ(?=Γ)', 'ף', text)

    # replace oyf, bay
    text = re.sub('(?<=Γ)אַף(?=Γ)', 'אױף', text)
    text = re.sub('(?<=Γ)אַפֿן(?=Γ)', 'אױפֿן', text)
    text = re.sub('(?<=Γ)אוף(?=Γ)', 'אױף', text)
    text = re.sub('(?<=Γ)אופֿ', 'אױפֿ', text)
    text = re.sub('(?<=Γ)באַ(?=Γ)', 'בײַ', text)
    text = re.sub('(?<=Γ)באַם(?=Γ)', 'בײַם', text)

    text = spell_loshn_koydesh(text)

    # remove Greek letters
    text = text.replace('Δ', '')
    text = text.replace('Γ', '')

    return text
