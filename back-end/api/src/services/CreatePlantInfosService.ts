import  AppDataSource  from "../../data_source"
import { PlantInfos } from "../entities/PlantInfos"

interface IPlantInfosRequest {
    name: string
    space_between_lines: number,
    space_between_plants: number,
}

class CreatePlantInfoService {

    async execute({name, space_between_lines, space_between_plants}:IPlantInfosRequest) {

        if ((!name) || (!space_between_lines) || (!space_between_plants)){
            throw new Error("Fill all infos")
        }

        const plantInfosRepository = AppDataSource.getRepository(PlantInfos)
        const plantInfoExists = await plantInfosRepository.findOneBy({
            name
        })

        if(plantInfoExists){
            throw new Error("Plant already exists")
        }

        const new_plant = plantInfosRepository.create({
            name, 
            space_between_lines,
            space_between_plants
        })

        plantInfosRepository.save(new_plant)

        return new_plant
    }
}