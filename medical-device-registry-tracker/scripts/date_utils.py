#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日期工具模块 - 处理北京时间时区和日期范围计算
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Tuple


# 北京时区
BEIJING_TZ = ZoneInfo("Asia/Shanghai")


def get_beijing_now() -> datetime:
    """获取当前北京时间"""
    return datetime.now(BEIJING_TZ)


def get_week_date_range(reference_date: datetime = None) -> Tuple[datetime, datetime]:
    """
    获取日期范围：上周五到本周五（北京时间）

    Args:
        reference_date: 参考日期，默认为当前北京时间

    Returns:
        (start_date, end_date): 上周五00:00:00 到 本周五23:59:59
    """
    if reference_date is None:
        now = get_beijing_now()
    else:
        now = reference_date.astimezone(BEIJING_TZ)

    # 找到当前周的周五
    # weekday(): Monday=0, Sunday=6
    # Friday=4
    current_weekday = now.weekday()
    days_since_friday = (current_weekday - 4) % 7

    # 本周五
    this_friday = now - timedelta(days=days_since_friday)
    this_friday = this_friday.replace(hour=23, minute=59, second=59, microsecond=999999)

    # 上周五
    last_friday = this_friday - timedelta(days=7)
    last_friday = last_friday.replace(hour=0, minute=0, second=0, microsecond=0)

    return last_friday, this_friday


def is_within_date_range(date_str: str, start_date: datetime, end_date: datetime,
                          date_format: str = "%Y-%m-%d") -> bool:
    """
    检查日期字符串是否在指定范围内

    Args:
        date_str: 日期字符串
        start_date: 范围开始
        end_date: 范围结束
        date_format: 日期格式

    Returns:
        True if within range
    """
    try:
        # 尝试多种日期格式
        formats = [
            date_format,
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y年%m月%d日",
        ]

        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str.strip(), fmt)
                parsed_date = parsed_date.replace(tzinfo=BEIJING_TZ)
                return start_date <= parsed_date <= end_date
            except ValueError:
                continue

        # 如果无法解析，尝试提取日期部分
        import re
        date_pattern = r'(\d{4})[/-]?(\d{1,2})[/-]?(\d{1,2})'
        match = re.search(date_pattern, date_str)
        if match:
            year, month, day = match.groups()
            parsed_date = datetime(int(year), int(month), int(day), tzinfo=BEIJING_TZ)
            return start_date <= parsed_date <= end_date

        return False

    except Exception:
        return False


def format_date_beijing(dt: datetime) -> str:
    """格式化日期为中文格式"""
    return dt.strftime("%Y年%m月%d日 %H:%M")


def format_date_short(dt: datetime) -> str:
    """格式化日期为短格式"""
    return dt.strftime("%Y-%m-%d")


def get_report_title(start_date: datetime, end_date: datetime) -> str:
    """生成报告标题"""
    gen_date = datetime.now().strftime('%Y%m%d')
    return f"医疗器械法规更新汇总 ({format_date_short(start_date)}~{format_date_short(end_date)}，生成于{gen_date})"
