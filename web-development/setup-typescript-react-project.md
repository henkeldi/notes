
# Setup Typescipt React Project

#### package.json

```json
{
  "name": "<package-name>",
  "description": "<description>",
  "version": "0.0.1",
  "author": "<autor>",
  "license": "ISC",
  "scripts": {
    "dev": "node fuse"
  },
  "dependencies": {
    "react": "^16.8.4",
    "react-dom": "^16.8.4"
  },
  "devDependencies": {
    "@types/react": "^16.8.8",
    "@types/react-dom": "^16.8.2",
    "fuse-box": "^3.7.1",
    "ts-loader": "^5.3.3",
    "tslint": "^5.14.0",
    "typescript": "^3.3.3333"
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

#### fuse.js

```javascript
const { FuseBox } = require("fuse-box");

const fuse = FuseBox.init({
    homeDir: "src",
    output: "public/$name.js",
});

fuse.bundle('vendor').instructions('~ **/**.tsx');
fuse.bundle("bundle").instructions(`!> [index.tsx]`).watch().hmr();

fuse.dev();

fuse.run();
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
  <script src="js/vendor.js"></script>
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

#### Run dev server

```bash
yarn dev
```

#### Build project for deployment

```bash
yarn build
```
