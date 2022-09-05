import "reflect-metadata"
import express from "express";
import {router} from "./routes"


const app = express()
var cors = require('cors')
app.use(express.json())
app.use(cors())
app.use(router)
app.get("/test", (request, response) => {
    return response.send("Olá NLW")
})
app.listen(process.env.PORT || 3333, () => console.log("Server is running"))