import { Column, CreateDateColumn, Entity, PrimaryColumn } from "typeorm";
import { v4 as uuid } from "uuid"

@Entity("plant_infos")
export class PlantInfos {
    @PrimaryColumn()
    id: string;

    @Column()
    name: string;

    @Column()
    space_between_lines: number;

    @Column()
    space_between_plants: number;

    constructor(){
        if(!this.id){
            this.id = uuid()
        }
    }
}