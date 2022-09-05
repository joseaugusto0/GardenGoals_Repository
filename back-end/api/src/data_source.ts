import { DataSource } from "typeorm"


const AppDataSource = new DataSource({
    type: "postgres",
    url: process.env["DATABASE_URL"],
    migrations: ['./src/database/migrations/*.ts'],
})

AppDataSource.initialize()
    .then(() => {
        console.log("Data Source has been initialized!")
    })
    .catch((err) => {
        console.error("Error during Data Source initialization", err)
    })

export default AppDataSource