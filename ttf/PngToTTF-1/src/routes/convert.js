import { Router } from "express";
import { convertHandler } from "../controllers/convertController.js";
import upload from "../middlewares/upload.js";

const router = Router();
router.post("/", upload.uploadArray, convertHandler);

export default router;
