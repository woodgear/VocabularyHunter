/* global chrome */
import * as tools from "./browser/browser_tool";
import init from './init'
import Api from './api'

async function saveCorpus() {
  const data = await tools.sendToContentScript({ "action": "saveCorpus" });
  console.log("get data from content script", data.title, data.url, data.article.length);
  const { userId, vhServer } = await init();
  console.log(userId, vhServer)
  const api = new Api(userId, vhServer);
  await api.saveCorpus(data.article, data.title, data.url)
  console.log("ok");
}

function initRightClickMenu() {
  const title = "save this article to vh";
  const id = chrome.contextMenus.create({
    "title": title,
    "contexts": ["all"],
    "id": "vh-right-click-save-article"
  });

  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === id) {
      saveCorpus()
    }
  });

}

initRightClickMenu()




chrome.runtime.onInstalled.addListener(function () {
  console.log('chrome.runtime.onInstalled')


  chrome.declarativeContent.onPageChanged.removeRules(undefined, function () {
    chrome.declarativeContent.onPageChanged.addRules([
      {
        conditions: [
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl: { hostContains: '.' }
          })
        ],
        actions: [
          new chrome.declarativeContent.ShowPageAction()
        ]
      }
    ])
  })
})
