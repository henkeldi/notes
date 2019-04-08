
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