import argparse
import sys
from static_analyser import PatternIdentifier, StaticAnalyser

def read_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="The Python file to analyze")
parser.add_argument("-s", "--save", help="Output file for the report")
args = parser.parse_args()

file_content = read_file(args.filename)
analyser = StaticAnalyser(args.filename, file_content)
pattern_identifier = PatternIdentifier()

analyser.analyse(pattern_identifier)

if args.save:
    analyser.save_report(args.save)
else:
    analyser.print_report()