#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMA 上传模块 - 医疗器械法规追踪 Skill
支持创建笔记并添加到知识库
"""

import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime


class IMAUploader:
    """IMA 上传器"""
    
    BASE_URL = "https://ima.qq.com"
    KB_ID = "ihJNh4Nl87Wqv-XLfXyOJSW1NMOBnVnk-HBnlcYgL4o="
    KB_NAME = "MD法规更新汇总"
    
    def __init__(self, client_id: str = None, api_key: str = None):
        """
        初始化 IMA 上传器
        
        Args:
            client_id: IMA Client ID（可选，从配置文件加载）
            api_key: IMA API Key（可选，从配置文件加载）
        """
        self.client_id = client_id
        self.api_key = api_key
        self._load_credentials()
    
    def _load_credentials(self):
        """加载 IMA 凭证"""
        import os
        
        # 环境变量优先
        self.client_id = os.environ.get("IMA_OPENAPI_CLIENTID", self.client_id)
        self.api_key = os.environ.get("IMA_OPENAPI_APIKEY", self.api_key)
        
        # 配置文件次之
        config_dir = Path.home() / ".config" / "ima"
        
        if not self.client_id:
            client_id_file = config_dir / "client_id"
            if client_id_file.exists():
                # 尝试 UTF-16（带 BOM）
                for enc in ["utf-16", "utf-8", "gbk"]:
                    try:
                        self.client_id = client_id_file.read_text(encoding=enc).strip()
                        break
                    except:
                        continue
        
        if not self.api_key:
            api_key_file = config_dir / "api_key"
            if api_key_file.exists():
                for enc in ["utf-16", "utf-8", "gbk"]:
                    try:
                        self.api_key = api_key_file.read_text(encoding=enc).strip()
                        break
                    except:
                        continue
    
    def _api_call(self, path: str, data: dict) -> dict:
        """
        调用 IMA API
        
        Args:
            path: API 路径
            data: 请求数据
            
        Returns:
            API 响应
        """
        if not self.client_id or not self.api_key:
            raise ValueError("IMA 凭证未配置")
        
        url = f"{self.BASE_URL}/{path}"
        json_data = json.dumps(data).encode("utf-8")
        
        req = urllib.request.Request(
            url,
            data=json_data,
            headers={
                "ima-openapi-clientid": self.client_id,
                "ima-openapi-apikey": self.api_key,
                "Content-Type": "application/json; charset=utf-8"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            raise Exception(f"HTTP {e.code}: {error_body}")
        except Exception as e:
            raise Exception(f"API 调用失败: {str(e)}")
    
    def create_note(self, content: str, title: str = None) -> dict:
        """
        创建笔记
        
        Args:
            content: Markdown 内容
            title: 标题（可选）
            
        Returns:
            {"success": True, "note_id": "xxx"} 或 {"success": False, "error": "xxx"}
        """
        try:
            # 确保内容是 UTF-8
            if isinstance(content, str):
                content = content.encode("utf-8").decode("utf-8")
            
            result = self._api_call("openapi/note/v1/import_doc", {
                "content_format": 1,  # Markdown
                "content": content
            })
            
            if result.get("code") == 0:
                note_id = result.get("data", {}).get("note_id")
                return {
                    "success": True,
                    "note_id": note_id
                }
            else:
                return {
                    "success": False,
                    "error": result.get("msg", "创建笔记失败")
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def add_to_knowledge_base(self, note_id: str, title: str = None) -> dict:
        """
        将笔记添加到知识库
        
        Args:
            note_id: 笔记 ID
            title: 知识库中显示的标题
            
        Returns:
            {"success": True, "media_id": "xxx"} 或 {"success": False, "error": "xxx"}
        """
        if not title:
            title = f"医疗器械法规更新报告 ({datetime.now().strftime('%Y-%m-%d')})"
        
        try:
            result = self._api_call("openapi/wiki/v1/add_knowledge", {
                "media_type": 11,  # 笔记类型
                "note_info": {
                    "content_id": note_id
                },
                "title": title,
                "knowledge_base_id": self.KB_ID
            })
            
            if result.get("code") == 0:
                return {
                    "success": True,
                    "media_id": result.get("data", {}).get("media_id")
                }
            else:
                return {
                    "success": False,
                    "error": result.get("msg", "添加知识库失败")
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def upload_report(self, content: str, title: str = None) -> dict:
        """
        上传报告到 IMA 知识库（完整流程）
        
        Args:
            content: Markdown 内容
            title: 报告标题
            
        Returns:
            完整结果
        """
        # 步骤1: 创建笔记
        note_result = self.create_note(content, title)
        if not note_result.get("success"):
            return {
                "success": False,
                "step": "create_note",
                "error": note_result.get("error")
            }
        
        note_id = note_result.get("note_id")
        
        # 步骤2: 添加到知识库
        kb_result = self.add_to_knowledge_base(note_id, title)
        if not kb_result.get("success"):
            return {
                "success": False,
                "step": "add_to_knowledge_base",
                "note_id": note_id,
                "error": kb_result.get("error")
            }
        
        return {
            "success": True,
            "note_id": note_id,
            "media_id": kb_result.get("media_id"),
            "knowledge_base": self.KB_NAME
        }


# 便捷函数
def upload_to_ima(content: str, title: str = None) -> dict:
    """上传报告到 IMA"""
    uploader = IMAUploader()
    return uploader.upload_report(content, title)


def create_ima_note(content: str, title: str = None) -> dict:
    """创建 IMA 笔记"""
    uploader = IMAUploader()
    return uploader.create_note(content, title)


def add_note_to_kb(note_id: str, title: str = None) -> dict:
    """将笔记添加到知识库"""
    uploader = IMAUploader()
    return uploader.add_to_knowledge_base(note_id, title)


if __name__ == "__main__":
    # 测试
    uploader = IMAUploader()
    
    if not uploader.client_id or not uploader.api_key:
        print("错误: IMA 凭证未配置")
        exit(1)
    
    print(f"Client ID: {uploader.client_id[:10]}...")
    
    # 测试创建笔记
    test_content = """# 测试报告

> 这是一条测试消息

## 内容

这是一条测试内容，验证 IMA API 是否正常工作。

---
*自动生成*
"""
    
    result = uploader.upload_report(test_content, "IMA API 测试")
    print(json.dumps(result, indent=2, ensure_ascii=False))
