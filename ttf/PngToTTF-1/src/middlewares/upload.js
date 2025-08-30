import multer from "multer";
import path from "path";

const MAX_FILES = 5000;
const WORKSPACE = path.resolve(process.cwd(), "workspace");
const SRC_DIR = path.join(WORKSPACE, "sourcePNG");

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, SRC_DIR);
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const fileFilter = (req, file, cb) => {
  if (file.mimetype === "image/png") {
    cb(null, true);
  } else {
    cb(new Error("只接受 PNG 格式"), false);
  }
};

const multerUpload = multer({
  storage,
  fileFilter,
  limits: { files: MAX_FILES },
});

// 多檔案上傳
export const uploadArray = multerUpload.array("files", MAX_FILES);

// 單一檔案上傳
export const uploadSingle = multerUpload.single("reference_image");

export default { uploadArray, uploadSingle };
