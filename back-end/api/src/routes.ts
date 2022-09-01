import { Router } from "express"
import { CreatePlantInfosController } from "./controller/CreatePlantsInfosController";


const router = Router();
const createUserController = new CreatePlantInfosController();

router.post("/plant_infos", createUserController.handle)
router.get("/test", (request, response) => {
    return response.send("Olá NLW")
})
export {router};