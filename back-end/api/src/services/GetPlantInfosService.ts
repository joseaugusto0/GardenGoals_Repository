import AppDataSource from "../../data_source"
import { PlantInfos } from "../entities/PlantInfos"

class GetPlantInfosService{

    async execute(name: null| string){
        
        const plantInfosRepository = AppDataSource.getRepository(PlantInfos)
        console.log(name)
        if (Object.keys(name).length==0){
            
            let queryGetAllPlantInfos = plantInfosRepository.createQueryBuilder('plant_infos').select("*")
            const values = await queryGetAllPlantInfos.getRawMany();
            return values

        }else{
            
            const value = await plantInfosRepository.findOneBy({name})
            return value
        }
               
    }

}

export {GetPlantInfosService}