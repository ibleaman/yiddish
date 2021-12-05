import re
from urllib.request import urlopen
import yiddish_unicode

url = 'https://raw.githubusercontent.com/ibleaman/loshn-koydesh-pronunciation/master/orthographic-to-phonetic.txt'
respellings_list = urlopen(url).read().decode('utf-8')
respellings_list = respellings_list.split('\n')
respellings_list = [line for line in respellings_list if line]

def respell_loshn_koydesh(text):
    lk = {}
    for line in respellings_list:
        key = yiddish_unicode.replace_with_precombined(line.split('\t')[0])
        entries = yiddish_unicode.replace_with_precombined(line.split('\t')[1])
        if key not in lk:
            lk[key] = entries.split(',')
            
    # loop over keys, in reverse order from longest keys to shortest
    for key in sorted(list(lk.keys()), key=len, reverse=True):
        # skip Germanic homographs, which are usually phonetic
        if key not in ["אין", "צום", "בין", "ברי", "מיד", "קין", "שער", "מעגן", "צו", "מאַנס", "טוען", "מערער"]:
            # skip less common LK variants, in favor of more common ones
            if lk[key][0] in ["אַדױשעם", "כאַנוקע", "גדױלע", "כאַװײרע", "מיכיע", "כאָװער", "אָרעװ", "מאָסער", "כיִעס", "זקאָנים", "נעװאָלע", "מאַשלעם"] and len(lk[key]) > 1:
                replacement = lk[key][1]
            else:
                replacement = lk[key][0]
                
            # replace whole words (separated by spaces & punctuation, but not
            # followed by an apostrophe);
            # also, append a Δ to the respelling so it's not accidentally overwritten
            # (e.g., to avoid סעודה to סודע to סױדע)
            text = re.sub(r'(?<![אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּתΔ])' + key + r'(?![\'אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּת])', 'Δ' + replacement, text)
    
    # last-minute: undo mistakes or missed items
    fixes = {
        "ר'": "רעב",
    }
    for key in fixes:
        text = re.sub(r'(?<![אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּתΔ])' + key + r'(?![\'אאַאָבבֿגדהװווּזחטייִײײַױכּכךלמםנןסעפּפפֿףצץקרששׂתּת])', fixes[key], text)
        
    # remove the added Δ
    text = re.sub('Δ', '', text)
    
    return text