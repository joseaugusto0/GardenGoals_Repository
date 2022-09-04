import AppDataSource from "../../data_source"
import { PlantInfos } from "../entities/PlantInfos"


interface iPlantInfoRequest{
    names: null | string[]
}

class GetPlantInfosService{

    async execute(names: iPlantInfoRequest){
        
        const plantInfosRepository = AppDataSource.getRepository(PlantInfos)
        var values;
        console.log(names)
        if (Object.keys(names).length==0){
            
            let queryGetAllPlantInfos = plantInfosRepository.createQueryBuilder('plant_infos').select("*")
            values = await queryGetAllPlantInfos.getRawMany();

        }else{
            
            async function get_info_by_name(name, _){
                const plantInfo = await plantInfosRepository.findOneBy({name})
                return plantInfo
            }

            values = await Promise.all(names['plant'].map(get_info_by_name))

        }
        
        return values        
    }
}

export {GetPlantInfosService}