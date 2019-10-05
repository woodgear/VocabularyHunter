/* global chrome */
import { parserArticle } from './content_parser'
console.log('i am a content script')

chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  console.log(
    sender.tab
      ? 'from a content script:' + sender.tab.url
      : 'from the extension'
  )
  if (msg.action === 'parser') {
    const res = onParserArticle()
    console.log(res)

    sendResponse(res)
  }
})

function onParserArticle () {
  console.log('onParserArticle')
  return { article: parserArticle(document.body) }
}
