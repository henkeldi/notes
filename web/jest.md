
# Jest

**lexer.test.ts**

```ts
test('', ()=>{
    
})
```

**lexer.ts**

```ts
test('', ()=>{
    
})
```

**package.json**

```json
{
  "name": "compiler",
  "version": "1.0.0",
  "description": "",
  "main": "jest.tsc.config.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {},
  "devDependencies": {
    "@types/jest": "^26.0.19",
    "@types/mocha": "^8.2.0",
    "ts-jest": "^26.4.4"
  }
}
```

**tsconfig.json**

```json
{
    "compilerOptions": {
        "target": "esnext",
        "lib": ["esnext"],
        "module": "esnext",
        "noImplicitAny": true,
        "strict": true,
        "sourceMap": true,
        "types": ["jest"],
    },

    "include": [
        "src/**/*.ts"
    ],
    "exclude": [
        "node_modules",
        "**/*.spec.ts",
    ]
}
```
