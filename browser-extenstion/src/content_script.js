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
    const article = onParserArticle()
    console.log(res,JSON.stringify({article}))

    sendResponse(res)
  }

  if (msg.action==="saveCorpus") {
    const {title,content} = onParserArticle();
    const url = window.location.href;
    sendResponse({title,article:content,url})
  }

})

function onParserArticle () {
  return  parserArticle(document)
}
