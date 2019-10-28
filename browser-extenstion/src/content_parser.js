
//document.body

export function str2cmd(cmd) {
  function isAlpha(c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'C')
  }
  function findIndex(str, startIndex, cb) {
    for (let x = startIndex; x < str.length; x++) {
      let c = str.charAt(x);
      if (cb(c)) {
        return x
      }
    }
    return -1;
  }
  function _str2cmd(cmd, output) {
    if (cmd.length === 0) {
      return
    }
    if (cmd.startsWith(".")) {
      const fieldLastIndex = findIndex(cmd, 1, c => {
        return !isAlpha(c)
      })
      if (fieldLastIndex === -1) {
        output.push({ "type": "object", "field": cmd.slice(1) })
        return
      }
      output.push({ "type": "object", "field": cmd.slice(1, fieldLastIndex) })
      return _str2cmd(cmd.slice(fieldLastIndex), output)
    }
    if (cmd.startsWith("[")) {
      const fieldLastIndex = findIndex(cmd, 1, c => c === ']')
      if (fieldLastIndex === -1 && fieldLastIndex === 1) {
        throw new Error("syntax eror array index is not correct")
      }
      if (cmd[1] === '"') {
        output.push({ "type": "array", "index": cmd.slice(2, fieldLastIndex - 1) })
        return _str2cmd(cmd.slice(fieldLastIndex + 1), output)
      }
      output.push({ "type": "array", "index": cmd.slice(1, fieldLastIndex) })
      return _str2cmd(cmd.slice(fieldLastIndex + 1), output)
    }
  }

  const res = [];
  _str2cmd(cmd, res);
  return res
}

export function _access(data, cmd) {
  if (cmd.length == 0) {
    return data
  }
  if (cmd[0].type == "object") {
    return _access(data[cmd[0].field], cmd.slice(1))
  }
  if (cmd[0].type == "array") {
    return _access(data[cmd[0].index], cmd.slice(1))
  }
}

export function access(data, cmd) {
  return _access(data, str2cmd(cmd))
}

function parser(node) {
  if (node.nodeName === "#text") {
    return node.data
  }
  if (node.nodeName === "CODE") {
    return ""
  }

  let childTxt = "";
  for (let child of node.childNodes) {
    childTxt += parser(child)
  }
  if (node.nodeName === "P") {
    childTxt += '\n'
  }
  if (node.nodeName.startsWith("H")) {
    childTxt += '\n'
  }
  if (node.nodeName.startsWith("UL")) {
    childTxt += '\n'
  }
  if (node.nodeName.startsWith("LI")) {
    childTxt += '\n'
  }
  return childTxt;
}

export function parserArticle(document) {
  const title = document.querySelector("body > article > header > h1 > p").innerText;
  const content = parser(document.querySelector("body > article > .content"));
  return { title, content }
}
