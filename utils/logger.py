#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام تسجيل الأحداث للأداة
"""

import logging
import os
from datetime import datetime

def setup_logger(name='SaudiHack'):
    """إعداد نظام تسجيل الأحداث"""
    
    # إنشاء مجلد السجلات إذا لم يكن موجوداً
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # إنشاء ملف السجل
    log_file = os.path.join(log_dir, f'saudihack_{datetime.now().strftime("%Y%m%d")}.log')
    
    # إعداد المسجل
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # منع التكرار
    if logger.handlers:
        return logger
    
    # معالج للملف
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # معالج للواجهة
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # تنسيق الرسائل
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger