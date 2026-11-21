"""Tests for the yiddish package.

Run from the repository root with:  pytest
(The word lists must be present in yiddish/submodules/: run `bash fetch_data.sh` first.)
"""
import re
from pathlib import Path

import pytest

import yiddish

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parent / 'data'

P = yiddish.replace_with_precomposed
D = yiddish.replace_with_decomposed

SENTENCE = 'אונדזער גאַנצע משפּחה װױנט אין די פֿאַראײניקטע שטאַטן.'


# ---------------------------------------------------------------------------
# Unicode and punctuation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('function,kwargs,text,expected', [
    (yiddish.replace_with_precomposed, {}, '\u05d0\u05b7', '\ufb2e'),                 # pasekh alef
    (yiddish.replace_with_precomposed, {}, 'וו וי יי', 'װ ױ ײ'),                      # digraphs -> ligatures
    (yiddish.replace_with_precomposed, {}, '\u05d9\u05d9\u05b7', '\ufb1f'),           # yud + yud + pasekh -> ײַ
    (yiddish.replace_with_precomposed, {}, '\u05f2\u05b7', '\ufb1f'),                 # ײ + pasekh -> ײַ
    (yiddish.replace_with_precomposed, {}, '\u05d1\u05bc', '\u05d1'),                 # dogesh on beys isn't used in YIVO

    (yiddish.replace_with_decomposed, {}, '\ufb2e', '\u05d0\u05b7'),
    (yiddish.replace_with_decomposed, {}, 'װ ױ ײ', 'וו וי יי'),
    (yiddish.replace_with_decomposed, {'vov_yud': True}, 'װ ױ ײ', 'װ ױ ײ'),           # ligatures kept
    # pasekh tsvey yudn: the standard Unicode decomposition is ײ + pasekh, and two yuds + pasekh
    # are treated as the same thing (the one case where digraph input gives a ligature in the output)
    (yiddish.replace_with_decomposed, {}, '\ufb1f', '\u05f2\u05b7'),
    (yiddish.replace_with_decomposed, {}, '\u05d9\u05d9\u05b7', '\u05f2\u05b7'),
    (yiddish.replace_with_decomposed, {'vov_yud': True}, '\u05d9\u05d9\u05b7', '\u05f2\u05b7'),
])
def test_unicode_conversions(function, kwargs, text, expected):
    assert function(text, **kwargs) == expected


def test_precomposed_and_decomposed_are_consistent():
    # converting is idempotent, and either form of the input gives the same result
    assert P(P(SENTENCE)) == P(SENTENCE)
    assert D(D(SENTENCE)) == D(SENTENCE)
    assert P(D(SENTENCE)) == P(SENTENCE)
    assert D(P(SENTENCE)) == D(SENTENCE)


def test_old_and_alternate_names_are_aliases():
    assert yiddish.replace_with_precombined is yiddish.replace_with_precomposed
    assert yiddish.romanise_german is yiddish.romanize_german


def test_replace_punctuation():
    # ASCII hyphen -> makef; geresh/prime -> '; gershayim/double prime -> "
    assert yiddish.replace_punctuation('בעל-עגלה ר׳ ר\u2032 ז״ל ז\u2033ל ר\' ז"ל') == 'בעל־עגלה ר\' ר\' ז"ל ז"ל ר\' ז"ל'


@pytest.mark.parametrize('text,expected', [
    (P('די פֿאַראײניקטע שטאַטן'), 'די פאראייניקטע שטאטן'),
    (P('בײַ װױנט אײ'), 'ביי וווינט איי'),             # ligatures become plain letters (ײַ too)
    ('\u05d1\u05b0\u05e8\u05b8\u0591', '\u05d1\u05b0\u05e8\u0591'),  # only the Yiddish pointing goes: shva and cantillation stay
    ('בעל־עגלה ר\' ז"ל café', 'בעל־עגלה ר\' ז"ל café'),  # makef, punctuation, and non-Hebrew accents stay
])
def test_strip_diacritics(text, expected):
    assert yiddish.strip_diacritics(text) == expected


# ---------------------------------------------------------------------------
# Romanization
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('text,kwargs,expected', [
    ('איבער', {}, 'iber'),
    ('ב\u05d9\u05d9\u05b7', {}, 'bay'),     # yud + yud + pasekh typed in place of ײַ
    (SENTENCE, {}, 'undzer gantse mshpkhh voynt in di fareynikte shtatn.'),
    (P('פֿאַראײניקטע'), {'loc': True}, 'fareyniḳṭe'),
    ('די משפּחה מאַשבער', {'loshn_koydesh': True}, 'di mishpokhe mashber'),
])
def test_transliterate(text, kwargs, expected):
    assert yiddish.transliterate(text, **kwargs) == expected
    assert yiddish.transliterate(D(text), **kwargs) == expected  # decomposed input works too


@pytest.mark.parametrize('text,kwargs,expected', [
    ('shloymele hot khasene gehat', {}, 'שלױמעלע האָט כאַסענע געהאַט'),
    ('Shloymele hOt khasene gehat', {}, 'שלױמעלע האָט כאַסענע געהאַט'),  # case is ignored
    ('shloymele hot khasene gehat', {'loshn_koydesh': True}, 'שלמהלע האָט חתונה געהאַט'),
])
def test_detransliterate(text, kwargs, expected):
    assert yiddish.detransliterate(text, **kwargs) == P(expected)


def test_romanize_german():
    text = 'װען װעלן מיר זיך שפּילן צוזאַמען?'
    assert yiddish.romanize_german(P(text)) == 'wen welen mir sich spilen zusamen?'
    assert yiddish.romanize_german(D(text)) == 'wen welen mir sich spilen zusamen?'  # decomposed input works too


# ---------------------------------------------------------------------------
# Loshn-koydesh
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('text,expected', [
    ('משפּחה', 'מישפּאָכע'),
    ('די משפּחה משפּחות.', 'די מישפּאָכע מישפּאָכעס.'),
    ('גאַנצע שטאַטן', 'גאַנצע שטאַטן'),     # no loshn-koydesh: unchanged
    ("ס'איז", "ס'איז"),                 # a word/letter followed by an apostrophe isn't matched
    ('בור־סוד', 'באָר־סוד'),             # hyphenated entry: respelled once, not twice
    ('סוד־גאַנץ', 'סאָד־גאַנץ'),           # makef separates words: the entry before it is still matched
    ('גאַנץ־סוד', 'גאַנץ־סאָד'),
    ('י"ש', 'יאַש'),                     # a roshe-teyves
    ('י״ש', 'יאַש'),
])
def test_respell_loshn_koydesh(text, expected):
    assert yiddish.respell_loshn_koydesh(text) == P(expected)
    assert yiddish.respell_loshn_koydesh(D(text)) == P(expected)  # decomposed input works too


def test_respell_treats_geresh_and_gershayim_like_apostrophe_and_quote():
    # each pair/triple is the same entry, typed with different punctuation
    quote_forms = ['מוהר"ר', 'מוהר״ר', 'מוהר\u2033ר']
    apostrophe_forms = ["ר' יוסף", 'ר׳ יוסף', 'ר\u2032 יוסף']
    for forms in (quote_forms, apostrophe_forms):
        results = {yiddish.respell_loshn_koydesh(form) for form in forms}
        assert len(results) == 1
        assert results != set(forms)          # and the entry really is respelled


def test_respell_does_not_treat_makef_and_ascii_hyphen_alike():
    assert yiddish.respell_loshn_koydesh('בור־סוד') != yiddish.respell_loshn_koydesh('בור-סוד')


def test_respell_output_is_precomposed_and_repeatable():
    first = yiddish.respell_loshn_koydesh(D(SENTENCE))
    assert first == P(first)
    assert yiddish.respell_loshn_koydesh(SENTENCE) == first


@pytest.mark.parametrize('text,expected', [
    ('מישפּאָכע', 'משפּחה'),
    ('ראָכל האָט כאַסענע', 'רחל האָט חתונה'),
])
def test_spell_loshn_koydesh(text, expected):
    assert yiddish.spell_loshn_koydesh(text) == P(expected)


def test_spell_reverses_respell():
    assert yiddish.spell_loshn_koydesh(yiddish.respell_loshn_koydesh('משפּחה')) == P('משפּחה')


# ---------------------------------------------------------------------------
# Orthographic variants
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('text,expected', [
    ('אונדזער הײליקע ייִדישע שפּראַך', 'אונזער הייליגע אידישע שפראך'),
    (SENTENCE, 'אונזער גאנצע משפחה וואוינט אין די פאראייניגטע שטאטן.'),
])
def test_hasidify(text, expected):
    assert yiddish.hasidify(text) == expected


def test_desovietify():
    assert yiddish.desovietify('דאָס לאָשנ פונ דעמ באלעגאָלע') == P('דאָס לשון פֿון דעם בעל־עגלה')


# ---------------------------------------------------------------------------
# The README's examples (so the documentation can't drift from the code)
# ---------------------------------------------------------------------------

def _readme():
    return (ROOT / 'README.md').read_text(encoding='utf-8')


def _readme_function_examples():
    examples = []
    for block in re.findall(r'```python\n(>>>.*?)```', _readme(), re.S):
        lines = [line for line in block.split('\n') if line.strip()]
        for call, expected in zip(lines[0::2], lines[1::2]):
            assert call.startswith('>>> ')
            examples.append((call[4:], expected))
    return examples


@pytest.mark.parametrize('call,expected', _readme_function_examples())
def test_readme_function_example(call, expected):
    assert eval(call, {'yiddish': yiddish}) == eval(expected)


def test_readme_function_examples_were_found():
    assert len(_readme_function_examples()) >= 15


def test_readme_example_block(capsys):
    code, expected = re.findall(r'```python\n(import yiddish.*?)```\n\nOutput:\n\n```\n(.*?)```', _readme(), re.S)[0]
    exec(code, {})
    assert capsys.readouterr().out.strip() == expected.strip()


# ---------------------------------------------------------------------------
# Snapshot: every word in the loshn-koydesh list, respelled
# ---------------------------------------------------------------------------

def test_loshn_koydesh_snapshot():
    source = (DATA / 'lk_test.txt').read_text(encoding='utf-8')
    expected = (DATA / 'lk_test_expected.txt').read_text(encoding='utf-8')
    actual = yiddish.respell_loshn_koydesh(source)

    if actual != expected:
        # (the output is precomposed, so split everything on the precomposed separator)
        separator = P(' האָט ')
        src_words = P(source).split(separator)
        got_words = actual.split(separator)
        want_words = expected.split(separator)
        if len(got_words) == len(want_words):
            diffs = [f'{s!r}: got {g!r}, expected {w!r}'
                     for s, g, w in zip(src_words, got_words, want_words) if g != w]
            pytest.fail(f'{len(diffs)} word(s) changed:\n' + '\n'.join(diffs[:20]))
        pytest.fail('respelled text differs from the saved snapshot (and the word count changed)')
