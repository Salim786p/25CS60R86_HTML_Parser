import ply.lex as lex
import ply.yacc as yacc
import json
import sys

# -----------------------------------------------------------------------------
# LEXER
# -----------------------------------------------------------------------------

tokens = (
    'LTSLASH', 'LT', 'GT', 'EQUALS', 'ID', 'STRING', 'TEXT'
)

states = (
    ('tag', 'exclusive'),
)

# Supported Tags and Attributes mapping 
SUPPORTED_TAGS = {
    'div': ['id', 'class'],
    'p': ['id', 'align', 'class'],
    'a': ['id', 'href', 'target', 'class']
}

t_tag_ignore = ' \t'
t_ignore = ''


def t_LTSLASH(t):
    r'</'
    t.lexer.begin('tag')
    return t

def t_LT(t):
    r'<'
    t.lexer.begin('tag')
    return t

def t_tag_GT(t):
    r'>'
    t.lexer.begin('INITIAL')
    return t

# def t_EQUALS(t):
#     r'='
#     return t

def t_TEXT(t):
    r'[^<>\n]+'
    return t

def t_tag_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t

def t_tag_EQUALS(t):
    r'='
    return t

def t_tag_STRING(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t

# def t_STRING(t):
#     r'\"[^\"]*\"'
#     t.value = t.value[1:-1] # Strip double quotes [cite: 21]
#     return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Lexer Error: Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

def t_tag_error(t):
    print(f"Lexer Error (tag): Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# -----------------------------------------------------------------------------
# PARSER & SEMANTIC VALIDATION
# -----------------------------------------------------------------------------

def p_document(p):
    '''document : content'''
    p[0] = {
        "type": "ELEMENT",
        "tagName": "document",
        "attributes": {},
        "children": p[1]
    }


def p_element_node(p):
    '''element : LT ID attributes GT content LTSLASH ID GT'''
    # Semantic Check: Tag Matching 
    if p[2] != p[7]:
        print(f"Semantic Error: Mismatched tags <{p[2]}> and </{p[7]}> at line {p.lineno(2)}")
        sys.exit(1)
    
    # Semantic Check: Supported Tags [cite: 146]
    if p[2] not in SUPPORTED_TAGS:
        print(f"Semantic Error: Unsupported tag <{p[2]}> at line {p.lineno(2)}")
        sys.exit(1)

    # Validate attributes for this specific tag [cite: 147]
    valid_attrs = SUPPORTED_TAGS[p[2]]
    for attr_name in p[3]:
        if attr_name not in valid_attrs:
            print(f"Semantic Error: Tag <{p[2]}> does not support attribute '{attr_name}'")
            raise SyntaxError("message")


    p[0] = {
        "type": "ELEMENT",
        "tagName": p[2],
        "attributes": p[3],
        "children": p[5]
    }

def p_element_text(p):
    '''element : TEXT'''
    p[0] = {
        "type": "TEXT",
        "value": p[1],
        "children": []
    }

def p_attributes(p):
    '''attributes : attributes attribute
                  | empty'''
    if len(p) == 3:
        p[0] = p[1]
        for k in p[2]:
            if k in p[0]:
                print(f"Semantic Error: Duplicate attribute '{k}'")
                sys.exit(1)
        p[0].update(p[2])
    else:
        p[0] = {}

def p_attribute(p):
    '''attribute : ID EQUALS STRING'''
    p[0] = {p[1]: p[3]}


def p_content(p):
    '''content : content element
               | empty'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = []

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Syntax Error: Unexpected token '{p.value}' at line {p.lineno}")
    else:
        print("Syntax Error: Unexpected End of File") # [cite: 152]

parser = yacc.yacc(debug = True)

# -----------------------------------------------------------------------------
# EXECUTION
# -----------------------------------------------------------------------------

def main():
    try:
        with open("input.html", "r") as f:
            data = f.read()
        
        result = parser.parse(data)
        
        if result:
            with open("output.json", "w") as f:
                json.dump(result, f, indent=4) # [cite: 46-47]
            print("Successfully parsed. Output written to output.json")
    except FileNotFoundError:
        print("Error: input.html not found.")

if __name__ == "__main__":
    main()