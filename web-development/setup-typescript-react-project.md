
# Setup Typescipt React Project

#### package.json

```json
{
    "name": "<package-name>",
    "description": "",
    "version": "0.0.1",
    "scripts": {
        "dev": "./node_modules/.bin/webpack-dev-server --hot --inline --open --config webpack.dev.js",
        "build": "./node_modules/.bin/webpack --config webpack.prod.js"
    },
    "author": "<author>",
    "license": "ISC",
    "dependencies": {
        "react": "^16.8.4",
        "react-dom": "^16.8.4"
    },
    "devDependencies": {
        "@types/react": "^16.8.8",
        "@types/react-dom": "^16.8.2",
        "terser-webpack-plugin": "^1.2.3",
        "ts-loader": "^5.3.3",
        "tslint": "^5.14.0",
        "typescript": "^3.3.3333",
        "webpack": "^4.29.6",
        "webpack-cli": "^3.3.0",
        "webpack-dev-server": "^3.2.1",
        "webpack-merge": "^4.2.1"
    }
}
```

#### tsconfig.json

```json
{
    "compilerOptions": {
        "noImplicitAny": true,
        "removeComments": true,
        "preserveConstEnums": true,
        "sourceMap": true,
        "module": "commonjs",
        "target": "es2017",
        "jsx": "react"
    },
    "include": [
        "src/**/*"
    ],
    "exclude": [
        "node_modules",
        "**/*.spec.ts"
    ]
}
```

#### webpack.common.js

```javascript
const path = require('path');

module.exports = {
    entry: {
        app: path.join(__dirname, 'src', 'index.tsx')
    },
    output: {
        path: path.join(__dirname, 'static', 'js')
    },
    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.json']
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                loader: 'ts-loader'
            }
        ]
    }
}
```

#### webpack.dev.js

```javascript
const merge = require('webpack-merge');
const path = require('path');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    mode: 'development',
    devtool: 'inline-source-map',
    devServer: {
        contentBase: path.join(__dirname, 'static'),
        publicPath: '/js'
    },
})
```

#### webpack.prod.js

```javascript
const merge = require('webpack-merge');
const TerserPlugin = require('terser-webpack-plugin');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    mode: 'production',
    devtool: 'source-map',
    optimization: {
        minimizer: [new TerserPlugin()],
    },
})
```


#### static/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Page</title>
    <meta charset="utf-8">
</head>
<body style="margin: 0" >
    <div id="app"></div>
    <script src="js/app.js"></script>
</body>
</html>
```

#### src/index.tsx

```typescript
import * as React from "react";
import * as ReactDOM from "react-dom";

ReactDOM.render(
    <h1>Hello, world!</h1>,
    document.getElementById('app')
);
```

#### Install dependencies

```bash
npm install
```

#### Run webpack dev server

```bash
npm run dev
```

#### Build project for deployment

```bash
npm run build
```
