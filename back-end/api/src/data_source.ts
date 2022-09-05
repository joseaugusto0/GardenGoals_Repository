import { DataSource } from "typeorm"


const AppDataSource = new DataSource({
    type: "postgres",
    url: process.env.DATABASE_URL,
    
    port: parseInt(process.env.PGPORT),
    username: process.env.PGUSER,
    password: process.env.PGPASSWORD,
    database: process.env.PGDATABASE,
    entities: ["dist/entities/*.js"],
    migrations: ["dist/database/migrations/*.js"],
})

AppDataSource.initialize()
    .then(() => {
        console.log("Data Source has been initialized!")
    })
    .catch((err) => {
        console.error("Error during Data Source initialization", err)
    })

export default AppDataSource