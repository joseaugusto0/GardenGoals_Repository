# Estrutura do Database
Para que possar ser feito um banco de dados conciso, foi feito a seguinte estruturação do mesmo:

## Estrutura da tabela de usuários
-   ID (Primary key)
-   Nome (varchar)
-   Email (varchar)
-   Senha (varchar)
-   Admin (boolean)
-   criado_em (date)
-   atualizado_em (date)

## Criando migration no typeorm -.3
data-source.ts na raíz da aplicação -> ./data-source.ts
```ts
    import {DataSource} from 'typeorm'

export const AppDataSource = new DataSource({
    type: "sqlite",
    database: "./src/database/database.sqlite",
    synchronize: true,
    logging: true,
    subscribers: [],
    migrations: [],
})
```
-   Adicionando o script typeorm no package.json
```json
    "scripts": {
        "dev": "ts-node-dev src/server.ts",
        "typeorm": "typeorm-ts-node-commonjs -d data-source.ts"
    },
```

-   Rodando as migrations
```
    npx typeorm migration:create ./src/database/migrations/CreateUsers
``` 