import ast
import sys
from typing import List, Dict

class StaticAnalyser:
    def __init__(self, filename: str):
        self.filename: str = filename
        self.tree: ast.AST = None
        self.report: List[Dict[str, str]] = []

    def read_file(self) -> str:
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            sys.exit(1)

    def generate_ast(self) -> None:
        file_content = self.read_file()
        self.tree = ast.parse(file_content, filename=self.filename)

    def analyse(self, pattern_identifier: 'PatternIdentifier') -> None:
        if self.tree is None:
            self.generate_ast()
        
        pattern_identifier.check_patterns(self.tree, self)
        
    def report_issue(self, line: int, explanation: str) -> None:
        self.report.append({
            'line': line,
            'explanation': explanation
        })

    def print_report(self) -> None:
        if not self.report:
            print("No issues found.")
        else:
            print(f"File: {self.filename}\n\n")
            for issue in self.report:
                print(f"Line: {issue['line']}")
                print(f"Issue: {issue['explanation']}")
                print("-" * 40)

    # This can also be replaced with the `> output_file` in terminal
    def save_report(self, output_file: str) -> None:
        with open(output_file, 'w', encoding='utf-8') as file:
            if not self.report:
                file.write("No issues found.\n")
            else:
                file.write(f"File: {self.filename}\n\n")
                for issue in self.report:
                    file.write(f"Line: {issue['line']}\n")
                    file.write(f"Issue: {issue['explanation']}\n")
                    file.write("-" * 40 + "\n")
        print(f"Report saved to {output_file}")

class PatternIdentifier:
    @staticmethod
    def check_patterns(tree: ast.AST, analyser: StaticAnalyser) -> None:
        LogsInTryBlockChecker(tree, analyser).check()
        # ConstantAreUppercaseChecker(tree, analyser).check()

# Pattern check for Prints/logging in Try blocks
class LogsInTryBlockChecker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST, analyser: StaticAnalyser):
        self.tree = tree
        self.analyser = analyser
        self.in_try_block = False

    def check(self):
        self.visit(self.tree)

    def visit_Try(self, node: ast.Try):
        old_in_try_block = self.in_try_block
        self.in_try_block = True # Visit only the body of the try block and ignore except and finally
        for stmt in node.body:
            self.visit(stmt)
        
        self.in_try_block = old_in_try_block

    def visit_Call(self, node: ast.Call):
        if self.in_try_block:
            stmt_type = None
            if isinstance(node.func, ast.Name) and node.func.id == 'print':
                stmt_type = 'print'
            elif (isinstance(node.func, ast.Attribute) and
                  isinstance(node.func.value, ast.Name) and
                  node.func.value.id == 'logging'):
                stmt_type = 'logging'
            
            if stmt_type:
                explanation = (f"{stmt_type.capitalize()} statement found in "
                               f"try block. Consider using proper error "
                               f"logging in except or finally block instead.\n"
                               f"Ignore, if it serves a needed purpose.")
                self.analyser.report_issue(node.lineno, explanation)
        
        self.generic_visit(node)
        

# For learning purpose - wrote this common pattern 
class ConstantAreUppercaseChecker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST, analyser: StaticAnalyser):
        self.tree = tree
        self.analyser = analyser

    def check(self):
        self.visit(self.tree)

    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if self.is_constant(name, node.value):
                if not name.isupper():
                    explanation = f"Constant variable '{name}' should be in uppercase format."
                    self.analyser.report_issue(node.lineno, explanation)

    @staticmethod
    def is_constant(name: str, value: ast.expr) -> bool:
        return (len(name) > 2 and 
                not name.startswith('_') and 
                isinstance(value, (ast.Constant, ast.Tuple)))
        

