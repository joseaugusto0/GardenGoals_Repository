import { Column, CreateDateColumn, Entity, PrimaryColumn } from "typeorm";
import { v4 as uuid } from "uuid"

@Entity("vegetable_gardens")
export class User {
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