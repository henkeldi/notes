
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

# Reference

* [Moder Compiler Implementation in Java by Andrew Appel](https://www.amazon.de/Modern-Compiler-Implementation-Andrew-Appel/dp/052182060X)
