const fs = require('fs')

const ChromeExtension = require('crx')

async function build () {
  const crx = new ChromeExtension({
    privateKey: fs.readFileSync('./vh-chrome-extension.pem')
  })
  const crxBuffer = await crx.load('./dist').then((crx) => crx.pack())
  fs.writeFileSync('./vh.crx', crxBuffer)
}

build()
