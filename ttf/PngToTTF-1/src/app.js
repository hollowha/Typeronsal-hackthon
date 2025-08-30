import express from "express";
import cors from "cors";
import path from "path";

import upload from "./middlewares/upload.js";
import convertRouter from "./routes/convert.js";
import aiGenerateRouter from "./routes/aiGenerate.js";

const app = express();

// CORS 配置
app.use(
  cors({
    origin: "*",
    methods: ["GET", "POST"],
    allowedHeaders: ["Content-Type"],
  })
);

// 提供靜態文件服務
app.use(express.static("public"));

// 路由配置
app.use("/convert", convertRouter);
app.use("/ai-generate", aiGenerateRouter);

export default app;
