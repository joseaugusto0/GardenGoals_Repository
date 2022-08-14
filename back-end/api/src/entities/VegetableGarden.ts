import { Column, CreateDateColumn, Entity, PrimaryColumn } from "typeorm";
import { v4 as uuid } from "uuid"

@Entity("vegetable_gardens")
export class User {
    @PrimaryColumn()
    id: string;

    @Column()
    garden_name: string;

    @Column()
    locality: string;

    @Column()
    light_time: number;

    @Column()
    wanted_cultures: string[];

    wanted_quantity: number;

    constructor(){
        if(!this.id){
            this.id = uuid()
        }
    }
}