import { DataSource } from "typeorm"

const AppDataSource = new DataSource({
    type: "sqlite",
    database: "./src/database/users.sqlite",
    entities: ['./src/entities/*.ts'],
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