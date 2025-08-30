#!/usr/bin/env python3
"""
检查 typersonal FastAPI 环境的依赖包
"""

def check_packages():
    """检查关键包的安装状态"""
    print("=" * 60)
    print("typersonal FastAPI 环境依赖检查")
    print("=" * 60)
    
    packages = {
        "FastAPI": "fastapi",
        "Uvicorn": "uvicorn",
        "PyTorch": "torch",
        "Transformers": "transformers",
        "Diffusers": "diffusers",
        "Pillow": "PIL",
        "OpenCV": "cv2",
        "NumPy": "numpy",
        "Motor": "motor",
        "Pymongo": "pymongo"
    }
    
    all_good = True
    
    for package_name, import_name in packages.items():
        try:
            if import_name == "PIL":
                import PIL
                version = PIL.__version__
            elif import_name == "cv2":
                import cv2
                version = cv2.__version__
            else:
                module = __import__(import_name)
                version = getattr(module, '__version__', '未知版本')
            
            print(f"✅ {package_name}: {version}")
            
        except ImportError as e:
            print(f"❌ {package_name}: 导入失败 - {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️  {package_name}: 检查失败 - {e}")
            all_good = False
    
    return all_good

def check_typersonal_modules():
    """检查 typersonal 相关模块"""
    print("\n" + "=" * 60)
    print("typersonal 模块检查")
    print("=" * 60)
    
    # 添加 typersonal 路径到 Python 路径
    import sys
    import os
    typersonal_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'typersonal'))
    if typersonal_path not in sys.path:
        sys.path.append(typersonal_path)
        print(f"已添加路径: {typersonal_path}")
    
    modules = [
        "shared.initializer",
        "shared.core"
    ]
    
    all_good = True
    
    for module_name in modules:
        try:
            module = __import__(module_name, fromlist=[''])
            print(f"✅ {module_name}: 导入成功")
        except ImportError as e:
            print(f"❌ {module_name}: 导入失败 - {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️  {module_name}: 检查失败 - {e}")
            all_good = False
    
    return all_good

def check_pytorch_info():
    """检查 PyTorch 信息"""
    print("\n" + "=" * 60)
    print("PyTorch 配置信息")
    print("=" * 60)
    
    try:
        import torch
        
        print(f"PyTorch 版本: {torch.__version__}")
        print(f"CUDA 可用: {torch.cuda.is_available()}")
        print(f"CUDA 版本: {torch.version.cuda if torch.cuda.is_available() else 'N/A'}")
        print(f"设备数量: {torch.cuda.device_count() if torch.cuda.is_available() else 0}")
        
        # 测试基本操作
        x = torch.randn(3, 3)
        y = torch.randn(3, 3)
        z = torch.mm(x, y)
        print(f"CPU 张量运算测试: ✅ (矩阵乘法: {z.shape})")
        
        return True
        
    except Exception as e:
        print(f"PyTorch 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("开始检查 typersonal FastAPI 环境...\n")
    
    # 检查基本包
    packages_ok = check_packages()
    
    # 检查 typersonal 模块
    modules_ok = check_typersonal_modules()
    
    # 检查 PyTorch
    pytorch_ok = check_pytorch_info()
    
    # 总结
    print("\n" + "=" * 60)
    print("检查结果总结")
    print("=" * 60)
    
    if packages_ok and modules_ok and pytorch_ok:
        print("🎉 所有检查通过！环境配置成功！")
        print("✅ 可以启动 FastAPI 服务器")
        print("\n启动命令:")
        print("  - Windows: 双击 start_server.bat")
        print("  - PowerShell: .\\start_server.ps1")
        print("  - 手动: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("❌ 环境配置有问题，请检查以下项目:")
        if not packages_ok:
            print("  - 基本依赖包安装")
        if not modules_ok:
            print("  - typersonal 模块路径")
        if not pytorch_ok:
            print("  - PyTorch 配置")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
