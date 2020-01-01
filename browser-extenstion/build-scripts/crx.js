const fs = require('fs')

const ChromeExtension = require('crx')

function getPem() {
  const pemFile = './secret/vh-chrome-extension.pem'
  if (fs.existsSync(pemFile)) {
    return fs.readFileSync(pemFile)
  }
  return process.env["CHROME_PEM"]
}

async function build () {
  const crx = new ChromeExtension({
    privateKey: getPem()
  })
  const crxBuffer = await crx.load('./dist').then((crx) => crx.pack())
  fs.writeFileSync('./vh.crx', crxBuffer)
}
console.log("start to build")
fs.writeFileSync("./out.debug","xxxx")
build()
console.log("build over");
