from ravenfall.lexer import tokenize 
import pprint as ppr

def pprint(contents):
    print('')
    ppr.pprint(contents)
    print('')

if __name__ == '__main__':
    with open('examples/code_basic/main.rf', 'r') as file:
        source_code = file.read()
        token_stream = tokenize(source_code)

        pprint(token_stream)
        # pprint(output)


