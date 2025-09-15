#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة SaudiHack للبحث عن الثغرات الأمنية في المواقع السعودية
المبرمج: SayerLinux
الموقع: https://github.com/SaudiLinux/
الايميل: SayerLinux1@gmail.com
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from core.vulnerability_scanner import VulnerabilityScanner
from utils.logger import setup_logger

def main():
    """الدالة الرئيسية لتشغيل الأداة"""
    
    # إعداد السجل
    logger = setup_logger()
    logger.info("بدء تشغيل أداة SaudiHack")
    
    # إنشاء تطبيق PyQt
    app = QApplication(sys.argv)
    app.setApplicationName("SaudiHack")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SaudiLinux")
    
    # إنشاء النافذة الرئيسية
    window = MainWindow()
    window.show()
    
    logger.info("تم تشغيل واجهة المستخدم بنجاح")
    
    # تشغيل التطبيق
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())