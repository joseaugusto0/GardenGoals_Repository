import { DataSource } from "typeorm"


const AppDataSource = new DataSource({
    type: "postgres",
    url: process.env["DATABASE_URL"],
})

AppDataSource.initialize()
    .then(() => {
        console.log("Data Source has been initialized!")
    })
    .catch((err) => {
        console.error("Error during Data Source initialization", err)
    })

export default AppDataSource