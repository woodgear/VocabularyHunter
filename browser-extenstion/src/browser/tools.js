/*global chrome*/

async function setStorage(key, val) {
  return new Promise((res, rej) => {
    const obj = {};
    obj[key] = val;
    chrome.storage.sync.set(obj, data => {
      res(data);
    });
  });
}

async function getStorage(key) {
  return new Promise((res, rej) => {
    chrome.storage.sync.get(key, data => {
      res(data);
    });
  });
}

async function sendToContentScript(msg, timeout = 3) {
  const timeoutMills = timeout * 1000;
  return new Promise((res, rej) => {
    const timeoutHandle = setTimeout(() => {
      rej("time out");
    }, timeoutMills);
    try {
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, msg, function(response) {
          clearTimeout(timeoutHandle);
          console.log("get response", response);
          res(response);
        });
      });
    } catch (error) {
      clearTimeout(timeoutHandle);
      rej(error);
    }
  });
}

export default {
  getStorage,
  setStorage,
  sendToContentScript
};
