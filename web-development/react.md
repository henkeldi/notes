
# React

### Install
```bash
yarn add react
yarn add react-dom
yarn add @types/react --dev
yarn add @types/react-dom --dev
```

### Controlled Component

```typescript
import React, { Component } from 'react'

interface MyTextfieldState {
  query: string
}

class MyTextfield extends Component<{}, MyTextfieldState> {

  state = {
    query: ""
  }

  updateQuery = (query:string) => {
    this.setState(() => ({
      query
    }))
  }

  render() {
    return <input
      type="text"    
      placeholder="Query"
      value={this.state.query}
      onChange={(event) => this.updateQuery(event.target.value)}
    />
  }

}

export default MyTextfield
```

### Using API to Fetch Data

*utils/SomeAPI.ts*

```typescript
const api = process.env.REACT_APP_ITEM_API_URL || 'http://localhost:5001'

export interface Item {
    id: string,
}

interface ItemResponse {
    items: Item[]
}
  
const headers = {
    'Accept': 'application/json',
    'Authorization': '<some-token>'
}

export const getAll = async () => {
    const response = await fetch(`${api}/some/api`, { headers })
    return (await response.json() as ItemResponse).items
}

export const remove = async (item:Item) => {
    const response = await fetch(`${api}/some/api/${item.id}`, { method: 'DELETE', headers })
    return (await response.json() as ItemResponse).items
}

export const create = async (item:Item) => {
    const response = await fetch(`${api}/some/api`, {
        method: 'POST',
        headers: {
            ...headers,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(item)
    })
    return await response.json()
}
```

*subcomponent.ts*

```typescript
import { Item } from 'utils/SomeAPI'
import * as SomeAPI from 'utils/SomeAPI'

interface SubComponentState {
  items: Item[],
}

class SubComponent extends Component<{}, SubComponentState> {

  async componentDidMount() {
    const items = await SomeAPI.getAll()
    this.setState({items})
  }

  removeItem(item:Item) {
    this.setState((currentState) => ({
      items: currentState.items.filter((c) => {
        return c.id !== item.id
      })
    }))
    SomeAPI.removeItem(item)
  }

  render() {// render items here}
}
```

### React Router

**Install**

```bash
yarn add react-router-dom
yarn add @types/react-router-dom --dev
```

**index.tsx**

```typescript
import * as ReactDOM from "react-dom";
import * as React from "react";
import { BrowserRouter } from "react-router-dom"

import { App } from './App'

ReactDOM.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
  document.getElementById('root')
)
```

**App.tsx**

```typescript
import * as React from 'react'
import { Route } from 'react-router-dom'

import { ShowItems } from './ShowItems'
import { CreateItem } from './CreateItem'

interface AppState {
    items:string[]
}

export class App extends React.Component<{}, AppState> {

    state = {
        items:[]
    }

    onCreateItem(item:Item) {
        this.setState((prevState => {prevState.items.push(item)}))
    }

    render() {
        return <div>
            <Route exact path='/' render={() =>(
                <ShowItems items={this.state.items} />
            )} />
            <Route path='/create' render={({ history }) => (
                <CreateItem
                    onCreateItem={(item) => {
                        this.onCreateItem(item)
                        history.push('/')
                    }}
                />
            )} />
        </div>
    }
}
```

**ShowItems.tsx**

```typescript
import * as React from 'react'
import { Link } from 'react-router-dom'

interface ShowItemsProps {
    items:string[]
}

export class ShowItems extends React.Component<ShowItemsProps, {}> {

    render() {
        return <div>
            <Link to='/create'>Create new Items</Link>
            <ul>
                {this.props.items.map(s => (
                    <li key={s}>Name: {s}</li>
                ))}
            </ul>
        </div>
    }

}
```

**CreateItems.tsx**

```typescript
import * as React from 'react'
import { Link } from 'react-router-dom'

interface CreateItemState {
  name: string,
}

export interface onCreateFunc {
  (item:string):void
}

interface CreateItemProps {
    onCreateItem:onCreateFunc
}

export class CreateItem extends React.Component<CreateItemProps, CreateItemState> {

  state = {
    name: '',
  }

  handleSubmit = (e:React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      this.props.onCreateItem(this.state.name);
  }

  onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    this.setState({
      'name': event.target.value
    })
  }

  render() {
    return <div>
      <Link to="/">Back</Link>
      <form onSubmit={this.handleSubmit}>
        <div>
          <input type='text' 
            value={this.state.name}
            onChange={this.onChange}
            placeholder='Name' />
          <button>Add Item</button>
        </div>
      </form>
    </div>
  }
}
```