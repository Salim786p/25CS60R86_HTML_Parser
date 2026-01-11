# Mini HTML Parser and DOM Builder using PLY

## Course
CS69202 – Design Lab

## Topic
Mini HTML Parser and DOM Builder using PLY (Python Lex-Yacc)

---

## 1. Problem Overview

This project implements a mini HTML parser for a restricted subset of HTML as specified in the Design Lab assignment.  
The parser performs lexical analysis, syntax analysis, semantic validation, constructs a DOM-like hierarchical tree, and serializes the result into JSON format.

The objective is to apply compiler design concepts such as tokenization, context-free grammar parsing, parse tree construction, and semantic checking using PLY.

---

## 2. Supported HTML Subset

### 2.1 Supported Tags and Attributes

| Tag | Supported Attributes |
|-----|----------------------|
| `div` | `id`, `class` |
| `p` | `id`, `align`, `class` |
| `a` | `id`, `href`, `target`, `class` |

### 2.2 Attribute Rules

- Attributes are optional  
- Attributes appear only in opening tags  
- Attribute values must be enclosed in double quotes  
- Attribute order is not significant  
- Duplicate attributes on the same tag are not allowed  
- Attributes not listed for a tag raise a semantic error  

---

## 3. System Architecture

The parser follows the standard compiler pipeline:

```
HTML Input
   ↓
Lexical Analysis (PLY Lexer)
   ↓
Syntax Analysis (PLY YACC Parser)
   ↓
Semantic Validation
   ↓
DOM Tree Construction
   ↓
JSON Serialization
```

---

## 4. Lexical Analysis

### 4.1 Design Rationale

HTML tokenization is context-sensitive:
- Outside HTML tags, text is treated as plain content
- Inside `< >`, tag names, attribute names, and values must be tokenized separately

To handle this correctly, the lexer uses exclusive states.

```python
states = (
    ('tag', 'exclusive'),
)
```

### 4.2 Lexer States

| State | Purpose |
|-------|---------|
| `INITIAL` | Tokenizes text outside HTML tags |
| `tag` | Tokenizes tag names and attributes inside `< >` |

### 4.3 Tokens

```python
tokens = (
    'LTSLASH', 'LT', 'GT',
    'ID', 'EQUALS', 'STRING',
    'TEXT'
)
```

### 4.4 Token Definitions

#### Entering Tag State

```python
def t_LT(t):
    r'<'
    t.lexer.begin('tag')
    return t

def t_LTSLASH(t):
    r'</'
    t.lexer.begin('tag')
    return t
```

#### Exiting Tag State

```python
def t_tag_GT(t):
    r'>'
    t.lexer.begin('INITIAL')
    return t
```

#### Tokens Inside Tags

```python
def t_tag_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t

def t_tag_EQUALS(t):
    r'='
    return t

def t_tag_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t
```

#### Text Outside Tags

```python
def t_TEXT(t):
    r'[^<>]+'
    return t
```

### 4.5 Lexer Error Handling

```python
def t_error(t):
    print(f"Lexer Error: Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

def t_tag_error(t):
    print(f"Lexer Error (tag): Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)
```

---

## 5. Syntax Analysis

### 5.1 Grammar Rules

```ebnf
document   → content
content    → content element | ε
element    → '<' ID attributes '>' content '</' ID '>'
element    → TEXT
attributes → attributes attribute | ε
attribute  → ID '=' STRING
```

---

## 6. Semantic Validation

Semantic checks performed during parsing include:

- Matching of opening and closing tags
- Validation of supported tags
- Validation of supported attributes per tag
- Detection of duplicate attributes

Errors are reported with line numbers wherever possible.

---

## 7. Data Structures

### 7.1 DOM Node Representation

Each node in the DOM tree is represented as a Python dictionary.

#### Element Node

```json
{
  "type": "ELEMENT",
  "tagName": "div",
  "attributes": { "id": "root" },
  "children": []
}
```

#### Text Node

```json
{
  "type": "TEXT",
  "value": "Hello",
  "children": []
}
```

---

## 8. Output Generation

After successful parsing and validation, the DOM tree is serialized into JSON format using Python’s `json` module.

```python
json.dump(result, f, indent=4)
```

The output is written to `output.json`.

---

## 9. Files Included

| File | Description |
|------|------------|
| `parser.py` | Lexer and parser implementation |
| `input.html` | Sample HTML input |
| `output.json` | Generated DOM tree |
| `README.md` | Project documentation |

---

## 10. Conclusion

This project demonstrates the application of compiler design principles to parse a restricted subset of HTML using PLY.  
The implementation adheres strictly to the Design Lab constraints and produces a validated DOM structure serialized in JSON format.
