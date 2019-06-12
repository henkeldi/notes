
# Firestore

Emulating Firestore locally

```javascript
exports.calculateCart = functions.firestore.document("carts/{cartId}/items/{itemId}")
  .onWrite(async (change, context) => {
    const cart = db.collection("cards").doc(context.params.cartId);
    const itemPrice = change.after.exists ? change.after.data().price : 0;
    
    console.log(`Ìtem added with price ${itemPrice}, recalculating.`);
    
    await db.runTransaction(async (transaction) => {
        const cartSnap = await transaction.get(cart);
        
        const currentPrice = cartSnap.get("price") || 0;
        const currentCount = cartSnap.get("count") || 0;
        
        return transaction.set(cart, {
            price: currentPrice + itemPrice,
            count: currentCount + 1
        }, { merge: true })
    })  
  })
```

```bash
firebase emulators:start
```