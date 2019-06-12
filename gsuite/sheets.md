
# Google Sheets with NodeJS

## Installation

```bash
npm install googleapis
```

## Hello World example

* Get *Speadsheet ID* from the browser url of the sheet

```javascript
const { google } = require('googleapis');

const SCOPES = ['https://www.gooogleapis.com/auth/spreadsheets'];

const sheet = google.sheets({
    version,
    auth
});

await sheets.spreadsheets.values.update({
    speadsheetId,
    range: 'A1',
    resource: {
        values: [['Hello World!']]
    },
});
```

# Links
* [Sheets API](https://www.developers.google.com/sheets/api/)
* [Cloud Functions](https://www.cloud.google.com/functions/)
* [Cloud Scheduler](https://www.cloud.google.com/scheduler/)
