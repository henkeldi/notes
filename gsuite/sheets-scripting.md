
# Google Sheets Scripting

```
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Tests')
      .addItem('run', 'run')
      .addItem('runSelected', 'runSelected')
      .addToUi();
}

function runSelected() {
  const sheet = SpreadsheetApp.getActiveSheet();
  var ranges = sheet.getActiveRangeList().getRanges()
  for (var i = 0; i < ranges.length; i++) {
    var range = ranges[i]
    doStuffWithRow(range.getRow()-1, range.getLastRow())
  }  
}

function run() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const range = sheet.getDataRange();
  const values = range.getValues();
  const startRow = 0
  const endRow = values.length
  for (var row = startRow; row < endRow; row++) {
    var entry = values[row][1]
    sheet.getRange(row, 4).setValue("<content>")
  }
}
```
