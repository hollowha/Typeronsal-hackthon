"""
SLM NPU 字型生成器
使用Snapdragon NPU (QNN) 進行高效字型生成
"""

import onnxruntime as ort
import numpy as np
import time
from PIL import Image
import cv2
import os
from typing import Optional, Dict, Any, Tuple
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SLMFontGenerator:
    """SLM NPU 字型生成器"""
    
    def __init__(self, model_path: str = None, use_npu: bool = True):
        """
        初始化SLM字型生成器
        
        Args:
            model_path: ONNX模型路徑
            use_npu: 是否使用NPU (HTP後端)
        """
        self.model_path = model_path or "./models/slm_font_model.onnx"
        self.use_npu = use_npu
        self.session = None
        self.input_name = None
        self.output_name = None
        self.input_shape = None
        
        # 初始化模型
        self._initialize_model()
    
    def _initialize_model(self):
        """初始化ONNX模型和執行會話"""
        try:
            if not os.path.exists(self.model_path):
                logger.warning(f"模型文件不存在: {self.model_path}")
                logger.info("將使用模擬模式進行測試")
                self._setup_mock_session()
                return
            
            # 設置執行提供者選項
            if self.use_npu:
                execution_provider_option = {
                    "backend_path": "QnnHtp.dll",
                    "enable_htp_fp16_precision": "1",
                    "htp_performance_mode": "high_performance"
                }
                providers = ["QNNExecutionProvider"]
                provider_options = [execution_provider_option]
            else:
                providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
                provider_options = []
            
            # 創建ONNX Runtime會話
            self.session = ort.InferenceSession(
                self.model_path,
                providers=providers,
                provider_options=provider_options
            )
            
            # 獲取輸入輸出信息
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name
            self.input_shape = self.session.get_inputs()[0].shape
            
            logger.info(f"模型初始化成功")
            logger.info(f"輸入名稱: {self.input_name}")
            logger.info(f"輸出名稱: {self.output_name}")
            logger.info(f"輸入形狀: {self.input_shape}")
            logger.info(f"執行提供者: {self.session.get_providers()}")
            
        except Exception as e:
            logger.error(f"模型初始化失敗: {e}")
            logger.info("切換到模擬模式")
            self._setup_mock_session()
    
    def _setup_mock_session(self):
        """設置模擬會話用於測試"""
        self.session = None
        self.input_name = "mock_input"
        self.output_name = "mock_output"
        self.input_shape = [1, 3, 64, 64]
        logger.info("已設置模擬模式")
    
    def preprocess_image(self, image: Image.Image, target_size: Tuple[int, int] = (64, 64)) -> np.ndarray:
        """
        預處理輸入圖片
        
        Args:
            image: PIL圖片
            target_size: 目標尺寸
            
        Returns:
            預處理後的numpy數組
        """
        # 轉換為RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 調整尺寸
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        
        # 轉換為numpy數組並正規化
        img_array = np.array(image).astype(np.float32) / 255.0
        
        # 調整維度: (H, W, C) -> (1, C, H, W)
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def postprocess_output(self, output: np.ndarray) -> Image.Image:
        """
        後處理模型輸出
        
        Args:
            output: 模型輸出
            
        Returns:
            處理後的PIL圖片
        """
        # 確保輸出是正確的形狀
        if len(output.shape) == 4:
            output = output[0]  # 移除batch維度
        
        # 轉換維度: (C, H, W) -> (H, W, C)
        output = np.transpose(output, (1, 2, 0))
        
        # 正規化到0-255範圍
        output = np.clip(output, 0, 1) * 255
        output = output.astype(np.uint8)
        
        return Image.fromarray(output)
    
    def generate_font(self, 
                      character: str, 
                      reference_image: Image.Image,
                      sampling_steps: int = 20,
                      style_strength: float = 0.8) -> Optional[Image.Image]:
        """
        生成字型圖片
        
        Args:
            character: 要生成的字元
            reference_image: 參考風格圖片
            sampling_steps: 採樣步數
            style_strength: 風格強度 (0.0-1.0)
            
        Returns:
            生成的字型圖片或None
        """
        try:
            start_time = time.time()
            
            # 檢查模型是否可用
            if self.session is None:
                logger.warning("模型未初始化，使用模擬生成")
                return self._mock_generate_font(character, reference_image)
            
            # 預處理輸入圖片
            input_data = self.preprocess_image(reference_image)
            
            # 準備輸入數據
            inputs = {self.input_name: input_data}
            
            # 執行推理
            logger.info(f"開始生成字型: {character}")
            outputs = self.session.run([self.output_name], inputs)
            
            # 後處理輸出
            result_image = self.postprocess_output(outputs[0])
            
            # 計算執行時間
            execution_time = (time.time() - start_time) * 1000
            logger.info(f"字型生成完成: {character}, 耗時: {execution_time:.2f}ms")
            
            return result_image
            
        except Exception as e:
            logger.error(f"字型生成失敗: {e}")
            return None
    
    def _mock_generate_font(self, character: str, reference_image: Image.Image) -> Image.Image:
        """模擬字型生成（用於測試）"""
        logger.info(f"模擬生成字型: {character}")
        
        # 創建一個簡單的模擬字型圖片
        img_size = (64, 64)
        img_array = np.ones((*img_size, 3), dtype=np.uint8) * 255
        
        # 添加一些簡單的圖案來模擬字型
        cv2.rectangle(img_array, (10, 10), (54, 54), (100, 100, 100), 2)
        cv2.putText(img_array, character, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)
        
        return Image.fromarray(img_array)
    
    def batch_generate_fonts(self, 
                            characters: list, 
                            reference_image: Image.Image,
                            **kwargs) -> Dict[str, Image.Image]:
        """
        批量生成字型
        
        Args:
            characters: 字元列表
            reference_image: 參考風格圖片
            **kwargs: 其他參數
            
        Returns:
            字元到圖片的映射
        """
        results = {}
        
        for char in characters:
            logger.info(f"批量生成字型: {char}")
            result = self.generate_font(char, reference_image, **kwargs)
            if result:
                results[char] = result
            else:
                logger.warning(f"字型生成失敗: {char}")
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """獲取模型信息"""
        if self.session is None:
            return {"status": "mock", "message": "使用模擬模式"}
        
        return {
            "status": "active",
            "providers": self.session.get_providers(),
            "input_name": self.input_name,
            "output_name": self.output_name,
            "input_shape": self.input_shape,
            "model_path": self.model_path
        }
    
    def cleanup(self):
        """清理資源"""
        if self.session:
            del self.session
            self.session = None
        logger.info("SLM生成器已清理")


# 便捷函數
def create_slm_generator(model_path: str = None, use_npu: bool = True) -> SLMFontGenerator:
    """創建SLM生成器實例"""
    return SLMFontGenerator(model_path, use_npu)


if __name__ == "__main__":
    # 測試代碼
    generator = create_slm_generator(use_npu=False)
    
    # 創建測試圖片
    test_image = Image.new('RGB', (64, 64), color='white')
    
    # 測試生成
    result = generator.generate_font("A", test_image)
    if result:
        result.save("test_output.png")
        print("測試成功！輸出已保存為 test_output.png")
    
    generator.cleanup()


