const SERVER_URL = "http://localhost:10000"
class Api {
    async hunter(id, article) {
        return fetch(`${SERVER_URL}/hunter`, {
            method: "POST",
            headers: {
                id,
                'content-type': 'application/json'
            },
            body: JSON.stringify({ article })
        }).then(res => {
            return res.json()
        }).then(res => res.words)
    }

    async getExplain(id, words) {
        console.log("get explain", words);
        return fetch(`${SERVER_URL}/explain`, {
            method: "POST",
            headers: {
                id,
                'content-type': 'application/json'
            },
            body: JSON.stringify({ words })
        }).then(res => {
            return res.json()
        })
    }

    async markAsKnow(id, words) {
        return fetch(`${SERVER_URL}/mark/know`, {
            method: "POST",
            headers: {
                id,
                'content-type': 'application/json'
            },
            body: JSON.stringify({ words })
        })
    }

    async markAsUnKnow(id, words) {
        return fetch(`${SERVER_URL}/mark/unknow`, {
            method: "POST",
            headers: {
                id,
                'content-type': 'application/json'
            },
            body: JSON.stringify({ words })
        })

    }
}

export default Api;