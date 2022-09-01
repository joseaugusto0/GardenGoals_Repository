import { Request, Response } from "express"
import CreatePlantInfosService from "../services/CreatePlantInfosService";

class PlantInfosController{
    async handle(request:Request, response: Response) {
        const {name, space_between_lines, space_between_plants} = request.body;

        const createPlantInfoService = new CreatePlantInfosService()

        const new_plant_infos = await createPlantInfoService.execute({name, space_between_lines, space_between_plants})
    
        return response.json(new_plant_infos)
    }

}

export default {CreatePlantInfosService}