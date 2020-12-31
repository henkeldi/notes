
import * as lexer from './lexer';

test('Must generate tokens from c language', () => {
    const text:string = `
        float match0(char *s)
        {if (!strcmp(s, "0.0", 3))
            return 0.;
        }
    `;
    type TokenType = "FLOAT"|"LPAREN"|"RPAREN"|"IF"|"CHAR"|"RETURN"|"STAR"|"LBRACE"|"RBRACE"
        |"BANG"|"COMMA"|"STRING"|"REAL"|"NUM"|"SEMI"|"ID"
    const token_definition:lexer.TokenDefinition<TokenType>[] = [
        {type: "FLOAT", regex: "float"},
        {type: "LPAREN", regex: "\\("},
        {type: "RPAREN", regex: "\\)"},
        {type: "IF", regex: "if"},
        {type: "CHAR", regex: "char"},
        {type: "RETURN", regex: "return"},
        {type: "STAR", regex: "\\*"},
        {type: "LBRACE", regex: "\\{"},
        {type: "RBRACE", regex: "\\}"},
        {type: "BANG", regex: "\\!"},
        {type: "COMMA", regex: "\\,"},
        {type: "STRING", regex: "\".*\""},
        {type: "REAL", regex: "[0-9]*\\.[0-9]*"},
        {type: "NUM", regex: "[0-9]+"},
        {type: "SEMI", regex: ";"},
        {type: "ID", regex: "[a-zA-Z][a-zA-Z0-9_]*"},
    ];
    const nontoken_definition = " |\n|\r|\\/\\*(\\*(?!\\/)|[^*])*\\*\\/";

    const tokens = lexer.lex(text, token_definition, nontoken_definition);

    const expected_tokens:lexer.Token<TokenType>[] = [
        { type: 'FLOAT', value: 'float' },
        { type: 'ID', value: 'match0' },
        { type: 'LPAREN', value: '(' },
        { type: 'CHAR', value: 'char' },
        { type: 'STAR', value: '*' },
        { type: 'ID', value: 's' },
        { type: 'RPAREN', value: ')' },
        { type: 'LBRACE', value: '{' },
        { type: 'IF', value: 'if' },
        { type: 'LPAREN', value: '(' },
        { type: 'BANG', value: '!' },
        { type: 'ID', value: 'strcmp' },
        { type: 'LPAREN', value: '(' },
        { type: 'ID', value: 's' },
        { type: 'COMMA', value: ',' },
        { type: 'STRING', value: '"0.0"' },
        { type: 'COMMA', value: ',' },
        { type: 'NUM', value: '3' },
        { type: 'RPAREN', value: ')' },
        { type: 'RPAREN', value: ')' },
        { type: 'RETURN', value: 'return' },
        { type: 'REAL', value: '0.' },
        { type: 'SEMI', value: ';' },
        { type: 'RBRACE', value: '}' },
    ];

    expect(tokens).toStrictEqual(expected_tokens);
});
