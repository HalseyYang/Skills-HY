#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法规追踪解析器模块

提供各来源网站的内容抓取和解析功能
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
from zoneinfo import ZoneInfo

# 可选依赖
try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


BEIJING_TZ = ZoneInfo("Asia/Shanghai")

# HTTP 头
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

# URL 基础映射表
URL_BASE_MAP = {
    "cmde": "https://www.cmde.org.cn",
    "nmpa": "https://www.nmpa.gov.cn",
    "nifdc": "https://www.nifdc.org.cn",
    "ydcmdei": "https://www.ydcmdei.org.cn",
    "mdei": "https://www.mdei.org.cn",
    "ec": "https://health.ec.europa.eu",
    "fda": "https://www.fda.gov",
    "ca": "https://www.canada.ca",
    "imdrf": "https://www.imdrf.org",
    "teamnb": "https://www.team-nb.org",
    "eurlex": "https://eur-lex.europa.eu",
}

# 噪音关键词 - 这些标题将被过滤掉
NOISE_KEYWORDS = [
    "rss", "feed", "atom",
    "events", "event", "calendar", "会议", "活动", "研讨会", "conference",
    "publications", "publication", "publications list", "list of publications",
    "related links", "external links", "quick links",
    "home", "homepage", "index", "main page",
    "subscribe", "newsletter", "email updates",
    "contact us", "about us", "about", "disclaimer",
    "cookie", "privacy", "terms",
    # EC特有噪音
    "register now", "registration", "recording available",
    "view all", "read more", "learn more",
    "notified body", "nb actors", "press corner",
]


def normalize_url(url: str, base_url: str = "") -> str:
    """
    规范化URL，将相对路径转换为绝对路径
    
    Args:
        url: 原始URL（可能是相对路径）
        base_url: 基础URL，用于解析相对路径
        
    Returns:
        规范化后的绝对URL
    """
    if not url:
        return ""
    
    # 已经是绝对路径
    if url.startswith(("http://", "https://")):
        return url
    
    # 清理 URL（移除空白、换行等）
    url = url.strip()
    
    # 处理不同类型的相对路径
    if url.startswith("//"):
        # 双斜杠开头的协议相对URL
        return "https:" + url
    elif url.startswith("/"):
        # 绝对路径，从根目录开始
        # 尝试从 base_url 提取域名
        if base_url:
            parsed = urlparse(base_url)
            return f"{parsed.scheme}://{parsed.netloc}{url}"
        # 尝试从 URL_BASE_MAP 匹配
        for key, base in URL_BASE_MAP.items():
            if key in base_url.lower():
                return base + url
    else:
        # 相对路径，需要拼接
        if base_url:
            return urljoin(base_url, url)
    
    return url


def is_noise_title(title: str) -> bool:
    """
    判断标题是否为噪音内容
    
    Args:
        title: 标题文本
        
    Returns:
        True 表示噪音内容，应该过滤
    """
    if not title:
        return True
    
    title_lower = title.lower().strip()
    
    # 检查是否完全匹配噪音关键词
    for keyword in NOISE_KEYWORDS:
        if title_lower == keyword or title_lower.startswith(keyword + " "):
            return True
    
    # 检查标题长度过短（通常是导航项）
    if len(title) < 5:
        return True
    
    return False


def fetch_page_requests(url: str, timeout: int = 30) -> Optional[str]:
    """使用 requests 抓取页面"""
    if not REQUESTS_AVAILABLE:
        return None

    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        response.encoding = response.apparent_encoding or 'utf-8'
        return response.text
    except Exception as e:
        print(f"  [FAIL] requests 抓取失败: {url} - {e}")
        return None


def fetch_page_playwright(url: str, timeout: int = 30) -> Optional[str]:
    """使用 Playwright 抓取页面（处理 JS 渲染）"""
    if not PLAYWRIGHT_AVAILABLE:
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
            content = page.content()
            browser.close()
            return content
    except Exception as e:
        print(f"  [FAIL] Playwright 抓取失败: {url} - {e}")
        return None


def fetch_page(url: str, use_dynamic: bool = False) -> Optional[str]:
    """抓取页面内容"""
    content = fetch_page_requests(url)
    if content:
        return content
    if use_dynamic:
        return fetch_page_playwright(url)
    return None


def parse_date(date_str: str) -> Optional[str]:
    """解析日期字符串"""
    if not date_str:
        return None

    date_str = date_str.strip()
    patterns = [
        (r'(\d{4})-(\d{1,2})-(\d{1,2})', '%Y-%m-%d'),
        (r'(\d{4})/(\d{1,2})/(\d{1,2})', '%Y/%m/%d'),
        (r'(\d{4})年(\d{1,2})月(\d{1,2})日', '%Y年%m月%d日'),
        (r'(\d{4})\.(\d{1,2})\.(\d{1,2})', '%Y.%m.%d'),
    ]

    for pattern, fmt in patterns:
        match = re.search(pattern, date_str)
        if match:
            try:
                if '年' in fmt:
                    parts = match.groups()
                    dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
                else:
                    dt = datetime.strptime(match.group(), fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

    return None


def filter_by_date_range(items: List[Dict], start_date: datetime,
                         end_date: datetime) -> List[Dict]:
    """按日期范围过滤条目"""
    filtered = []
    for item in items:
        pub_date_str = item.get("publish_date", "")
        pub_date = parse_date(pub_date_str)

        if pub_date:
            try:
                pub_dt = datetime.strptime(pub_date, "%Y-%m-%d")
                pub_dt = pub_dt.replace(tzinfo=BEIJING_TZ)
                if start_date <= pub_dt <= end_date:
                    item["publish_date"] = pub_date
                    filtered.append(item)
            except ValueError:
                filtered.append(item)
        else:
            filtered.append(item)

    return filtered


def parse_nmpa(html: str, source_name: str, base_url: str = "") -> List[Dict]:
    """解析 NMPA 药监局页面"""
    if not html or not REQUESTS_AVAILABLE:
        return []

    items = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        news_items = soup.select('ul.list li, .news_list li, .article-list li')

        for li in news_items:
            link_tag = li.select_one('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            
            # 过滤噪音
            if is_noise_title(title):
                continue
            
            raw_url = link_tag.get('href', '')
            url = normalize_url(raw_url, base_url or "https://www.nmpa.gov.cn")

            # 尝试从列表项中提取日期
            date_tag = li.select_one('.date, .time, span')
            pub_date = parse_date(date_tag.get_text() if date_tag else '')
            
            # 也尝试从父容器查找日期
            if not pub_date:
                parent = li.find_parent(['ul', 'div'])
                if parent:
                    date_tag = parent.select_one('.date, .time')
                    pub_date = parse_date(date_tag.get_text() if date_tag else '')

            if title:
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": pub_date,
                    "tags": extract_tags(title)
                })
    except Exception as e:
        print(f"  [FAIL] 解析 NMPA 失败: {e}")

    return items


def parse_cmde(html: str, source_name: str, base_url: str = "") -> List[Dict]:
    """解析 CMDE 器械审评中心页面"""
    if not html:
        return []

    items = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # 扩展选择器列表
        selectors = [
            '.news_list li', '.article-list li', '.list ul li', 
            '.main-list li', '.xwlist li', '.list li',
            '.content-list li', '.article li', 
            '.news-list li', '.infolist li'
        ]

        news_items = []
        for selector in selectors:
            news_items = soup.select(selector)
            if news_items:
                break

        for li in news_items:
            link_tag = li.select_one('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            
            # 过滤噪音
            if is_noise_title(title):
                continue
            
            raw_url = link_tag.get('href', '')
            url = normalize_url(raw_url, base_url or "https://www.cmde.org.cn")

            # 尝试从列表项中提取日期
            date_tag = li.select_one('.date, .time, span, font, .date-text')
            pub_date = parse_date(date_tag.get_text() if date_tag else '')
            
            # 也尝试从父容器查找日期
            if not pub_date:
                parent = li.find_parent(['ul', 'div', 'section'])
                if parent:
                    date_tag = parent.select_one('.date, .time, .time-text, .date-text')
                    pub_date = parse_date(date_tag.get_text() if date_tag else '')

            if title:
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": pub_date,
                    "tags": extract_tags(title)
                })
    except Exception as e:
        print(f"  [FAIL] 解析 CMDE 失败: {e}")

    return items


def parse_ec_health(html: str, source_name: str, base_url: str = "") -> List[Dict]:
    """解析欧盟 EC Health 页面
    
    欧盟EC网站使用不同的HTML结构：
    - 日期通常在 <time> 标签的 datetime 属性或文本中
    - 内容通常在 article 或 .view-list 容器中
    - 也可能在 sidebar 或 related-content 中
    - 有些页面需要从标题或URL中提取日期信息
    """
    if not html:
        return []

    items = []
    seen_urls = set()  # 去重
    seen_titles = set()  # 标题去重
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # EC特有的噪音URL模式 - 过滤掉
        noise_url_patterns = [
            "/events", "/event/", "/calendar",
            "/publications", "/publication/",
            "/newsletter", "/subscribe", "/contact",
            "/presscorner", "/newsroom",
            "feed", "rss", "atom",
            "/about", "/disclaimer", "/privacy",
            "/node/", "/page=", "#", "javascript:",
        ]
        
        # EC特有的噪音标题关键词
        ec_noise_keywords = [
            "register now", "registration", "recording available",
            "view all", "read more", "learn more",
            "language-switcher", "language selector",
        ]
        
        # 高价值法规关键词 - 这些内容优先保留
        high_value_keywords = [
            'mdcg', 'mdr', 'ivdr', 'guidance', 'regulation', 'directive',
            'q&a', 'q and a', 'standard', 'harmonised', 'harmonized',
            'udi', 'eudamed', 'nb', 'notified body',
            'pmcf', 'pms', 'psur', 'fsca', 'fsn',
            'clinical', 'post-market', 'vigilance',
            'borderline', 'classification', 'software',
            'ivd', 'mdsw', 'aimd',
        ]
        
        # 多种选择器策略
        selector_groups = [
            # 最新动态页面 - 最优先
            ['.view-list .views-row', '.view-list article', '.news-list .item', '.documents-list li'],
            # 一般内容页面
            ['article', '.content article', '.page-content article'],
            # 列表页面
            ['.item-list li', '.document-list li', '.listing li'],
            # 侧边栏链接
            ['aside a', '.sidebar a', '.related a'],
        ]
        
        news_items = []
        for selectors in selector_groups:
            for sel in selectors:
                news_items = soup.select(sel)
                if news_items:
                    break
            if news_items:
                break

        for item in news_items:
            link_tag = item.select_one('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            raw_url = link_tag.get('href', '')
            
            # URL噪音过滤
            url_lower = raw_url.lower()
            is_noise_url = any(pattern in url_lower for pattern in noise_url_patterns)
            
            # 过滤噪音URL
            if is_noise_url:
                continue
            
            # 过滤噪音标题
            if is_noise_title(title):
                continue
            
            # EC特定噪音标题过滤
            title_lower = title.lower()
            if any(kw in title_lower for kw in ec_noise_keywords):
                # 但保留包含高价值法规关键词的内容
                has_high_value = any(kw in title_lower for kw in high_value_keywords)
                if not has_high_value:
                    continue
            
            url = normalize_url(raw_url, base_url or "https://health.ec.europa.eu")
            
            # 去重（URL和标题都检查）
            if url in seen_urls or title.lower() in seen_titles:
                continue
            seen_urls.add(url)
            seen_titles.add(title.lower())
            
            # 检查是否是法规相关链接
            is_regulation_link = any(kw in url_lower for kw in high_value_keywords)
            
            # 如果不是高价值链接，尝试从标题判断
            if not is_regulation_link:
                has_high_value_title = any(kw in title_lower for kw in high_value_keywords)
                if not has_high_value_title:
                    # 跳过非法规相关链接
                    continue

            # 解析日期 - EC使用多种格式
            pub_date = None
            
            # 1. 尝试 <time> 标签
            time_tag = item.select_one('time')
            if time_tag:
                datetime_attr = time_tag.get('datetime', '')
                if datetime_attr:
                    pub_date = parse_date(datetime_attr.split('T')[0])
                if not pub_date:
                    pub_date = parse_date(time_tag.get_text(strip=True))
            
            # 2. 尝试 class="date" 的元素
            if not pub_date:
                date_tag = item.select_one('.date, .date-display, .published, .created')
                if date_tag:
                    pub_date = parse_date(date_tag.get_text(strip=True))
            
            # 3. 从标题中提取日期（如 "MDCG 2025-10"）
            if not pub_date:
                date_match = re.search(r'\((\d{4}-\d{2}|\d{4})\)', title)
                if date_match:
                    date_str = date_match.group(1)
                    if '-' in date_str:
                        pub_date = date_str  # 已经是 YYYY-MM 格式
                    else:
                        pub_date = date_str  # 只有年份

            # 4. 从URL中提取日期
            if not pub_date:
                url_date_match = re.search(r'(\d{4}-\d{2}-\d{2}|\d{4}-\d{2}|\d{8})', url)
                if url_date_match:
                    date_str = url_date_match.group(1)
                    if len(date_str) == 8:
                        pub_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                    elif len(date_str) == 6:
                        pub_date = f"{date_str[:4]}-{date_str[4:6]}"
                    elif len(date_str) == 4:
                        pub_date = date_str
            
            # 5. 尝试从父容器的文本中提取日期
            if not pub_date:
                parent = item.find_parent(['li', 'div', 'article'])
                if parent:
                    parent_text = parent.get_text()
                    date_match = re.search(r'(\d{1,2}\s+\w+\s+\d{4})|(\d{4}-\d{2}-\d{2})', parent_text)
                    if date_match:
                        pub_date = parse_date(date_match.group())

            if title:
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": pub_date,
                    "tags": extract_tags(title)
                })
    except Exception as e:
        print(f"  [FAIL] 解析 EC Health 失败: {e}")

    return items


def parse_fda(html: str, source_name: str, base_url: str = "") -> List[Dict]:
    """解析 FDA 相关页面"""
    if not html:
        return []

    items = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        news_items = soup.select('.list-view .item, .news-events .item, .views-row, article, .listing li, .documents-list li')

        for item in news_items:
            link_tag = item.select_one('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            
            # 过滤噪音
            if is_noise_title(title):
                continue
            
            raw_url = link_tag.get('href', '')
            url = normalize_url(raw_url, base_url or "https://www.fda.gov")

            # FDA日期解析
            pub_date = None
            time_tag = item.select_one('time')
            if time_tag:
                datetime_attr = time_tag.get('datetime', '')
                if datetime_attr:
                    pub_date = parse_date(datetime_attr.split('T')[0])
                if not pub_date:
                    pub_date = parse_date(time_tag.get_text(strip=True))
            
            if not pub_date:
                date_tag = item.select_one('.date, time, .published, .meta')
                pub_date = parse_date(date_tag.get_text() if date_tag else '')

            if title:
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": pub_date,
                    "tags": extract_tags(title)
                })
    except Exception as e:
        print(f"  [FAIL] 解析 FDA 失败: {e}")

    return items


def parse_ca_health(html: str, source_name: str, base_url: str = "") -> List[Dict]:
    """解析加拿大 Health Canada 页面"""
    if not html:
        return []

    items = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        news_items = soup.select('.items-row, .news-list li, .listing li, article')

        for item in news_items:
            link_tag = item.select_one('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            
            # 过滤噪音
            if is_noise_title(title):
                continue
            
            raw_url = link_tag.get('href', '')
            url = normalize_url(raw_url, base_url or "https://www.canada.ca")

            # Canada日期解析
            pub_date = None
            time_tag = item.select_one('time')
            if time_tag:
                datetime_attr = time_tag.get('datetime', '')
                if datetime_attr:
                    pub_date = parse_date(datetime_attr.split('T')[0])
            
            if not pub_date:
                date_tag = item.select_one('.date, time, .published')
                pub_date = parse_date(date_tag.get_text() if date_tag else '')

            if title:
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": pub_date,
                    "tags": extract_tags(title)
                })
    except Exception as e:
        print(f"  [FAIL] 解析 Health Canada 失败: {e}")

    return items


def parse_imdrf(html: str, source_name: str, base_url: str = "") -> List[Dict]:
    """解析 IMDRF 页面"""
    if not html:
        return []

    items = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        news_items = soup.select('.view-list .item, .document-list li, article')

        for item in news_items:
            link_tag = item.select_one('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            
            # 过滤噪音
            if is_noise_title(title):
                continue
            
            raw_url = link_tag.get('href', '')
            url = normalize_url(raw_url, base_url or "https://www.imdrf.org")

            # IMDRF日期解析
            pub_date = None
            time_tag = item.select_one('time')
            if time_tag:
                datetime_attr = time_tag.get('datetime', '')
                if datetime_attr:
                    pub_date = parse_date(datetime_attr.split('T')[0])
            
            if not pub_date:
                date_tag = item.select_one('.date, .published')
                pub_date = parse_date(date_tag.get_text() if date_tag else '')

            if title:
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": pub_date,
                    "tags": extract_tags(title)
                })
    except Exception as e:
        print(f"  [FAIL] 解析 IMDRF 失败: {e}")

    return items


def parse_teamnb(html: str, source_name: str, base_url: str = "") -> List[Dict]:
    """解析 Team NB 页面"""
    if not html:
        return []

    items = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        news_items = soup.select('.news-item, .post, .item-list li, article')

        for item in news_items:
            link_tag = item.select_one('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            
            # 过滤噪音
            if is_noise_title(title):
                continue
            
            raw_url = link_tag.get('href', '')
            url = normalize_url(raw_url, base_url or "https://www.team-nb.org")

            # Team NB日期解析
            pub_date = None
            time_tag = item.select_one('time')
            if time_tag:
                datetime_attr = time_tag.get('datetime', '')
                if datetime_attr:
                    pub_date = parse_date(datetime_attr.split('T')[0])
            
            if not pub_date:
                date_tag = item.select_one('.date, .time, .posted-on, .entry-date')
                pub_date = parse_date(date_tag.get_text() if date_tag else '')

            if title:
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": pub_date,
                    "tags": extract_tags(title)
                })
    except Exception as e:
        print(f"  [FAIL] 解析 Team NB 失败: {e}")

    return items


def parse_generic_cn(html: str, source_name: str, base_url: str = "") -> List[Dict]:
    """解析通用中国来源页面（如中检院、标准管理中心等）"""
    if not html:
        return []

    items = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # 通用中文网站列表选择器
        selectors = [
            'ul.list li', 'ul.news-list li', 'ul.article-list li',
            '.list li', '.news-list li', '.article-list li',
            '.infolist li', '.info-list li',
            '.news li', '.news-ul li',
            'table.list tr', '.tab-content li',
            '.main-list li', '.content-list li'
        ]

        news_items = []
        for selector in selectors:
            news_items = soup.select(selector)
            if news_items:
                break

        for li in news_items:
            link_tag = li.select_one('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            
            # 过滤噪音
            if is_noise_title(title):
                continue
            
            raw_url = link_tag.get('href', '')
            url = normalize_url(raw_url, base_url or "https://www.nifdc.org.cn")

            # 尝试多种日期格式
            pub_date = None
            date_tag = li.select_one('.date, .time, .datetime, span, font, .date-text')
            if date_tag:
                pub_date = parse_date(date_tag.get_text())
            
            if not pub_date:
                parent = li.find_parent(['ul', 'div', 'table'])
                if parent:
                    date_tag = parent.select_one('.date, .time, .datetime')
                    if date_tag:
                        pub_date = parse_date(date_tag.get_text())

            if title:
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": pub_date,
                    "tags": extract_tags(title)
                })
    except Exception as e:
        print(f"  [FAIL] 解析通用CN来源失败: {e}")

    return items


def extract_tags(title: str) -> List[str]:
    """从标题中提取标签"""
    tags = []

    tag_keywords = {
        "征求意见": "征求意见",
        "意见征求": "征求意见",
        "修订": "修订",
        "正式发布": "正式发布",
        "实施": "实施",
        "解读": "解读",
        "指南": "指南",
        "指导原则": "指导原则",
        "注册": "注册",
        "临床": "临床",
        "标准": "标准",
        "召回": "召回",
        "警示": "警示",
        "通知": "通知",
        "公告": "公告",
        "MDR": "MDR",
        "IVDR": "IVDR",
        "FDA": "FDA",
        "CE": "CE",
        "510(k)": "510(k)",
        "PMA": "PMA",
        "UDI": "UDI",
        "QMS": "QMS",
        "ISO": "ISO",
        "EN": "EN",
        "YY": "YY",
        "GB": "GB",
        "IMDRF": "IMDRF",
        "MDCG": "MDCG",
        "PMCF": "PMCF",
        "PMS": "PMS",
        "PSUR": "PSUR",
        "FSCA": "FSCA",
        "FSN": "FSN",
    }

    title_upper = title.upper()
    for keyword, tag in tag_keywords.items():
        if keyword.upper() in title_upper:
            if tag not in tags:
                tags.append(tag)

    return tags


def parse_cn_regional(html: str, source_name: str, base_url: str = "") -> List[Dict]:
    """解析中国区域审评中心页面（长三角/大湾区）
    
    兼容多种布局，通用中文新闻列表页
    """
    if not html:
        return []

    items = []
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # 区域审评中心常见布局选择器
        selectors = [
            '.news-list li', '.news_list li', '.list li',
            '.article-list li', '.infolist li', '.notice-list li',
            '.main-content li', '.content li',
            'ul.list li', '.listBox li', '.listbox li',
            '.new-list li', '.newlist li',
        ]

        news_items = []
        for selector in selectors:
            news_items = soup.select(selector)
            if news_items:
                break

        # fallback: 遍历全部 <a> 标签并通过文本判断
        if not news_items:
            all_links = soup.select('a')
            for a in all_links:
                title = a.get_text(strip=True)
                if is_noise_title(title):
                    continue
                raw_url = a.get('href', '')
                url = normalize_url(raw_url, base_url)
                if not url or url == base_url:
                    continue
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": None,
                    "tags": extract_tags(title)
                })
            return items

        for li in news_items:
            link_tag = li.select_one('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            if is_noise_title(title):
                continue

            raw_url = link_tag.get('href', '')
            url = normalize_url(raw_url, base_url)

            pub_date = None
            date_tag = li.select_one('.date, .time, span, em, font')
            if date_tag:
                pub_date = parse_date(date_tag.get_text())

            if title:
                items.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "publish_date": pub_date,
                    "tags": extract_tags(title)
                })
    except Exception as e:
        print(f"  [FAIL] 解析区域审评中心失败: {e}")

    return items


# ─────────────────────────────────────────────
# web_search 兜底：供 run_tracker 调用的辅助函数
# ─────────────────────────────────────────────

# 各反爬来源对应的 web_search 查询模板
WEB_SEARCH_QUERIES = {
    "nmpa": "site:nmpa.gov.cn 医疗器械 通知 公告 指导原则 {year}年{month}月",
    "cmde_main": "site:cmde.org.cn 器械审评 最新 通知 指南 {year}年{month}月",
    "cmde_report": "site:cmde.org.cn 审评报告 {year}年{month}月",
    "cmde_faq": "site:cmde.org.cn 共性问题 解答 {year}年{month}月",
    "cmde_forum": "site:cmde.org.cn 论坛 讨论 最新 {year}年{month}月",
    "ydcmdei": "site:ydcmdei.org.cn 长三角器械审评 {year}年{month}月",
    "mdei_gba": "site:mdei.org.cn 大湾区器械审评 {year}年{month}月",
    "nifdc_standard": "site:nifdc.org.cn 器械标准 征集 发布 {year}年{month}月",
}

# 来源名称映射
SOURCE_NAMES = {
    "nmpa": "国家药品监督管理局",
    "cmde_main": "器械审评中心",
    "cmde_report": "器械审评中心-审评报告",
    "cmde_faq": "器械审评中心-共性问题",
    "cmde_forum": "器械审评中心-论坛",
    "ydcmdei": "器械审评中心（长三角）",
    "mdei_gba": "器械审评中心（大湾区）",
    "nifdc_standard": "中检院标准管理中心",
}

# 来源URL映射
SOURCE_URLS = {
    "nmpa": "https://www.nmpa.gov.cn/ylqx/index.html",
    "cmde_main": "https://www.cmde.org.cn/",
    "cmde_report": "https://www.cmde.org.cn/xwdt/shpbg/index.html",
    "cmde_faq": "https://www.cmde.org.cn/splt/ltgxwt/index.html",
    "cmde_forum": "https://www.cmde.org.cn/splt/index.html",
    "ydcmdei": "https://www.ydcmdei.org.cn/",
    "mdei_gba": "https://www.mdei.org.cn/",
    "nifdc_standard": "https://www.nifdc.org.cn/nifdc/bshff/ylqxbzhgl/index.html",
}


def get_web_search_query(source_id: str, start_date: datetime, end_date: datetime) -> str:
    """
    生成 web_search 兜底查询语句
    
    Args:
        source_id: 来源 ID
        start_date: 起始日期
        end_date: 结束日期
        
    Returns:
        查询语句字符串
    """
    template = WEB_SEARCH_QUERIES.get(source_id, "")
    if not template:
        return ""
    
    # 使用结束日期的年月（最新月份）
    year = end_date.year
    month = end_date.month
    
    return template.format(year=year, month=month)


def get_blocked_cn_sources() -> List[str]:
    """
    获取所有需要 web_search 兜底的国内来源 ID 列表
    
    Returns:
        反爬来源 ID 列表
    """
    return list(WEB_SEARCH_QUERIES.keys())


def fetch_source(source_config: Dict, start_date: datetime,
                 end_date: datetime) -> Tuple[List[Dict], str]:
    """抓取单个来源"""
    source_id = source_config.get("id", "")
    source_name = source_config.get("name", "")
    url = source_config.get("url", "")
    source_type = source_config.get("type", "static")
    parser_name = source_config.get("parser", "")

    print(f"  正在抓取: {source_name} ({source_id})")

    # web_fetch 类型来源由 run_tracker 通过 AI 工具处理，此处直接跳过
    if source_type == "web_fetch":
        print(f"    -> [web_fetch] 此来源由 AI web_fetch 工具处理，跳过直接抓取")
        return [], "web_fetch"

    use_dynamic = (source_type == "dynamic")
    html = fetch_page(url, use_dynamic=use_dynamic)

    if not html:
        return [], "failed"

    # 根据解析器类型选择解析函数，并传递 base_url
    if "cmde" in parser_name or source_id.startswith("cmde"):
        items = parse_cmde(html, source_name, url)
    elif "nmpa" in parser_name or source_id == "nmpa":
        items = parse_nmpa(html, source_name, url)
    elif "eu" in parser_name:
        items = parse_ec_health(html, source_name, url)
    elif "fda" in parser_name or source_id.startswith("fda"):
        items = parse_fda(html, source_name, url)
    elif "ca" in parser_name or source_id.startswith("ca"):
        items = parse_ca_health(html, source_name, url)
    elif "imdrf" in parser_name:
        items = parse_imdrf(html, source_name, url)
    elif "teamnb" in parser_name:
        items = parse_teamnb(html, source_name, url)
    elif source_id in ("ydcmdei", "mdei_gba"):
        # 区域审评中心
        items = parse_cn_regional(html, source_name, url)
    elif "generic" in parser_name or "cn_" in parser_name:
        # 通用中国来源解析器
        items = parse_generic_cn(html, source_name, url)
    else:
        items = parse_cmde(html, source_name, url)

    # 过滤噪音内容
    items = [item for item in items if not is_noise_title(item.get("title", ""))]
    
    items = filter_by_date_range(items, start_date, end_date)
    status = "success" if items else "partial"
    return items, status


def fetch_all_sources_with_webfetch_tracking(config: Dict, start_date: datetime,
                                             end_date: datetime) -> Tuple[List[Dict], List[Dict]]:
    """
    抓取所有来源，并追踪需要 AI web_fetch 工具处理的来源。

    Returns:
        (all_items, web_fetch_sources): 普通抓取的条目列表 + 需要AI工具处理的来源列表
    """
    all_items = []
    web_fetch_sources = []  # 需要 AI web_fetch 工具处理的来源
    regions = config.get("regions", {})

    for region_code, region_info in regions.items():
        region_name = region_info.get("name", region_code)
        sources = region_info.get("sources", [])

        print(f"\n[NET] {region_name}:")

        for source in sources:
            try:
                items, status = fetch_source(source, start_date, end_date)

                # 标记 web_fetch 来源，加入待补抓清单
                if status == "web_fetch":
                    source_with_region = dict(source)
                    source_with_region["region"] = region_code
                    web_fetch_sources.append(source_with_region)
                    print(f"    -> [⚠️ 需AI补抓] {source.get('name')} ({source.get('id')})")
                    continue

                for item in items:
                    item["region"] = region_code

                all_items.extend(items)
                print(f"    -> 获取 {len(items)} 条")
                time.sleep(1)

            except Exception as e:
                print(f"    [FAIL] 抓取失败: {e}")

    return all_items, web_fetch_sources


def fetch_all_sources(config: Dict, start_date: datetime,
                      end_date: datetime) -> List[Dict]:
    """抓取所有来源（兼容旧接口，内部委托给新函数）"""
    items, _ = fetch_all_sources_with_webfetch_tracking(config, start_date, end_date)
    return items


if __name__ == "__main__":
    from .date_utils import get_week_date_range

    start, end = get_week_date_range()
    print(f"测试日期范围: {start} ~ {end}")

    test_dates = ["2026-04-12", "2026/04/12", "2026年04月12日", "Apr 12, 2026"]
    print("\n日期解析测试:")
    for d in test_dates:
        result = parse_date(d)
        print(f"  '{d}' -> {result}")

    print("\n标签提取测试:")
    test_titles = [
        "关于公开征求《医疗器械产品技术要求编写指导原则（修订版征求意见稿）》意见的通知",
        "MDR Article 83 - PMS Plan Technical Documentation Updated",
        "FDA 510(k) Substantial Equivalence Guide"
    ]
    for t in test_titles:
        tags = extract_tags(t)
        print(f"  '{t[:30]}...' -> {tags}")
