import argparse
import re
import yiddish_unicode
import respell_lk

parser = argparse.ArgumentParser(description="respeller for Yiddish")
parser.add_argument("-i", "--input", required=True, help="text file")
parser.add_argument("-o", "--output", required=True, help="where to save reformatted text file")
parser.add_argument("-l", "--lk", action='store_true')
args = parser.parse_args()

with open(args.input, "r") as content_file:
    input_string = content_file.read()

output_string = yiddish_unicode.replace_with_precombined(input_string)
output_string = yiddish_unicode.replace_punctuation(output_string)

if args.lk:
    output_string = respell_lk.respell_loshn_koydesh(output_string)

with open(args.output, "w") as text_file:
    text_file.write(output_string)
