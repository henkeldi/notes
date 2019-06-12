
# Puppeteer

*Browser Automation Library. Puppeteer = Node.js + Chrome. Open pages, navigate to websites, evaluate Javascript*

## Installation

```bash
npm install puppeteer
```

## Usage

```javascript
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://joel.tools/merch');
  const price = await page.$eval('.price', div => div.textContent);
  console.log(price);
  await browser.close();
})();
```

Puppeteer for Firefox

```bash
npm install puppeteer-firefox
```

Browser context to speed up tests

```javascript
const browser = await puppeteer.launch();

it('should have a pay button', async () => {
  const context = await browser.createIncognitoBrowserContext();
  const page = await context.newPage();
  await page.goto('https://joel.tools/merch');
  expect(await page.$('button.gpay-button')).toBeTruthy();
  await context.close();
})
```

Flaky tests (tests that sometimes pass sometimes don't)

```javascript
it('should pay', async () =>{
  const page = await context.newPage();
  await page.goto('https://joel.tools/merch/');
  await page.waitForSelector('button.gpay-button');

  const response = page.waitForResponse(res => res.url().endsWith('/pay'));
  await page.click('button.gpay-button');
  await response;
  assert(await page.$('.successful-purchase'));
});
```

# Source

[Modern Web Testing and Automation with Puppeteer](https://www.youtube.com/watch?v=MbnATLCuKI4)
