from ravenfall.frontend.lexer import tokenize 
from ravenfall.frontend.parser import Parser
import pprint as ppr

def pprint(contents):
    print('')
    ppr.pprint(contents)
    print('')

if __name__ == '__main__':
    parser = Parser()
    
    with open('examples/code_basic/main.rf', 'r') as file:
        source_code = file.read()
        token_stream = tokenize(source_code)
        ast = parser.produce_ast(token_stream)
        
        # pprint(token_stream)
        pprint(ast)
