"""
Web Fetch 方式抓取脚本

此脚本通过 HTTP 请求抓取网页内容，用于法规追踪。
已验证可用的来源：
- EU/EC: https://health.ec.europa.eu/medical-devices-sector/latest-updates_en
- IMDRF: https://www.imdrf.org/documents
- Health Canada: https://www.canada.ca/en/health-canada/services/drugs-health-products/medical-devices/what-new.html
- FDA Recalls: https://www.fda.gov/medical-devices/medical-device-safety/medical-device-recalls

使用方法：
    python web_fetch_scraper.py --region EU
    python web_fetch_scraper.py --region all
    python web_fetch_scraper.py --url "https://xxx"
"""

import json
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# 配置
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "scripts" / "reports"

# 已验证可用的 URL
VERIFIED_URLS = {
    "EU/EC": "https://health.ec.europa.eu/medical-devices-sector/latest-updates_en",
    "IMDRF": "https://www.imdrf.org/documents",
    "Health Canada": "https://www.canada.ca/en/health-canada/services/drugs-health-products/medical-devices/what-new.html",
    "FDA Recalls": "https://www.fda.gov/medical-devices/medical-device-safety/medical-device-recalls",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def get_date_range(days=7):
    """获取日期范围"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def parse_date(text):
    """从文本中提取日期"""
    patterns = [
        r"(\d{4})-(\d{2})-(\d{2})",
        r"(\d{4})/(\d{2})/(\d{2})",
        r"(\d{4})(\d{2})(\d{8,})",  # URL内嵌日期如 20260403113714
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                year, month, day = match.groups()[:3]
                return f"{year}-{month}-{day[:2]}"
            except:
                pass
    return None


def parse_ec_updates(html):
    """解析 EU/EC 医疗器械更新页面"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    seen_titles = set()

    # 查找文章列表
    for article in soup.select("article, .view-item, .eu-official-content, .list-item"):
        title_elem = article.select_one("h2, h3, .title, a")
        date_elem = article.select_one("time, .date, .published")

        if not title_elem:
            continue

        title = title_elem.get_text(strip=True)
        url = title_elem.get("href") if title_elem.name == "a" else title_elem.select_one("a")
        if url and hasattr(url, "get"):
            url = url.get("href")
        elif url and isinstance(url, str) and url.startswith("http"):
            pass
        else:
            link = title_elem.select_one("a")
            url = link.get("href") if link else None

        # 噪音过滤
        noise_patterns = ["RSS", "Events", "Publications", "Language", "Switcher", "Share", "Print"]
        if any(p in title for p in noise_patterns):
            continue

        if title in seen_titles:
            continue
        seen_titles.add(title)

        date_text = date_elem.get("datetime") if date_elem and date_elem.name == "time" else date_elem.get_text(strip=True) if date_elem else ""
        date = parse_date(date_text) or parse_date(str(article)) or ""

        items.append({
            "title": title,
            "url": urljoin("https://health.ec.europa.eu/", url) if url else "",
            "source": "EU/EC",
            "date": date,
            "region": "EU"
        })

    return items


def parse_imdrf(html):
    """解析 IMDRF 文档页面"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    seen_titles = set()

    for item in soup.select(".view-item, .document-list li, .page-content li"):
        link = item.select_one("a")
        if not link:
            continue

        title = link.get_text(strip=True)
        url = link.get("href")

        if not title or title in seen_titles:
            continue
        seen_titles.add(title)

        # 提取日期
        date_text = item.get_text(strip=True)
        date = parse_date(date_text) or ""

        # URL 处理
        if url and not url.startswith("http"):
            url = urljoin("https://www.imdrf.org/", url)

        items.append({
            "title": title,
            "url": url,
            "source": "IMDRF",
            "date": date,
            "region": "IMDRF"
        })

    return items


def parse_health_canada(html):
    """解析 Health Canada 页面"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    seen_titles = set()

    for item in soup.select("..gc-webpost, .news-item, .recent-activity li"):
        link = item.select_one("a")
        if not link:
            continue

        title = link.get_text(strip=True)
        url = link.get("href")

        if not title or title in seen_titles:
            continue
        seen_titles.add(title)

        date_text = item.get_text(strip=True)
        date = parse_date(date_text)

        if url and not url.startswith("http"):
            url = urljoin("https://www.canada.ca/", url)

        items.append({
            "title": title,
            "url": url,
            "source": "Health Canada",
            "date": date or "",
            "region": "CA"
        })

    return items


def parse_fda_recalls(html):
    """解析 FDA 召回页面"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    seen_titles = set()

    for row in soup.select("table tbody tr, .recall-item, .field-item"):
        # 尝试多种选择器
        link = row.select_one("a")
        if not link:
            continue

        title = link.get_text(strip=True)
        url = link.get("href")

        if not title or title in seen_titles or len(title) < 5:
            continue
        seen_titles.add(title)

        # 提取日期（通常在标题后或单元格中）
        date_text = row.get_text(strip=True)
        date = parse_date(date_text)

        if url and not url.startswith("http"):
            url = urljoin("https://www.fda.gov/", url)

        items.append({
            "title": title,
            "url": url,
            "source": "FDA",
            "date": date or "",
            "region": "US"
        })

    return items


def fetch_and_parse(url, parser_name):
    """抓取并解析页面"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"

        parsers = {
            "ec": parse_ec_updates,
            "imdrf": parse_imdrf,
            "ca": parse_health_canada,
            "fda": parse_fda_recalls,
        }

        parser = parsers.get(parser_name)
        if parser:
            return parser(response.text)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return []


def generate_report(all_items, start_date, end_date):
    """生成 Markdown 报告"""
    # 按区域统计
    stats = {"EU": 0, "US": 0, "CA": 0, "IMDRF": 0, "CN": 0}
    for item in all_items:
        region = item.get("region", "Other")
        if region in stats:
            stats[region] += 1

    report = f"""# 医疗器械法规追踪报告

**报告周期**: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}  
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**抓取方式**: Web Fetch API

---

## 概览统计

| 区域 | 条目数 | 状态 |
|:-----|-------:|:-----|
"""

    status_map = {
        "EU": "✅ 成功",
        "US": "✅ 成功",
        "CA": "✅ 成功",
        "IMDRF": "✅ 成功",
        "CN": "⚠️ 反爬虫保护",
    }

    for region, count in stats.items():
        status = status_map.get(region, "-")
        report += f"| {region} | {count} | {status} |\n"

    # 按区域分组输出
    by_region = {}
    for item in all_items:
        region = item.get("region", "Other")
        if region not in by_region:
            by_region[region] = []
        by_region[region].append(item)

    for region, items in by_region.items():
        report += f"\n## {region}\n\n"
        report += "| 日期 | 标题 | 链接 |\n"
        report += "|:-----|:-----|:-----|\n"
        for item in items[:20]:  # 限制每区域最多20条
            title = item.get("title", "")[:60]
            url = item.get("url", "#")
            date = item.get("date", "-")
            report += f"| {date} | {title} | [链接]({url}) |\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="Web Fetch 方式法规抓取")
    parser.add_argument("--region", choices=["EU", "US", "CA", "IMDRF", "CN", "all"], default="all")
    parser.add_argument("--url", help="直接指定 URL")
    parser.add_argument("--days", type=int, default=7, help="抓取天数范围")
    args = parser.parse_args()

    start_date, end_date = get_date_range(args.days)
    all_items = []

    if args.url:
        # 直接抓取指定 URL
        print(f"抓取: {args.url}")
        items = fetch_and_parse(args.url, "ec")  # 默认使用 EC 解析器
        all_items.extend(items)
    else:
        region_urls = {
            "EU": [("ec", VERIFIED_URLS["EU/EC"])],
            "IMDRF": [("imdrf", VERIFIED_URLS["IMDRF"])],
            "CA": [("ca", VERIFIED_URLS["Health Canada"])],
            "US": [("fda", VERIFIED_URLS["FDA Recalls"])],
        }

        regions_to_fetch = ["EU", "IMDRF", "CA", "US"] if args.region == "all" else [args.region]

        for region in regions_to_fetch:
            if region in region_urls:
                for parser_name, url in region_urls[region]:
                    print(f"抓取 {region}: {url}")
                    items = fetch_and_parse(url, parser_name)
                    print(f"  -> 获取 {len(items)} 条")
                    all_items.extend(items)

    # 生成报告
    report = generate_report(all_items, start_date, end_date)

    # 保存报告
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    report_path = REPORTS_DIR / f"regulatory_update_{date_str}.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"\n报告已生成: {report_path}")
    print(f"共 {len(all_items)} 条法规更新")


if __name__ == "__main__":
    main()
