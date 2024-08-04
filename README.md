# yiddish

A Python library for processing Yiddish text

Isaac L. Bleaman (<bleaman@berkeley.edu>) and contributors (see commit history)

## What is this for?

This library includes functions to carry out common tasks when dealing with Yiddish text. For example, you might wish to replace precombined Unicode characters (such as אַ, U+FB2E) with their decomposed versions (אַ, which is U+05D0 followed by U+05B7). Or you might wish to transliterate YIVO Yiddish text
(`איבער` to `iber`) or render it in the orthography used more commonly in the 
Hasidic community (`שנײיִק` to `שנייאיג`).

See the source file, `yiddish.py`, for the full list of supported functions.

## How to install

    pip install yiddish
    
## How to cite

If you'd like to cite `yiddish` in a publication, you can include a link to the source:
    https://github.com/ibleaman/yiddish
    
## Example

```python
import yiddish

output = ''

string = 'אונדזער גאַנצע משפּחה װױנט אין די פֿאַראײניקטע שטאַטן.'

output += yiddish.replace_with_precombined(string) + '\n'
output += yiddish.respell_loshn_koydesh(string) + '\n'
output += yiddish.strip_diacritics(string) +  '\n'
output += yiddish.transliterate(string) +  '\n'
output += yiddish.transliterate(string, loshn_koydesh=True) +  '\n'
output += yiddish.hasidify(string)

output += '\n\n'

string_two = 'shloymele hot khasene gehat mit rokhls tokhter leye.'

output += yiddish.detransliterate(string_two) + '\n'
output += yiddish.detransliterate(string_two, loshn_koydesh=True)

print(output)

```

Output:

```
אונדזער גאַנצע משפּחה װױנט אין די פֿאַראײניקטע שטאַטן.
אונדזער גאַנצע מישפּאָכע װױנט אין די פֿאַראײניקטע שטאַטן.
אונדזער גאנצע משפחה וווינט אין די פאראייניקטע שטאטן.
undzer gantse mshpkhh voynt in di fareynikte shtatn.
undzer gantse mishpokhe voynt in di fareynikte shtatn.
אונזער גאנצע משפחה וואוינט אין די פאראייניגטע שטאטן.

שלױמעלע האָט כאַסענע געהאַט מיט ראָכלס טאָכטער לײע.
שלמהלע האָט חתונה געהאַט מיט רחלס טאָכטער לאה.
```