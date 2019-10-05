import zlib from 'zlib'

function gzip (body) {
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
  constructor (id, vhServer) {
    this.id = id
    this.vhServer = vhServer
  }

  async hunter (article) {
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

  async getExplain (words) {
    console.log('get explain', words)
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

  async markAsKnow (words) {
    return fetch(`${this.vhServer}/api/vh/mark/know`, {
      method: 'POST',
      headers: {
        id: this.id,
        'content-type': 'application/json'
      },
      body: JSON.stringify({ words })
    })
  }

  async markAsUnKnow (words) {
    return fetch(`${this.vhServer}/api/vh/mark/unknow`, {
      method: 'POST',
      headers: {
        id: this.id,
        'content-type': 'application/json'
      },
      body: JSON.stringify({ words })
    })
  }
}

export default Api
