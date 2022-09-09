import { Request, Response } from "express"
import {PythonShell} from "python-shell"
import { GetPlantInfosService } from "../services/GetPlantInfosService"

interface iRunSolverRequest{
    polygon: string,
    coordenates: [number[]],
    width: number,
    height: number
    selectedPlants: string
}

class RunSolverController{
    async handle(request: Request, response: Response){
        try{
            if (Object.keys(request.body).length==0){
                response.statusMessage = "Any parameters has been passed"
                response.status(400).end()
                return
            }

            const data: iRunSolverRequest = request.body           

            const getPlantInfosService = new GetPlantInfosService()              
            
            const plantInfos = await Promise.all(Object.values(data.selectedPlants).map(
                async function (plantName) {
                    if (plantName != "") {
                        const value = await getPlantInfosService.execute(plantName)
                        
                        return value
                    }
                    return null
                }
            ))

            console.log({...data,plantInfos})
            const py_options = PythonShell.defaultOptions = {
                mode: 'text',
                pythonPath: '../python/optimizer_app/venv/Scripts/python.exe',
                pythonOptions: ['-u'], // get print results in real-time
                scriptPath: '../python/optimizer_app/src',
                args: [JSON.stringify({...data,plantInfos})]
            }

            console.log("Running solver")

            PythonShell.run("main.py", py_options, await function(err, results){
                if (err){
                    console.log(err)
                    response.status(400).send(err)
                    return
                }
                console.log(results)
                var finalResult = results.join().split("finalResult: ")
                
                response.send(finalResult[1])
            })
            return response.status(200).json
        }catch(err){
            return response.status(400).json({error: err.message})
        }
        
        
        
        
    }
}

export {RunSolverController}