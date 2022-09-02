import { Router } from "express"
import { CreatePlantInfosController } from "./controller/CreatePlantsInfosController";
import { RunSolverController } from "./controller/RunSolverController";


const router = Router();
const createUserController = new CreatePlantInfosController();
const runSolverController = new RunSolverController()

router.post("/plant_infos", createUserController.handle)
router.post("/run_solver", runSolverController.handle)
router.get("/test", (request, response) => {
    return response.send("Olá NLW")
})
export {router};