
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
        "target": "es5",
        "lib": [
          "dom",
          "dom.iterable",
          "esnext"
        ],
        "noImplicitAny": true,
        "removeComments": true,
        "preserveConstEnums": true,
        "allowSyntheticDefaultImports": true,
        "strict": true,
        "sourceMap": true,
        "module": "esnext",
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
        bundle: path.join(__dirname, 'src', 'index.tsx')
    },
    output: {
        path: path.join(__dirname, 'public', 'js')
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
        contentBase: path.join(__dirname, 'public'),
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


#### public/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1, shrink-to-fit=no"
  />
  <title>My Page</title>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
  <script src="js/bundle.js"></script>
</body>
</html>
```

#### src/index.tsx

```typescript
import ReactDOM from "react-dom";
import React from "react";

import SubComponent from './subcomponent'

ReactDOM.render(
  <SubComponent />,
  document.getElementById('root')
)
```

#### src/subcomponent.tsx

```typescript
import React, { Component } from 'react'

class SubComponent extends Component<{}, {}> {

  render() {
    return <h1>Hello World</h1>;
  }

}

export default SubComponent;
```

#### Install dependencies

```bash
yarn install
```

#### Run webpack dev server

```bash
yarn dev
```

#### Build project for deployment

```bash
yarn build
```
