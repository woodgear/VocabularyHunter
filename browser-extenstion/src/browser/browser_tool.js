/* global chrome */

/* eslint prefer-promise-reject-errors: "off" */
export async function setStorage (key, val) {
  return new Promise((res, rej) => {
    const obj = {}
    obj[key] = val
    chrome.storage.local.set(obj, () => {
      console.log('Value is set to ' + JSON.stringify(obj))
      res()
    })
  })
}

export async function getStorage (key) {
  return new Promise((res, rej) => {
    chrome.storage.local.get([key], (result) => {
      console.log('getStorage', result[key])
      res(result[key])
    })
  })
}

export async function sendToContentScript (msg, timeout = 3) {
  const timeoutMills = timeout * 1000
  return new Promise((res, rej) => {
    const timeoutHandle = setTimeout(() => {
      rej('time out')
    }, timeoutMills)
    try {
      console.log("start try send");
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        console.log("find tab");
        chrome.tabs.sendMessage(tabs[0].id, msg, function (response) {
          console.log("rece response",response)
          clearTimeout(timeoutHandle)
          res(response)
        })
      })
    } catch (error) {
      clearTimeout(timeoutHandle)
      rej(error)
    }
  })
}

export async function getDevConfig () {
  try {
    const url = chrome.runtime.getURL('extenstion_config/config.json')
    const res = await fetch(url)
    return res.json()
  } catch (error) {
    return {}
  }
}
