import express from 'express'
import { AppDataSource } from '../data-source'

const app = express()

app.get('/users', (req, res) => {
    //Inserir a função aqui
    return res.send("hello World")
})

app.listen(3333, () => {
    console.log('HTTP Server Running')
})