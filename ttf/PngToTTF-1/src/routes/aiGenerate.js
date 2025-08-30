import { Router } from "express";
import { aiGenerateHandler } from "../controllers/aiGenerateController.js";
import upload from "../middlewares/upload.js";

const router = Router();
router.post("/", upload.uploadSingle, aiGenerateHandler);

export default router;
