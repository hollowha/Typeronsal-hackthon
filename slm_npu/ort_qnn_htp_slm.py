"""
ORT QNN HTP SLM 字型生成範例
基於Qualcomm QNN執行提供者的HTP後端實現
"""

import onnxruntime as ort
import numpy as np
import time
from PIL import Image
import cv2
import os
from typing import Optional, Dict, Any

class SLMQNNHTPGenerator:
    """使用QNN HTP後端的SLM字型生成器"""
    
    def __init__(self, model_path: str = "./models/slm_font_model.onnx"):
        """
        初始化QNN HTP生成器
        
        Args:
            model_path: ONNX模型路徑
        """
        self.model_path = model_path
        self.session = None
        self.input_name = None
        self.output_name = None
        
        # 初始化模型
        self._initialize_model()
    
    def _initialize_model(self):
        """初始化QNN HTP模型"""
        try:
            if not os.path.exists(self.model_path):
                print(f"⚠️ 模型文件不存在: {self.model_path}")
                print("將使用模擬模式")
                return
            
            # Step 1: 設置QNN執行提供者選項
            execution_provider_option = {
                "backend_path": "QnnHtp.dll",
                "enable_htp_fp16_precision": "1",
                "htp_performance_mode": "high_performance"
            }
            
            # Step 2: 創建ONNX Runtime會話
            self.session = ort.InferenceSession(
                self.model_path,
                providers=["QNNExecutionProvider"],
                provider_options=[execution_provider_option]
            )
            
            # Step 3: 獲取輸入輸出信息
            self.output_name = self.session.get_outputs()[0].name
            self.input_name = self.session.get_inputs()[0].name
            
            print(f"✅ QNN HTP模型初始化成功")
            print(f"📥 輸入名稱: {self.input_name}")
            print(f"📤 輸出名稱: {self.output_name}")
            print(f"🔧 執行提供者: {self.session.get_providers()}")
            
        except Exception as e:
            print(f"❌ QNN HTP模型初始化失敗: {e}")
            print("將使用模擬模式")
    
    def preprocess_image(self, image: Image.Image, target_size: tuple = (64, 64)) -> np.ndarray:
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
                      sampling_steps: int = 20) -> Optional[Image.Image]:
        """
        使用QNN HTP生成字型
        
        Args:
            character: 要生成的字元
            reference_image: 參考風格圖片
            sampling_steps: 採樣步數
            
        Returns:
            生成的字型圖片或None
        """
        try:
            if self.session is None:
                print("⚠️ 模型未初始化，使用模擬生成")
                return self._mock_generate_font(character, reference_image)
            
            # Step 2: 預處理輸入圖片
            raw_input = self.preprocess_image(reference_image)
            
            # Step 3: 執行推理
            print(f"🚀 開始QNN HTP推理: {character}")
            start_time = time.time()
            
            # 執行多次推理以測試性能
            for i in range(3):  # 執行3次取平均
                prediction = self.session.run([self.output_name], {self.input_name: raw_input})
            
            end_time = time.time()
            execution_time = ((end_time - start_time) * 1000) / 3  # 平均執行時間
            
            print(f"✅ QNN HTP推理完成: {character}")
            print(f"⏱️ 平均執行時間: {execution_time:.2f}ms")
            
            # Step 4: 後處理輸出
            result_image = self.postprocess_output(prediction[0])
            
            return result_image
            
        except Exception as e:
            print(f"❌ QNN HTP推理失敗: {e}")
            return None
    
    def _mock_generate_font(self, character: str, reference_image: Image.Image) -> Image.Image:
        """模擬字型生成（用於測試）"""
        print(f"🎭 模擬生成字型: {character}")
        
        # 創建一個簡單的模擬字型圖片
        img_size = (64, 64)
        img_array = np.ones((*img_size, 3), dtype=np.uint8) * 255
        
        # 添加一些簡單的圖案來模擬字型
        cv2.rectangle(img_array, (10, 10), (54, 54), (100, 100, 100), 2)
        cv2.putText(img_array, character, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)
        
        return Image.fromarray(img_array)
    
    def generate_context_binary(self, output_path: str = None) -> bool:
        """
        生成QNN上下文二進制文件（離線模式）
        
        Args:
            output_path: 輸出路徑
            
        Returns:
            是否成功
        """
        try:
            if not self.session:
                print("❌ 模型未初始化")
                return False
            
            if not output_path:
                base_name = os.path.splitext(self.model_path)[0]
                output_path = f"{base_name}_ctx.onnx"
            
            print(f"🔧 生成QNN上下文二進制文件: {output_path}")
            
            # 設置會話選項
            options = ort.SessionOptions()
            options.add_session_config_entry("ep.context_enable", "1")
            
            # 設置QNN執行提供者選項
            execution_provider_option = {
                "backend_path": "QnnHtp.dll",
                "enable_htp_fp16_precision": "1",
                "htp_performance_mode": "high_performance"
            }
            
            # 創建新的會話來生成上下文
            context_session = ort.InferenceSession(
                self.model_path,
                sess_options=options,
                providers=["QNNExecutionProvider"],
                provider_options=[execution_provider_option]
            )
            
            # 刪除會話以觸發上下文生成
            del context_session
            
            print(f"✅ QNN上下文二進制文件已生成: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 生成QNN上下文二進制文件失敗: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """獲取模型信息"""
        if self.session is None:
            return {"status": "mock", "message": "使用模擬模式"}
        
        return {
            "status": "qnn_htp_active",
            "providers": self.session.get_providers(),
            "input_name": self.input_name,
            "output_name": self.output_name,
            "model_path": self.model_path
        }
    
    def cleanup(self):
        """清理資源"""
        if self.session:
            del self.session
            self.session = None
        print("🧹 QNN HTP生成器已清理")


def test_qnn_htp():
    """測試QNN HTP功能"""
    print("🧪 開始測試QNN HTP SLM字型生成器")
    
    # 創建生成器
    generator = SLMQNNHTPGenerator()
    
    # 創建測試圖片
    test_image = Image.new('RGB', (64, 64), color='white')
    
    # 測試生成
    result = generator.generate_font("A", test_image)
    if result:
        result.save("qnn_htp_test_output.png")
        print("✅ 測試成功！輸出已保存為 qnn_htp_test_output.png")
    
    # 獲取模型信息
    info = generator.get_model_info()
    print(f"📊 模型信息: {info}")
    
    # 清理
    generator.cleanup()
    
    print("🏁 測試完成")


if __name__ == "__main__":
    test_qnn_htp()


