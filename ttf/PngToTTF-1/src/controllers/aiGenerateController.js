import { execSync } from "child_process";
import fs from "fs";
import path from "path";
import fetch from "node-fetch";
import FormData from "form-data";
import { v4 as uuidv4 } from "uuid";

const API_BASE_URL = "https://typersonal.dy6.click/8000";
const COMMON_CHARS = "的一是不了人我在有他這為之大來以個中上們到說國和地也子時道出而要於就下得可你年生自會那後能對著事其裡所去行過家十天為麼起還方沒想看得起把工對開而已些現山民候經發工向事命給長水幾義三同麼度門起動根力自物世品加沒北什造百規熱領七海口東導器壓志世金增爭濟階油思術極交受聯什認六共權收證改清己必美再採轉更單風切打白教速花帶安場身車例真務具萬每目至達走積示議聲報鬥完類八離華名確才科張信馬節話米整空元今集溫傳土許步群廣石記需段研界拉林律叫且究觀越織裝影算低持音眾書布复容兒須際商非驗連斷深難近礦千周委素技備半辦青省列習響約支般史感勞便團往酸歷市克何除消構府稱太準精值號率族維劃選標寫存候毛親快效斯院查江型眼王按格養易置派層片始卻專狀育廠京識適屬圓包火住調滿縣局照參紅細引聽該鐵價嚴龍飛";

// 創建臨時存儲目錄
const TEMP_DIR = path.resolve(process.cwd(), "temp");
const SCRIPTS_DIR = path.resolve(process.cwd(), "scripts");

if (!fs.existsSync(TEMP_DIR)) {
  fs.mkdirSync(TEMP_DIR);
}

async function generateSingleCharacter(char, referenceImagePath, outputPath, maxRetries = 3, delayMs = 3000) {
  let retries = maxRetries;
  let lastError;

  while (retries > 0) {
    try {
      // Wait before making request to prevent rate limiting
      await new Promise(resolve => setTimeout(resolve, delayMs));

      // Create a new FormData instance for each request
      const form = new FormData();
      form.append('character', char);
      form.append('sampling_step', '20');
      
      // Create a new read stream for each request
      const imageStream = fs.createReadStream(referenceImagePath);
      form.append('reference_image', imageStream, {
        filename: 'reference.png',
        contentType: 'image/png'
      });

      console.log(`Generating character: ${char}`);
      console.log(`Using reference image: ${referenceImagePath}`);
      
      const response = await fetch(`${API_BASE_URL}/ai/generate`, {
        method: "POST",
        body: form,
        timeout: 30000 // 30 second timeout
      });

      const responseText = await response.text();
      console.log("API Response:", responseText); // Add this for debugging

      if (!response.ok) {
        throw new Error(`API returned error (${response.status}): ${responseText}`);
      }

      let data;
      try {
        data = JSON.parse(responseText);
      } catch (e) {
        console.error('Failed to parse response:', responseText);
        throw new Error('Invalid response format from API');
      }

      if (!data.image) {
        throw new Error('No image URL in response');
      }

      console.log(`Downloading generated image from: ${data.image}`);

      // Download the generated image
      const imageResponse = await fetch(data.image);
      if (!imageResponse.ok) {
        throw new Error(`Failed to download generated image: ${imageResponse.statusText}`);
      }

      const generatedBuffer = await imageResponse.buffer();
      
      // Verify the buffer is valid
      if (!generatedBuffer || generatedBuffer.length === 0) {
        throw new Error("Generated image buffer is empty");
      }

      // Create a unique filename for each character
      const codePoint = char.codePointAt(0).toString(16).padStart(4, '0');
      const uniqueFilename = `u+${codePoint}.png`;
      const outputFilePath = path.join(path.dirname(outputPath), uniqueFilename);

      // Save the image
      fs.writeFileSync(outputFilePath, generatedBuffer);

      // Verify the file was written successfully
      if (!fs.existsSync(outputFilePath)) {
        throw new Error("Failed to save generated image");
      }

      console.log(`Successfully generated and saved character: ${char} to ${outputFilePath}`);
      return outputFilePath;

    } catch (err) {
      lastError = err;
      retries--;
      console.log(`Failed to generate ${char}, retries left: ${retries}. Error: ${err.message}`);
      
      if (retries > 0) {
        // Increase delay between retries
        await new Promise(resolve => setTimeout(resolve, delayMs * 2));
      }
    }
  }

  throw new Error(`Failed to generate character ${char} after ${maxRetries} attempts. Last error: ${lastError.message}`);
}

export async function aiGenerateHandler(req, res) {
  if (!req.file) {
    return res.status(400).json({ error: "請上傳參考字型圖片" });
  }

  const sessionId = uuidv4();
  const sessionDir = path.join(TEMP_DIR, sessionId);
  const workspaceDir = path.join(sessionDir, "workspace");
  let cleanupDone = false;

  try {
    // Create directory structure
    fs.mkdirSync(sessionDir);
    fs.mkdirSync(workspaceDir);
    fs.mkdirSync(path.join(workspaceDir, "final_font"));
    fs.mkdirSync(path.join(workspaceDir, "svg_separate"));
    fs.mkdirSync(path.join(workspaceDir, "pico"));
    fs.mkdirSync(path.join(workspaceDir, "sourcePNG"));

    // Save reference image
    const referenceImagePath = path.join(sessionDir, "reference.png");
    fs.copyFileSync(req.file.path, referenceImagePath);

    // Verify the reference image
    if (!fs.existsSync(referenceImagePath)) {
      throw new Error("Failed to save reference image");
    }

    const referenceStats = fs.statSync(referenceImagePath);
    if (referenceStats.size === 0) {
      throw new Error("Reference image is empty");
    }

    // Generate all characters
    console.log("Starting character generation...");
    const generatedImages = [];
    const sourcePNGDir = path.join(workspaceDir, "sourcePNG");

    // Take first character for testing
    const testChars = [COMMON_CHARS[0]]; // Just test with first character "的"
    for (const char of testChars) {
      const baseImagePath = path.join(sourcePNGDir, "temp.png");
      const finalPath = await generateSingleCharacter(char, referenceImagePath, baseImagePath);
      if (finalPath) {
        generatedImages.push(finalPath);
      }
    }

    if (generatedImages.length === 0) {
      throw new Error("No characters were successfully generated");
    }

    // Convert to font
    const originalCwd = process.cwd();
    try {
      process.chdir(workspaceDir);

      // Execute conversion scripts
      const scripts = [
        "potrace.js",
        "run_pico.js",
        "merge.js",
        "readfile.js",
        "generate-font.js"
      ];

      for (const script of scripts) {
        console.log(`Executing ${script}...`);
        execSync(`node "${path.join(SCRIPTS_DIR, script)}"`, {
          stdio: "inherit",
          env: {
            ...process.env,
            WORKSPACE_DIR: workspaceDir,
          },
        });
      }
    } finally {
      process.chdir(originalCwd);
    }

    // Verify and send font file
    const fontPath = path.join(workspaceDir, "final_font", "fontpico.ttf");
    if (!fs.existsSync(fontPath)) {
      throw new Error("Font file generation failed");
    }

    const fontStats = fs.statSync(fontPath);
    if (fontStats.size === 0) {
      throw new Error("Generated font file is empty");
    }

    res.download(fontPath, "generated-font.ttf", (err) => {
      if (err) {
        console.error("Download failed:", err);
      }
      
      if (!cleanupDone) {
        cleanupDone = true;
        // Clean up temporary files
        try {
          fs.rmSync(sessionDir, { recursive: true, force: true });
        } catch (cleanErr) {
          console.error("Cleanup failed:", cleanErr);
        }
      }
    });

  } catch (error) {
    if (!cleanupDone) {
      cleanupDone = true;
      try {
        fs.rmSync(sessionDir, { recursive: true, force: true });
      } catch (cleanErr) {
        console.error("Cleanup failed:", cleanErr);
      }
    }
    console.error("Processing failed:", error);
    res.status(500).json({ error: error.message || "Font generation failed" });
  }
}
