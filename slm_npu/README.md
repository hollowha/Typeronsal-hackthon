# SLM NPU 字型生成

這個資料夾包含使用Snapdragon NPU (SLM) 進行字型生成的相關代碼。

## 功能特點

- 使用Qualcomm QNN執行提供者
- 支援HTP (Hexagon Tensor Processor) 後端
- 針對字型生成優化的ONNX模型
- 支援FP16精度和高效能模式

## 文件結構

```
slm_npu/
├── README.md                    # 說明文件
├── requirements.txt             # Python依賴
├── models/                      # ONNX模型文件
├── slm_generator.py            # 主要的SLM生成器
├── ort_qnn_htp_slm.py         # QNN HTP執行範例
├── model_converter.py          # 模型轉換工具
└── test_slm.py                 # 測試腳本
```

## 使用方法

1. 安裝依賴：`pip install -r requirements.txt`
2. 運行測試：`python test_slm.py`
3. 在FastAPI中使用：導入`slm_generator.py`

## 技術規格

- 支援的後端：CPU/GPU/HTP
- 精度：FP16 (HTP), FP32 (CPU/GPU)
- 效能模式：high_performance
- 模型格式：ONNX


