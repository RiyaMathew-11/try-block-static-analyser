import argparse
from static_analyser import PatternIdentifier, StaticAnalyser


parser = argparse.ArgumentParser()
parser.add_argument("filename", help="The Python file to analyze")
parser.add_argument("-s", "--save", help="Output file for the report")
args = parser.parse_args()

analyser = StaticAnalyser(args.filename)
pattern_identifier = PatternIdentifier()

analyser.analyse(pattern_identifier)


if args.save:
    analyser.save_report(args.save)
else: 
    analyser.print_report()