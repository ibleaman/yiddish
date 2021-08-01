# note: output of detransliterate uses precombined Unicode characters

import re
import yiddish_unicode

translit_table = [ # all are precombined
    ('א', ''),
    ('אַ', 'a'),
    ('אָ', 'o'),
    ('ב', 'b'),
    ('בֿ', 'v'),
    ('ג', 'g'),
    ('ד', 'd'),
    ('ה', 'h'),
    ('ו', 'u'),
    ('וּ', 'u'),
    ('װ', 'v'),
    ('ױ', 'oy'),
    ('זש', 'zh'),
    ('ז', 'z'),
    ('ח', 'kh'),
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
    romanized = yiddish_unicode.replace_with_precombined(string)

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
    ('ay', 'ײַ'),
    ('ey', 'ײ'),
    ('oy', 'ױ'),
    ('zh', 'זש'),
    ('kh', 'כ'),
    ('sh', 'ש'),
    ('ts', 'צ'),
    ('ii', 'יִיִ'),
    ('iyi', 'יִייִ'),
    ('yi', 'ייִ'),
    ('iy', 'יִי'),
    ('uvu', 'וּװוּ'),
    ('uv', 'וּװ'),
    ('vu', 'װוּ'),
    ('uu', 'וּוּ'),
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

def detransliterate(string):
    for pair in reverse_translit_table:
        string = re.sub(pair[0], pair[1], string)

    return string
