
# Firebase Functions

Scheduled Functions

```javascript
exports.scheduledJob = functions.pubsub.schedule("every day 03:00").onRun(async() => {
    console.log("All done! See you tomorrow morning!")
})
```

Run when file added to storage:

```javascript
exports.scanReceipt = functions.storage.object().onFinalize( (object) => {
    // Determine the bucket and path that triggered s
    const fileBucket = object.bucket;
    const filePath = object.name;
    
    // Get the UID and file name from the path
    const uid = path.dirname(filePath).substring(filePath.indexOf('/') +1);
    const fileName = path.basename(filePath);
    
    // Call Cloud Vision to find text in the receipt
    const visionClient = new vision.ImageAnnotatorClient();
    return visionClient.textDetection(`gs://${fileBucket}/${filePath}`).then((result) =>{
        const detections = result.textAnnotations;
        
        // Find the total amount in this receipt
        const amount = receipt.findTotal(detections);
        
        // Determine the document to write the amount from this receipt to
        let expenseDoc = admin.firestore().doc(`users/${uid}/expenses/${fileName}`);
        
        // Write the amount to this new document
        return expenseDoc.set({
            created_at: admin.firestore.FieldValue.serverTimestamp(),
            item_cost: amount
        });
    });
});
```

Run when firestore entry is created:

```javascript
exports.calculateUserCost = functions.firestore
    .document('users/{uid}/expenses/{expenseId}').onCreate((snap, context)=>{
    // Determine the UID and the amount of the receipt
    const amount = snap.data().item_cost;
    const uid = context.params.uid;
    
    // Increase the user_mount for the user
    return admin.firestore().collection('users').doc(uid).set({
        user_cost: admin.firestore.FieldValue.increment(amount),
        last_updated: admin.firestore.FieldValue.serverTimestamp()
    }, {merge: true});
    
})
```

Run when firestore entry is updated:

```javascript
exports.calculateUserCost = functions.firestore
    .document('users/{uid}').onWrite((change, context)=>{
    let old_total = change.before && change.before.data() && change.before.data().user_cost ? change.before.data().user_cost;
    let new_total = change.after.data().user_cost;    
    
    if (old_total === new_total) return true;

    // Load all user documents
    return admin.firestore().collection('users').get().then((querySnapshot)=>{
        let promises = [];
        querySnapshot.forEach((doc)=>{
            promises.push(
                doc.ref.update({
                    team_cost: admin.firestore.FieldValue.incerement(new_total - old_total),
                    last_update: admin.firestore.FieldValue.serverTimestamp()
                });
            );
        });
        return Promise.all(promises);
    });
})
``