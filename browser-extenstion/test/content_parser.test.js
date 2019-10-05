import { assert } from 'chai'
import puppeteer from 'puppeteer'
import { exec } from 'child_process'
import path from 'path'
const executablePath = './chrome-linux/chrome'

async function buildDomUtil () {
  return new Promise((res, rej) => {
    exec('npx webpack --env build-dom-util --mode development', (err, stdout) => {
      if (err) {
        rej(err)
      }
      res('./dist/dom_util.js')
    })
  })
}

describe('ParserArticle shoud correct', () => {
  let browser = null
  // 编程的艺术就在于抽象和复制粘贴

  before(async () => {
    browser = await puppeteer.launch(
      {
        executablePath
        // headless: false,
        // slowMo: 3000,
        // devtools: true
      }
    )
  })

  after(async () => {
    await browser.close()
  })

  async function testParserArticle (filePath, expectTxt) {
    const page = await browser.newPage()
    await page.goto(filePath)
    const domUtilPath = await buildDomUtil()
    await page.addScriptTag({ path: domUtilPath })
    const result = await page.evaluate(async () => {
      /* eslint no-undef: "off" */
      return Promise.resolve(domUtil.parserArticle(document.body))
    })
    console.log('result', result)
    assert.equal(result, expectTxt)
  }

  it('for debug parserArticle', async () => {
    const page = await browser.newPage()
    await page.goto('file:///home/oaa/lab/VocabularyHunter/browser-extenstion/mock-data/test.html')
    const domUtilPath = await buildDomUtil()
    await page.addScriptTag({ path: domUtilPath })
    const result = await page.evaluate(async () => {
      return Promise.resolve(domUtil.parserArticle(document.body))
    })
    console.log('result', result)
  })

  it('should get corrent data', async () => {
    const filePath = `file://${path.join(process.cwd(), 'mock-data/test.html')}`
    await testParserArticle(filePath, 'ssssssss\n\nppppppp\n\nVisit W3Schools.com!')
  })
})
