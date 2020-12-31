
import * as parser from './parser';

test('Must parse context free grammer', () => {
    const grammer:parser.GrammerRule[] = [
        {nonterminal: "S", rule: ["if", "E", "then", "S", "else", "S"]},
        {nonterminal: "S", rule: ["begin", "S", "L"]},
        {nonterminal: "S", rule: ["print", "E"]},
        {nonterminal: "L", rule: ["end"]},
        {nonterminal: "L", rule: [";", "S", "L"]},
        {nonterminal: "E", rule: ["num", "=", "num"]},
    ];

    const root = parser.parse(tokens, grammer);
});
