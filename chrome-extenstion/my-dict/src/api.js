const SERVER_URL = "http://localhost:5000"
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
        console.log("not yet")
    }

    async markAsUnKnow(id, words) {
        console.log("not yet")
    }
}

export default Api;