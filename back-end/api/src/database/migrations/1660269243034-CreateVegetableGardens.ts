import { MigrationInterface, QueryRunner, Table } from "typeorm"

export class CreateVegetableGardens1660269243034 implements MigrationInterface {

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.createTable(
            
            new Table({
                name: "vegetable_gardens",
                columns:[
                    {
                        name: 'id',
                        type: "uuid",
                        isPrimary: true
                    },
                    {
                        name: 'garden_name',
                        type: "varchar",
                    },
                    {
                        name: 'locality',
                        type: "varchar",
                    },
                    {
                        name: "light_time",
                        type: "real"
                    },
                    {
                        name: "wanted_cultures",
                        type: "blob"
                    },
                    {
                        name: "wanted_quantity",
                        type: "int"
                    },
                    {
                        name: "user_id",
                        type: "uuid"
                    }
                ],
                foreignKeys: [
                    {
                        name: "fk_vegetable_gardens",
                        columnNames: ["user_id"],
                        referencedTableName: "users",
                        referencedColumnNames: ["id"]
                    }
                ]
            })
        )
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.dropTable("vegetable_gardens")
    }


}
