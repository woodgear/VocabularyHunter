import { assert } from 'chai'
import puppeteer from 'puppeteer'
import { exec } from 'child_process'
import path from 'path'
import { writeFileSync } from 'fs'
import *  as dom from '../src/content_parser'
const executablePath = './chrome-linux/chrome'

async function buildDomUtil() {
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
        executablePath,
        headless: false,
        slowMode: 300000,
        devtools: true
      }
    )
  })

  after(async () => {
    await browser.close()
  })

  async function testParserArticle(filePath, expectTxt) {
    const page = await browser.newPage()
    await page.goto(filePath)
    const domUtilPath = await buildDomUtil()
    await page.addScriptTag({ path: domUtilPath })
    const result = await page.evaluate(async () => {
      /* eslint no-undef: "off" */
      return Promise.resolve(domUtil.parserArticle(document))
    })
    console.log('result', result)
    assert.equal(result, expectTxt)
  }

  it.only('for debug parserArticle', async () => {
    const page = await browser.newPage()
    await page.goto("https://sites.fas.harvard.edu/~lib215/reference/programming/unix-esr.html")
    const domUtilPath = await buildDomUtil()
    await page.addScriptTag({ path: domUtilPath })
    const result = await page.evaluate(async () => {
      return Promise.resolve(domUtil.parserArticle(document))
    })
    console.log(result.content)
    writeFileSync("content.data", result.content);
    writeFileSync("content.data.json",JSON.stringify(result.content));
    
    // assert.equal(result.title, "I made a NES emulator in Rust using generators");
  }).timeout(100 * 1000)

  // it('should get corrent data', async () => {
  //   const filePath = `file://${path.join(process.cwd(), 'mock-data/test.html')}`
  //   await testParserArticle(filePath, 'ssssssss\n\nppppppp\n\nVisit W3Schools.com!')
  // })


  it('test parser', async () => {
    let data = { a: "a" }
    assert.equal(dom._access(data, [{ "type": "object", "field": "a" }]), data.a)
    data = { a: { "a": "a" } }
    assert.equal(dom._access(data, [{ "type": "object", "field": "a" }]), data.a)
    data = { a: ["a"] }
    assert.equal(dom._access(data, [{ "type": "object", "field": "a" }, { "type": "array", "index": 0 }]), data.a[0])

    assert.deepEqual(dom.str2cmd(".a"), [{ "type": "object", "field": "a" }])
    assert.deepEqual(dom.str2cmd("[1]"), [{ "type": "array", "index": "1" }])
    assert.deepEqual(dom.str2cmd(".a[1]"), [{ "type": "object", "field": "a" }, { "type": "array", "index": "1" }])
    assert.deepEqual(dom.str2cmd("[1].a"), [{ "type": "array", "index": "1" }, { "type": "object", "field": "a" }])
    assert.deepEqual(dom.str2cmd("[\"ccccc\"].a"), [{ "type": "array", "index": "ccccc" }, { "type": "object", "field": "a" }])

    data = { a: "a" }
    assert.equal(dom.access(data, ".a"), data.a)
    data = { a: { "a": "a" } }
    assert.equal(dom.access(data, ".a.a"), data.a.a)
    data = { a: ["a"] }
    assert.equal(dom.access(data, ".a[0]"), data.a[0])
  })
})
