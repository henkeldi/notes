
export interface TokenDefinition<T> {
    type: T,
    regex: string
}

export interface Token<T> {
    type: T,
    value: string
}

export const lex = <T>(text:string, tokenDefinitions:TokenDefinition<T>[], nontokenDefinition:string):Token<T>[] => {
    const tokens:Token<T>[] = []
    const skipRegex = RegExp(nontokenDefinition, "y");
    let currentSearchIndex = 0;
    while (currentSearchIndex < text.length) {
        skipRegex.lastIndex = currentSearchIndex;
        if (skipRegex.test(text)) {
            currentSearchIndex = skipRegex.lastIndex;
        } else {
            const { token, lastIndex } = findToken<T>(text, tokenDefinitions, currentSearchIndex);
            if (token && lastIndex) {
                tokens.push(token);
                currentSearchIndex = lastIndex;
            } else {
                const prettyText = removeLineBreaksAndTabs(text.substr(currentSearchIndex));
                throw Error(`Got input that did not match any definition: ${prettyText}`);
            }
        }
    }
    return tokens;
}

const findToken = <T>(text:string, tokenDefinitions:TokenDefinition<T>[], lastIndex:number):TokenSearchResult<T> => {
    for (const token of tokenDefinitions) {
        const regExp = RegExp(token.regex, "y");
        regExp.lastIndex = lastIndex;
        const match = regExp.exec(text);
        if (match) {
            return {
                token: { type: token.type, value: match[0] },
                lastIndex: regExp.lastIndex
            }
        }
    }
    return {}
}

const removeLineBreaksAndTabs = (text:string) => {
    return text.replace(/\n/g,"\\n").replace(/\t/g,"\\t");
}

interface TokenSearchResult<T> {
    token?: Token<T>,
    lastIndex?: number
}
