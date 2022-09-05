import { Router, Request, Response } from "express"
import { CreatePlantInfosController } from "./controller/CreatePlantsInfosController";
import { GetAllPlantInfosController } from "./controller/GetAllPlantInfosController";
import { RunSolverController } from "./controller/RunSolverController";


const router = Router();
const createPlantInfoController = new CreatePlantInfosController();
const runSolverController = new RunSolverController();
const getAllPlantInfosController =  new GetAllPlantInfosController();

router.get("/", (request: Request, response: Response) => {
    response.status(200).send("Foi")
})
router.post("/plant_infos", createPlantInfoController.handle)
router.post("/run_solver", runSolverController.handle)
router.post("/get_plant_infos", getAllPlantInfosController.handle)
export {router};