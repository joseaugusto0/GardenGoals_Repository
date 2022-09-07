import { DataSource } from "typeorm"

var data = null
if (process.env.DEV){
    data = {
        type : "sqlite",
        database: './src/database/db.sqlite',
        entities: ["./src/entities/*.ts"],
        migrations: ["./src/database/migrations/*.ts"],
    }
}else{
    data = {
        type: "postgres",
        url: process.env.DATABASE_URL,
        
        port: parseInt(process.env.PGPORT),
        username: process.env.PGUSER,
        password: process.env.PGPASSWORD,
        database: process.env.PGDATABASE,
        entities: ["dist/entities/*.js"],
        migrations: ["dist/database/migrations/*.js"],
    }
}

const AppDataSource = new DataSource(data)

AppDataSource.initialize()
    .then(() => {
        console.log("Data Source has been initialized!")
    })
    .catch((err) => {
        console.error("Error during Data Source initialization", err)
    })

export default AppDataSource