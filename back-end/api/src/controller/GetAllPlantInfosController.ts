import {Request, Response} from 'express'
import { GetPlantInfosService } from '../services/GetPlantInfosService'

class GetAllPlantInfosController{

    async handle(request: Request, response: Response){
        try{

            const names = request.body

            const getPlantInfosService = new GetPlantInfosService()
            const plantInfo = await getPlantInfosService.execute(names)

            
            return response.status(200).json(plantInfo)

        }catch(err){
            return response.status(400).json({error: err.message})
        }
    }
}

export { GetAllPlantInfosController }