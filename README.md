# yiddish

A Python library for processing Yiddish text

by Isaac L. Bleaman (<bleaman@berkeley.edu>)

See the commit history for additional contributors.

## What is this for?

This library includes functions to carry out common tasks when dealing with Yiddish text. For example, you might wish to replace precomposed Unicode characters (such as `אַ`, U+FB2E) with their decomposed versions (`אַ`, which is U+05D0 followed by U+05B7). Or you might wish to transliterate YIVO Yiddish text (`איבער` to `iber`) or render it in the orthography used more commonly in the Hasidic community (`שנײיִק` to `שנייאיג`).

See [Functions](#functions) below for the full list.

## How to install

    pip install yiddish

The package requires Python 3.9 or later and has no dependencies.

Note: The wordlists the package relies on are bundled into the releases on PyPI, but they are not stored in this repository. If you wish to install from the source, clone the repository, run `bash fetch_data.sh` to download the wordlists, and then run `pip install .`. (Installing directly with `pip install git+https://github.com/ibleaman/yiddish` will not include them, and the package will fail to import.)

## License and data

The library is released under the MIT License (see `LICENSE.md`).

The wordlists come from two separate repositories, [loshn-koydesh-pronunciation](https://github.com/ibleaman/loshn-koydesh-pronunciation) and [hasidify_lexicon](https://github.com/ibleaman/hasidify_lexicon), and are bundled into each release. The *loshn-koydesh* lexicon was inspired by the work of lexicographer Yitskhok Niborski and expanded and adapted from a wordlist put together by Eliezer Niborski; see its repository for the sources. The *hasidify* list was initially created by me for personal use during my doctoral research, based on my own intuitions about common spelling correspondences.

## How to cite

If you'd like to cite `yiddish` in a publication, please include a link to https://github.com/ibleaman/yiddish or https://pypi.org/project/yiddish/

## Example

```python
import yiddish

output = ''

string = 'אונדזער גאַנצע משפּחה װױנט אין די פֿאַראײניקטע שטאַטן.'

output += yiddish.replace_with_precomposed(string) + '\n'
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

## Functions

All functions take a string and return a string. Input may be in precomposed (e.g., אַ, U+FB2E) or decomposed (אַ, U+05D0 + U+05B7) form, except where noted.

### Unicode and punctuation

**`replace_with_precomposed(string)`**: replace decomposed characters with precomposed ones. (`replace_with_precombined` is an older name for the same function and still works.) Note that characters such as אַ (U+FB2E) belong to Unicode's Alphabetic Presentation Forms block and are excluded from standard NFC normalization, so `unicodedata.normalize('NFC', ...)` will not produce them; this function will.

```python
>>> yiddish.replace_with_precomposed('\u05d0\u05b7')
'אַ'

>>> len(yiddish.replace_with_precomposed('\u05d0\u05b7'))
1
```

**`replace_with_decomposed(string, vov_yud=False)`**: replace precomposed characters with decomposed ones. With `vov_yud=True`, ligatures that are already present in the input (װ, ױ, ײ) are kept, but digraphs (וו, וי, יי) are not converted into ligatures. (To use ligatures throughout, run `replace_with_precomposed` first, then this function with `vov_yud=True`.) There is one exception, which applies whether or not `vov_yud` is set: ײַ (*pasekh tsvey yudn*) and two *yud*s followed by *pasekh* both become ligature ײ + *pasekh* (U+05F2 U+05B7), the standard Unicode decomposition of ײַ.

```python
>>> yiddish.replace_with_decomposed('\ufb2e')
'אַ'

>>> len(yiddish.replace_with_decomposed('\ufb2e'))
2
```

```python
>>> yiddish.replace_with_decomposed('װױנט')
'וווינט'
```

**`replace_punctuation(string)`**: use the punctuation conventional for (at least much of) Yiddish text on the web: ASCII hyphens become *makef*, and *geresh*/*gershayim*/prime variants become `'` and `"`.

```python
>>> yiddish.replace_punctuation('ר׳ יוסף ז״ל')
'ר\' יוסף ז"ל'
```

**`strip_diacritics(string)`**: remove the *nekudes*/pointing used in standard (YIVO) Yiddish orthography (*pasekh*, *komets*, *khirek*, *dogesh*, *rofe*, and *sin* dot) and expand the ligatures װ, ױ, ײ, ײַ into plain letters. Other Hebrew points and cantillation marks are not removed.

```python
>>> yiddish.strip_diacritics('די פֿאַראײניקטע שטאַטן')
'די פאראייניקטע שטאטן'
```

### Romanization

**`transliterate(string, loshn_koydesh=False, loc=False)`**: romanize Yiddish text using the YIVO system. With `loc=True`, a Library of Congress-style system is used instead. With `loshn_koydesh=True`, Hebrew- and Aramaic-origin words are first respelled as they are pronounced (see `respell_loshn_koydesh`).

```python
>>> yiddish.transliterate('איבער')
'iber'
```

```python
>>> yiddish.transliterate('פֿאַראײניקטע', loc=True)
'fareyniḳṭe'
```

```python
>>> yiddish.transliterate('די משפּחה מאַשבער', loshn_koydesh=True)
'di mishpokhe mashber'
```

**`detransliterate(string, loshn_koydesh=False)`**: convert YIVO-style romanization back to Yiddish script. With `loshn_koydesh=True`, Hebrew- and Aramaic-origin words are given their traditional spelling. The output uses precomposed Unicode characters (but you can run `replace_with_decomposed` on the output if desired).

```python
>>> yiddish.detransliterate('shloymele hot khasene gehat')
'שלױמעלע האָט כאַסענע געהאַט'
```

```python
>>> yiddish.detransliterate('shloymele hot khasene gehat', loshn_koydesh=True)
'שלמהלע האָט חתונה געהאַט'
```

**`romanize_german(text)`**: (also available as `romanise_german`) a German-style romanization (originally designed for use with the aeneas audio-text synchronizer).

```python
>>> yiddish.romanize_german('װען װעלן מיר זיך שפּילן צוזאַמען?')
'wen welen mir sich spilen zusamen?'
```

### *Loshn-koydesh*

These use the wordlists from [loshn-koydesh-pronunciation](https://github.com/ibleaman/loshn-koydesh-pronunciation).

**`respell_loshn_koydesh(text)`**: respell Hebrew- and Aramaic-origin words as they are pronounced. The output uses precomposed Unicode.

```python
>>> yiddish.respell_loshn_koydesh('משפּחה')
'מישפּאָכע'
```

**`spell_loshn_koydesh(text)`**: the reverse: give Hebrew- and Aramaic-origin words their traditional spelling.

```python
>>> yiddish.spell_loshn_koydesh('מישפּאָכע')
'משפּחה'
```

### Orthographic variants

**`hasidify(text)`**: render text in the spelling used more commonly in the Hasidic community.

```python
>>> yiddish.hasidify('אונדזער הײליקע ייִדישע שפּראַך')
'אונזער הייליגע אידישע שפראך'
```

**`desovietify(text)`**: convert Soviet Yiddish orthography to standard (YIVO) orthography.

```python
>>> yiddish.desovietify('דאָס לאָשנ פונ דעמ באלעגאָלע')
'דאָס לשון פֿון דעם בעל־עגלה'
```
