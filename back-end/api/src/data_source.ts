import { DataSource } from "typeorm"
import { PlantInfos } from "./entities/PlantInfos"


const AppDataSource = new DataSource({
    type: "postgres",
    url: process.env["DATABASE_URL"],
    port: parseInt(process.env["PGPORT"]),
    username: process.env["PGUSER"],
    password: process.env["PGPASSWORD"],
    database: process.env["PGDATABASE"],
    entities: [PlantInfos]
})

AppDataSource.initialize()
    .then(() => {
        console.log("Data Source has been initialized!")
    })
    .catch((err) => {
        console.error("Error during Data Source initialization", err)
    })

export default AppDataSource