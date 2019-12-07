import zlib from 'zlib'

function gzip(body) {
  return new Promise(function (resolve, reject) {
    zlib.gzip(body, (err, buffer) => {
      if (err) {
        reject(err)
      }
      resolve(buffer)
    })
  })
}

class Api {
  constructor(id, vhServer) {
    this.id = id
    this.vhServer = vhServer
  }

  async hunter(article) {
    const url = `${this.vhServer}/api/vh/hunter`
    const body = JSON.stringify({ article })
    const zipBody = await gzip(body)
    console.log('start hunter', body.length, zipBody.length)
    return fetch(url, {
      method: 'POST',
      headers: {
        id: this.id,
        'content-type': 'application/json',
        'content-encoding': 'gzip'
      },
      body: zipBody
    }).then(res => {
      console.log('get  hunter response')
      return res.json()
    }).then(res => res.words)
  }

  async export() {
    return fetch(`${this.vhServer}/api/vh/export/all`, {
      method: 'POST',
      headers: {
        id: this.id,
        'content-type': 'application/json',
        'content-encoding': 'gzip'
      }
    }).then(res => {
      return res.json()
    })
  }

  async import(words) {
    return fetch(`${this.vhServer}/api/vh/import/all`, {
      method: 'POST',
      headers: {
        id: this.id,
        'content-type': 'application/json',
        'content-encoding': 'gzip'
      },
      body: await gzip(JSON.stringify({ words }))
    })
  }

  async getExplain(words) {
    return fetch(`${this.vhServer}/api/vh/explain`, {
      method: 'POST',
      headers: {
        id: this.id,
        'content-type': 'application/json',
        'content-encoding': 'gzip'
      },
      body: await gzip(JSON.stringify({ words }))
    }).then(res => {
      return res.json()
    })
  }

  async markAsKnow(words) {
    return fetch(`${this.vhServer}/api/vh/mark/know`, {
      method: 'POST',
      headers: {
        id: this.id,
        'content-type': 'application/json'
      },
      body: JSON.stringify({ words })
    })
  }

  async markAsUnKnow(words) {
    return fetch(`${this.vhServer}/api/vh/mark/unknow`, {
      method: 'POST',
      headers: {
        id: this.id,
        'content-type': 'application/json'
      },
      body: JSON.stringify({ words })
    })
  }

  async saveCorpus(article, title, url) {
    return fetch(`${this.vhServer}/api/vh/corpus`, {
      method: 'POST',
      headers: {
        id: this.id,
        'content-type': 'application/json'
      },
      body: JSON.stringify({ article, title, url })
    })
  }
}

export default Api
