
# JavaScript

## New in JavaScript 2019

Private fields

```javascript
class IncrementCounter
    #count = 0;
    get value() {
        return this.#count;
    }
    increment(){
        this.#count++;
    }
}
```

Flat lists

```javascript
// Flatten one level:
const array = [1, [2, [3]]]
array.flat();
// -> [1, 2, [3]]


// Flatten recursively until the array contains no
// more nested arrays:
array.flat(Infinity);
// -> [1, 2, 3]
```

Flat map

```javascript
const duplicate = (x) => [x, x];

[2, 3, 4].map(duplicate);
// -> [[2, 2], [3, 3], [4, 4]]

[2, 3, 4].map(duplicate).flat(); // slow
// -> [2, 2, 3, 3, 4, 4]

[2, 3, 4].flatMap(duplicate); // fast
// -> [2, 2, 3, 3, 4, 4]
```

Relative Time Format

```javascript
const rtf = new Intl.RelativeTimeFormat('en', {numeric: 'auto'});

rtf.format(-1, 'day');
// -> 'yesterday'

rtf.format(0, 'day');
// -> 'today'

rtf.format(1, 'day');
// -> 'tomorrow'

rtf.format(-1, 'week');
// -> 'last week'
```

ListFormat

```javascript
const lfEnglish = new Intl.ListFormat('en', { type: 'disjunction' });
lfEnglish.format(['Ada', 'Grace']);
// -> 'Ada and Grace'

lfEnglish.format(['Ada', 'Grace', 'Ida']);
// -> 'Ada, Grace and Ida'
```

Format Range

```javascript
const start = new Date(startTimestamp)
// -> 'May 7, 2019'

const end = new Date(endTimestamp)
// -> 'May 9, 2019'

const fmt = new Intl.DateTimeFormat('en', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})
const output = fmt.formatRange(start, end);
// -> 'May 7 - 9, 2019'
```
