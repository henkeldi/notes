
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
const { FuseBox,
    CSSPlugin,
    WebIndexPlugin,
    ImageBase64Plugin,
} = require("fuse-box");

const fuse = FuseBox.init({
    homeDir: "src",
    output: "public/$name.js",
    target: "browser@es2018",
    sourceMaps: true,
    plugins: [
        WebIndexPlugin({
            title: "<Webpage Title>",
            template: "src/index.html",
        }),
        CSSPlugin(),
        ImageBase64Plugin()
    ]
});

fuse.bundle('vendor').instructions('~ **/**.tsx');
fuse.bundle("bundle").instructions(`!> [index.tsx]`).watch().hmr();

fuse.dev();

fuse.run();
```

#### src/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1, shrink-to-fit=no"
  />
  <title>$title</title>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
  $bundles
</body>
</html>
```

#### src/index.tsx

```typescript
import * as ReactDOM from "react-dom";
import * as React from "react";

import './styles/main.css'

import SubComponent from './subcomponent'

ReactDOM.render(
  <SubComponent />,
  document.getElementById('root')
)
```

#### src/subcomponent.tsx

```typescript
import * as React from 'react';

class SubComponent extends React.Component<{}, {}> {

  render() {
    return <h1>Hello World</h1>;
  }

}

export default SubComponent;
```


#### styles/main.css

```css
body {
    padding: 100px;
    background: white;
}
```
#### images.d.ts
```
declare module "*.jpeg";
declare module "*.jpg";
declare module "*.gif";
declare module "*.png";
declare module "*.svg";
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
