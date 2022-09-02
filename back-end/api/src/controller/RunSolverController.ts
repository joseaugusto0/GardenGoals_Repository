import { Request, Response } from "express"
import {PythonShell} from "python-shell"


class RunSolverController{
    async handle(request: Request, response: Response){


        if (Object.keys(request.body).length==0){
            response.statusMessage = "Any parameters has been passed"
            response.status(400).end()
            return
        }

        const py_options = PythonShell.defaultOptions = {
            mode: 'text',
            pythonPath: '../python/venv/Scripts/python.exe',
            pythonOptions: ['-u'], // get print results in real-time
            scriptPath: '../python/optimizer_app/src',
            args: [JSON.stringify(request.body)]
        }
        console.log("Running solver")

        PythonShell.run("main.py", py_options, await function(err, results){
            if (err){
                response.status(400).send(err)
            }
            console.log(results)
            var finalResult = results.join().split("finalResult: ")
            console.log(finalResult[1])
            
        })


        response.send("Runned")
    }
}

export {RunSolverController}