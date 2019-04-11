
# React

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