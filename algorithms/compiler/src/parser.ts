
export interface GrammerRule {
    nonterminal: string,
    rule: string[]
}

class Node {

};

export const parse = (grammer:GrammerRule[]):Node => {

    return new Node();
};
