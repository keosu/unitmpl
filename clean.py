#!/usr/bin/env python3
"""
项目清理脚本
清理项目中的临时文件、缓存文件和构建产物
"""
import os
import shutil
import glob
from pathlib import Path


def clean_python_cache():
    """清理Python缓存文件"""
    print("🧹 清理Python缓存文件...")
    
    # 清理__pycache__目录
    for pycache_dir in glob.glob("**/__pycache__", recursive=True):
        if os.path.exists(pycache_dir):
            shutil.rmtree(pycache_dir)
            print(f"  ✅ 删除: {pycache_dir}")
    
    # 清理.pyc文件
    for pyc_file in glob.glob("**/*.pyc", recursive=True):
        os.remove(pyc_file)
        print(f"  ✅ 删除: {pyc_file}")


def clean_node_modules():
    """清理Node.js依赖"""
    print("🧹 清理Node.js依赖...")
    
    for node_modules in glob.glob("**/node_modules", recursive=True):
        if os.path.exists(node_modules):
            print(f"  📦 发现 node_modules: {node_modules}")
            print("    💡 使用 'pnpm install' 重新安装依赖")


def clean_build_artifacts():
    """清理构建产物"""
    print("🧹 清理构建产物...")
    
    build_dirs = ["dist", "build", "unpackage", ".next", ".nuxt"]
    
    for build_dir in build_dirs:
        for path in glob.glob(f"**/{build_dir}", recursive=True):
            if os.path.exists(path):
                shutil.rmtree(path)
                print(f"  ✅ 删除: {path}")


def clean_logs():
    """清理日志文件"""
    print("🧹 清理日志文件...")
    
    log_patterns = ["**/*.log", "**/logs", "**/*.log.*"]
    
    for pattern in log_patterns:
        for log_path in glob.glob(pattern, recursive=True):
            if os.path.isfile(log_path):
                os.remove(log_path)
                print(f"  ✅ 删除: {log_path}")
            elif os.path.isdir(log_path):
                shutil.rmtree(log_path)
                print(f"  ✅ 删除目录: {log_path}")


def clean_temp_files():
    """清理临时文件"""
    print("🧹 清理临时文件...")
    
    temp_patterns = [
        "**/*.tmp", "**/*.temp", "**/*.swp", "**/*.swo", "**/*~",
        "**/test_*.py", "**/fix_*.py", "**/*_test.py"
    ]
    
    for pattern in temp_patterns:
        for temp_file in glob.glob(pattern, recursive=True):
            if os.path.isfile(temp_file):
                # 排除重要的测试文件
                if not any(important in temp_file for important in ["test_main", "conftest"]):
                    os.remove(temp_file)
                    print(f"  ✅ 删除: {temp_file}")


def clean_database_files():
    """清理数据库文件"""
    print("🧹 清理开发数据库文件...")
    
    db_patterns = ["**/*.db", "**/*.sqlite", "**/*.sqlite3"]
    
    for pattern in db_patterns:
        for db_file in glob.glob(pattern, recursive=True):
            if os.path.isfile(db_file):
                # 只删除明显的开发/测试数据库
                if any(dev_name in db_file.lower() for dev_name in ["dev", "test", "temp", "local"]):
                    os.remove(db_file)
                    print(f"  ✅ 删除: {db_file}")
                else:
                    print(f"  ⚠️  保留: {db_file} (生产数据库)")


def clean_os_files():
    """清理操作系统生成的文件"""
    print("🧹 清理操作系统文件...")
    
    os_patterns = [
        "**/.DS_Store", "**/.DS_Store?", "**/._*", 
        "**/.Spotlight-V100", "**/.Trashes",
        "**/ehthumbs.db", "**/Thumbs.db"
    ]
    
    for pattern in os_patterns:
        for os_file in glob.glob(pattern, recursive=True):
            if os.path.exists(os_file):
                if os.path.isfile(os_file):
                    os.remove(os_file)
                else:
                    shutil.rmtree(os_file)
                print(f"  ✅ 删除: {os_file}")


def main():
    """主清理函数"""
    print("🚀 开始项目清理...")
    print("=" * 50)
    
    try:
        clean_python_cache()
        print()
        
        clean_build_artifacts()
        print()
        
        clean_logs()
        print()
        
        clean_temp_files()
        print()
        
        clean_database_files()
        print()
        
        clean_os_files()
        print()
        
        clean_node_modules()
        print()
        
        print("=" * 50)
        print("✅ 项目清理完成！")
        print()
        print("💡 建议运行的命令:")
        print("   - 前端: pnpm install")
        print("   - 后端: pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ 清理过程中出错: {e}")


if __name__ == "__main__":
    main()
