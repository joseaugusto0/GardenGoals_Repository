import axios from "axios";


export const api = axios.create({
    baseURL: "http://154.780.1.3:3333"
})