import { Column, CreateDateColumn, Entity, PrimaryColumn } from "typeorm";
import { v4 as uuid } from "uuid"

@Entity("users")
export class User {
    @PrimaryColumn()
    id: string;

    @Column()
    login: string;

    @Column()
    password: string;

    @CreateDateColumn()
    created_at: Date;

    constructor(){
        if(!this.id){
            this.id = uuid()
        }
    }
}