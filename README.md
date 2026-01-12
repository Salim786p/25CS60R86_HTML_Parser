# Mini HTML Parser and DOM Builder using PLY

## Course
 - Design Lab (CS69202)
 - Roll Number - 25CS60R86
 - Name - Salim Akhter Ansari


## 1. Problem Overview

This Assignment implements a **mini HTML parser** for a restricted subset of HTML.  
The parser performs **lexical analysis**, **syntax analysis**, **semantic validation**, constructs a **DOM-like hierarchical tree**, and serializes the result into **JSON format**.

The implementation strictly follows compiler design principles and uses **PLY only**, without relying on any external HTML/XML parsing libraries.

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
- Attribute values must be enclosed in **double quotes**  
- Attribute order is not significant  
- Duplicate attributes on the same tag are not allowed  
- Attributes not listed for a tag raise a **semantic error**

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

HTML tokenization is **context-sensitive**:

- Outside tags → text content
- Inside `< >` → tag names, attribute names, and attribute values

To correctly distinguish these contexts, the lexer uses **exclusive lexer states**.

---

### 4.2 Lexer States

```python
states = (
    ('tag', 'exclusive'),
)
```

| State | Purpose |
|------|---------|
| `INITIAL` | Tokenizes text outside HTML tags |
| `tag` | Tokenizes tag names and attributes inside `< >` |

---

### 4.3 Tokens

```python
tokens = (
    'LTSLASH', 'LT', 'GT',
    'ID', 'EQUALS', 'STRING',
    'TEXT'
)
```

---

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
    r'[^<>\n]+'
    return t
```

---

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

## 5. Syntax Analysis (Grammar)

The grammar below is extracted **directly from the implementation** and is **LALR(1)-compatible**, as verified using `parser.out`.

### 5.1 Grammar Rules (Exact)

```ebnf
document   → content

content    → content element
           | ε

element    → '<' ID attributes '>' content '</' ID '>'
           | TEXT

attributes → attributes attribute
           | ε

attribute  → ID '=' STRING
```

---

## 6. Semantic Validation

Semantic checks are embedded inside parser actions:

- Matching of opening and closing tag names
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
  "attributes": {
    "id": "root"
  },
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

After successful parsing and semantic validation, the DOM tree is serialized into JSON format using Python’s `json` module.

```python
json.dump(result, f, indent=4)
```

The output is written to `output.json`.

---

## 9. Files Included

| File | Description |
|------|------------|
| `25CS60R86.py` | Lexer and parser implementation |
| `input.html` | Sample HTML input |
| `output.json` | Generated DOM tree |
| `README.md` | Project documentation |

---

## 10. Notes on Grammar Correctness

- The grammar avoids ambiguous productions such as `A → A A`
- Left recursion in `content → content element` is **safe in LALR(1)** parsing
- Grammar correctness is validated via the generated `parser.out`

---

12 JAN 2026