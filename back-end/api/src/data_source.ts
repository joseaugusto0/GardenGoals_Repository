import { DataSource } from "typeorm"
import { CreatePlantInfos1662069261633 } from "./database/migrations/1662069261633-CreatePlantInfos"
import { PlantInfos } from "./entities/PlantInfos"


const AppDataSource = new DataSource({
    type: "postgres",
    url: process.env["DATABASE_URL"],
    migrations: [CreatePlantInfos1662069261633],
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