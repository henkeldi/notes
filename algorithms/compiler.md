
# Compiler

## Lexer

Step 1: Define tokens

| Type  | Example | Regex |
| ------|------ | ------------- |
| `ID` | temp data | [a-zA-Z][a-zA-Z0-9]* |
| `NUM` | 13 43 | [0-9]+ |
| `COMMA` | , | , |
| `LPAREN` | ( | ( |

Step 2: Define skip regexes

| Type  | Example | Regex |
| ------|------ | ------------- |
| Comment | # bla blubb | '#' [a-z]* '\n' |
| Whitespace | ' ' '\t' '\n' | (' '\|'\t'\|'\n')+ |

## Parser

### Recursive-Descent Parser

*Use if first symbol of every grammer rule starts with terminal symbol.*

```
S -> if E then S else S
S -> begin S L
S -> print E
L -> end
L -> ; S L
E -> num = num
```

Parser code:

```java
final int IF=1, THEN=2, ELSE=3, BEGIN=4, END=5, PRINT=6, SEMI=7, NUM=8, EQ=9;

int tok = getToken();
void advance() {tok = getToken();}
void eat(int t) {if (tok==t) advance(); else error();}

void S() {
    switch(tok) {
        case IF: eat(IF); E(); eat(THEN); S(); eat(ELSE); S(); break;
        case BEGIN: eat(BEGIN); S(); L();
        case PRINT: eat(PRINT); E();
        default : error();
    }
}
void L() {
    switch(tok) {
        case END: eat(END); break;
        case SEMI: eat(SEMI); S(); L(); break;
    }
}
void E() {eat(NUM); eat(EQ); eat(NUM);}
```

# Reference

* [Moder Compiler Implementation in Java by Andrew Appel](https://www.amazon.de/Modern-Compiler-Implementation-Andrew-Appel/dp/052182060X)
