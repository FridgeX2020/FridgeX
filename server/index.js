const express = require('express')
const cors = require('cors')
const path = require('path');
const app = express()
const fs = require("fs")
const port = 3000

app.use(cors())

app.get('/', (req, res) => {
        let file = path.join(__dirname, 'data/storage.json');
        let json = require(file)

        res.json(json)
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
