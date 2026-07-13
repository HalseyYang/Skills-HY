#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
去重模块 - 管理已推送记录的本地存储
"""

import json
import hashlib
from pathlib import Path
from typing import Set, Dict, List
from datetime import datetime


class RegistryDeduplicator:
    """法规追踪去重器"""

    def __init__(self, data_dir: Path = None):
        """
        初始化去重器

        Args:
            data_dir: 数据存储目录，默认为 skill 目录下的 data 文件夹
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"

        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = data_dir / "seen_registry.json"

        # 内存缓存
        # 改为「来源 + URL」和「来源 + 标准化标题」复合键，防止 in-place 更新被误拦
        self._seen_keys: Set[str] = set()  # "source#url" 或 "source#title_normalized"
        self._registry: List[Dict] = []

        # 加载已有记录
        self._load()

    def _load(self):
        """从文件加载已推送记录"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._registry = data.get("items", [])

                    # 构建索引（source + url 和 source + title 复合键）
                    for item in self._registry:
                        source = (item.get("source") or "").lower()
                        url = (item.get("url") or "").lower()
                        title_norm = self._normalize_title(item.get("title") or "")
                        if url:
                            self._seen_keys.add(f"{source}#{url}")
                        if title_norm:
                            self._seen_keys.add(f"{source}#{title_norm}")
            except (json.JSONDecodeError, IOError):
                self._registry = []

    def _save(self):
        """保存记录到文件"""
        data = {
            "last_updated": datetime.now().isoformat(),
            "items": self._registry
        }
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _normalize_title(self, title: str) -> str:
        """标准化标题用于比较"""
        if not title:
            return ""
        # 转小写，去除多余空格
        return " ".join(title.lower().split())

    def is_seen(self, url: str = None, title: str = None, source: str = None) -> bool:
        """
        检查条目是否已推送过

        使用「来源 + URL」和「来源 + 标准化标题」复合键去重。
        同一来源的相同 URL 或相同标题才视为重复；
        不同来源的相同 URL/标题不受影响。
        这样可以正确处理 EU 来源 in-place 更新（URL 不变但内容/日期更新）的情况。

        Args:
            url: 条目 URL
            title: 条目标题
            source: 来源名称（用于构建复合键）

        Returns:
            True if already seen
        """
        s = (source or "").lower()
        if not s:
            # 无 source 时退化到纯 URL/标题匹配（兼容旧调用）
            if url:
                if url.lower().strip() in self._seen_keys:
                    return True
            if title:
                if self._normalize_title(title) in self._seen_keys:
                    return True
            return False

        url_key = f"{s}#{url.lower().strip()}" if url else None
        title_key = f"{s}#{self._normalize_title(title)}" if title else None

        if url_key and url_key in self._seen_keys:
            return True
        if title_key and title_key in self._seen_keys:
            return True

        return False

    def add(self, url: str, title: str, source: str, region: str,
            publish_date: str = None, tags: List[str] = None):
        """
        添加已推送记录

        Args:
            url: 条目 URL
            title: 条目标题
            source: 来源名称
            region: 区域（如 CN, EU, US, CA）
            publish_date: 发布日期
            tags: 标签列表
        """
        # 构建唯一标识（优先用 URL）
        url_normalized = url.lower().strip() if url else ""
        title_normalized = self._normalize_title(title)
        source_lower = (source or "").lower()

        item = {
            "id": hashlib.md5((url_normalized or title_normalized).encode()).hexdigest()[:12],
            "url": url_normalized,
            "title": title,
            "source": source,
            "region": region,
            "publish_date": publish_date,
            "tags": tags or [],
            "added_at": datetime.now().isoformat()
        }

        self._registry.append(item)
        # 复合键去重
        if url_normalized:
            self._seen_keys.add(f"{source_lower}#{url_normalized}")
        if title_normalized:
            self._seen_keys.add(f"{source_lower}#{title_normalized}")
        self._save()

    def filter_new(self, items: List[Dict]) -> List[Dict]:
        """
        过滤出未推送的新条目

        Args:
            items: 原始条目列表

        Returns:
            仅包含新条目的列表
        """
        new_items = []
        for item in items:
            if not self.is_seen(
                url=item.get("url"),
                title=item.get("title"),
                source=item.get("source")
            ):
                new_items.append(item)
        return new_items

    def get_statistics(self) -> Dict:
        """获取去重统计信息"""
        regions = {}
        for item in self._registry:
            region = item.get("region", "Unknown")
            regions[region] = regions.get(region, 0) + 1

        return {
            "total": len(self._registry),
            "by_region": regions,
            "last_updated": self._registry[-1]["added_at"] if self._registry else None
        }


# 测试代码
if __name__ == "__main__":
    dedup = RegistryDeduplicator()

    # 测试去重
    print("测试去重功能:")
    print(f"URL 'https://example.com' 是否已见过: {dedup.is_seen(url='https://example.com')}")

    # 添加一条记录
    dedup.add(
        url="https://example.com/test",
        title="测试法规",
        source="测试来源",
        region="CN"
    )

    print(f"添加后 URL 'https://example.com/test' 是否已见过: {dedup.is_seen(url='https://example.com/test')}")

    # 统计
    print(f"当前统计: {dedup.get_statistics()}")
