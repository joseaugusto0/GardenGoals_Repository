import {EntityRepository, Repository} from "typeorm";
import { PlantInfos } from "../entities/PlantInfos"

    @EntityRepository(PlantInfos)
    @EntityRepository(PlantInfos)
    class PlantInfosRepositories extends Repository<PlantInfos>{}
        // O extend é para conseguirmos pegar todas as funções da classe repository, provida pela typeorm, que contém funções como salvar novos dados na tabela, excluir, etc.

    export { PlantInfosRepositories };