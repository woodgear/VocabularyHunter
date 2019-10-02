class Api {
    constructor(id, vhServer) {
        this.id = id;
        this.vhServer = vhServer;
    }

    async hunter(article) {
        return fetch(`${this.vhServer}/hunter`, {
            method: "POST",
            headers: {
                id:this.id,
                'content-type': 'application/json'
            },
            body: JSON.stringify({ article })
        }).then(res => {
            return res.json()
        }).then(res => res.words)
    }

    async getExplain(words) {
        console.log("get explain", words);
        return fetch(`${this.vhServer}/explain`, {
            method: "POST",
            headers: {
                id:this.id,
                'content-type': 'application/json'
            },
            body: JSON.stringify({ words })
        }).then(res => {
            return res.json()
        })
    }

    async markAsKnow(words) {
        return fetch(`${this.vhServer}/mark/know`, {
            method: "POST",
            headers: {
                id:this.id,
                'content-type': 'application/json'
            },
            body: JSON.stringify({ words })
        })
    }

    async markAsUnKnow(words) {
        return fetch(`${this.vhServer}/mark/unknow`, {
            method: "POST",
            headers: {
                id:this.id,
                'content-type': 'application/json'
            },
            body: JSON.stringify({ words })
        })

    }
}

export default Api;