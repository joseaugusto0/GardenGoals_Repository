import { MigrationInterface, QueryRunner, Table } from "typeorm"

export class CreatePlantInfos1662069261633 implements MigrationInterface {

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.createTable(
            
            new Table({
                name: "plant_infos",
                columns:[
                    {
                        name: 'id',
                        type: "uuid",
                        isPrimary: true
                    },
                    {
                        name: 'name',
                        type: "varchar",
                    },
                    {
                        name: "space_between_lines",
                        type: "int"
                    },
                    {
                        name: "space_between_plants",
                        type: "int"
                    }
                ]
            })
        )
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.dropTable("plant_infos")
    }

}
