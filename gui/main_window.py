#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
النافذة الرئيسية لأداة SaudiHack
"""

import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTextEdit, QLineEdit, 
                             QProgressBar, QTabWidget, QTableWidget, QTableWidgetItem,
                             QFileDialog, QMessageBox, QComboBox, QSpinBox,
                             QCheckBox, QGroupBox, QSplitter, QTextBrowser, QFormLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QBrush, QColor, QLinearGradient
from core.vulnerability_scanner import VulnerabilityScanner
from utils.logger import setup_logger
from utils.report_generator import ReportGenerator

class ScanThread(QThread):
    """خيط منفصل للبحث عن الثغرات"""
    progress_updated = pyqtSignal(int)
    result_found = pyqtSignal(dict)
    scan_finished = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, target, scan_type="full"):
        super().__init__()
        self.target = target
        self.scan_type = scan_type
        self.scanner = VulnerabilityScanner()
        
    def run(self):
        try:
            results = self.scanner.scan_target(self.target, self.scan_type)
            self.scan_finished.emit(results)
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self):
        super().__init__()
        self.logger = setup_logger()
        self.scan_thread = None
        self.results = []
        self.init_ui()
        
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle('SaudiHack - أداة البحث عن الثغرات الأمنية')
        self.setGeometry(100, 100, 1200, 800)
        
        # تعيين أيقونة النافذة
        icon = QIcon('images/saudihack_logo.svg')
        self.setWindowIcon(icon)
        
        # إنشاء الخلفية المتدرجة
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QPushButton {
                background-color: #89b4fa;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #74c7ec;
            }
            QPushButton:pressed {
                background-color: #6c9ded;
            }
            QLineEdit {
                background-color: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QTextEdit, QTextBrowser {
                background-color: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 5px;
                font-family: 'Consolas', monospace;
            }
            QTableWidget {
                background-color: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 5px;
                gridline-color: #45475a;
            }
            QHeaderView::section {
                background-color: #45475a;
                color: #cdd6f4;
                padding: 5px;
                border: 1px solid #6c7086;
            }
            QProgressBar {
                background-color: #313244;
                border: 2px solid #45475a;
                border-radius: 5px;
                text-align: center;
                color: #cdd6f4;
            }
            QProgressBar::chunk {
                background-color: #a6e3a1;
                border-radius: 3px;
            }
            QLabel {
                color: #cdd6f4;
                font-size: 14px;
            }
            QComboBox {
                background-color: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 5px;
                padding: 5px;
            }
            QGroupBox {
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # إنشاء القائمة الرئيسية
        self.create_menu()
        
        # إنشاء القسم المركزي
        self.create_central_widget()
        
        # إنشاء شريط الحالة
        self.create_status_bar()
        
        self.logger.info("تم تهيئة واجهة المستخدم بنجاح")
        
    def create_menu(self):
        """إنشاء القائمة الرئيسية"""
        menubar = self.menuBar()
        
        # قائمة الملف
        file_menu = menubar.addMenu('ملف')
        
        # إجراءات القائمة
        save_action = file_menu.addAction('حفظ النتائج')
        save_action.triggered.connect(self.save_results)
        
        export_action = file_menu.addAction('تصدير التقرير')
        export_action.triggered.connect(self.export_report)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('خروج')
        exit_action.triggered.connect(self.close)
        
        # قائمة المساعدة
        help_menu = menubar.addMenu('مساعدة')
        
        about_action = help_menu.addAction('حول')
        about_action.triggered.connect(self.show_about)
        
    def create_central_widget(self):
        """إنشاء القسم المركزي"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # إنشاء التبويبات
        self.create_tabs(main_layout)
        
    def create_tabs(self, main_layout):
        """إنشاء التبويبات"""
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # تبويب الفحص
        self.scan_tab = self.create_scan_tab()
        self.tabs.addTab(self.scan_tab, "فحص الثغرات")
        
        # تبويب مسح قواعد البيانات
        self.database_tab = self.create_database_tab()
        self.tabs.addTab(self.database_tab, "مسح قواعد البيانات")
        
        # تبويب معلومات المبرمج
        self.about_tab = self.create_about_tab()
        self.tabs.addTab(self.about_tab, "عن المبرمج")
        
        # تبويب النتائج
        self.results_tab = self.create_results_tab()
        self.tabs.addTab(self.results_tab, "النتائج")
        
        # تبويب التقارير
        self.reports_tab = self.create_reports_tab()
        self.tabs.addTab(self.reports_tab, "التقارير")
        
    def create_scan_tab(self):
        """إنشاء تبويب الفحص"""
        scan_widget = QWidget()
        layout = QVBoxLayout()
        scan_widget.setLayout(layout)
        
        # عنوان
        title = QLabel("SaudiHack - أداة البحث عن الثغرات الأمنية")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #89b4fa; margin: 20px;")
        layout.addWidget(title)
        
        # مجموعة إعدادات الفحص
        scan_group = QGroupBox("إعدادات الفحص")
        scan_layout = QVBoxLayout()
        scan_group.setLayout(scan_layout)
        
        # حقل إدخال الهدف
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("الهدف:"))
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("أدخل عنوان الموقع أو النطاق...")
        target_layout.addWidget(self.target_input)
        scan_layout.addLayout(target_layout)
        
        # نوع الفحص
        scan_type_layout = QHBoxLayout()
        scan_type_layout.addWidget(QLabel("نوع الفحص:"))
        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems([
            "فحص شامل",
            "فحص سريع",
            "فحص XSS",
            "فحص SQL Injection",
            "فحص ملفات التكوين",
            "فحص البورتات"
        ])
        scan_type_layout.addWidget(self.scan_type_combo)
        scan_layout.addLayout(scan_type_layout)
        
        layout.addWidget(scan_group)
        
        # أزرار التحكم
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("بدء الفحص")
        self.start_button.clicked.connect(self.start_scan)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("إيقاف")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_scan)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)
        
        # شريط التقدم
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # منطقة عرض النتائج الحية
        self.log_display = QTextBrowser()
        self.log_display.setMaximumHeight(200)
        layout.addWidget(self.log_display)
        
        return scan_widget
        
    def create_results_tab(self):
        """إنشاء تبويب النتائج"""
        results_widget = QWidget()
        layout = QVBoxLayout()
        results_widget.setLayout(layout)
        
        # جدول النتائج
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "الثغرة", "الخطورة", "الوصف", "الهدف", "الحالة", "الإجراء"
        ])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.results_table)
        
        # أزرار التحكم بالنتائج
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton("تحديث")
        refresh_button.clicked.connect(self.refresh_results)
        button_layout.addWidget(refresh_button)
        
        export_button = QPushButton("تصدير")
        export_button.clicked.connect(self.export_results)
        button_layout.addWidget(export_button)
        
        layout.addLayout(button_layout)
        
        return results_widget

    def create_about_tab(self):
        """إنشاء تبويب معلومات المبرمج"""
        about_tab = QWidget()
        layout = QVBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap('images/saudihack_logo.svg')
        logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel('SaudiHack')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""QLabel {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin: 10px 0;
        }""")
        
        # Description
        desc_label = QLabel('أداة متقدمة للبحث عن الثغرات الأمنية في المواقع السعودية')
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("""QLabel {
            font-size: 14px;
            color: #7f8c8d;
            margin-bottom: 20px;
        }""")
        
        # Developer info
        dev_group = QGroupBox('معلومات المبرمج')
        dev_group.setStyleSheet("""QGroupBox {
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            border: 2px solid #3498db;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }""")
        
        dev_layout = QFormLayout()
        
        name_label = QLabel('الاسم:')
        name_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        name_value = QLabel('SayerLinux')
        name_value.setStyleSheet("color: #34495e;")
        
        website_label = QLabel('الموقع:')
        website_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        website_value = QLabel('<a href="https://github.com/SaudiLinux/">https://github.com/SaudiLinux/</a>')
        website_value.setOpenExternalLinks(True)
        website_value.setStyleSheet("color: #3498db;")
        
        email_label = QLabel('البريد:')
        email_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        email_value = QLabel('<a href="mailto:SayerLinux1@gmail.com">SayerLinux1@gmail.com</a>')
        email_value.setOpenExternalLinks(True)
        email_value.setStyleSheet("color: #3498db;")
        
        dev_layout.addRow(name_label, name_value)
        dev_layout.addRow(website_label, website_value)
        dev_layout.addRow(email_label, email_value)
        
        dev_group.setLayout(dev_layout)
        
        # Version info
        version_label = QLabel('الإصدار: 1.0.0')
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("""QLabel {
            font-size: 12px;
            color: #95a5a6;
            margin-top: 20px;
        }""")
        
        layout.addStretch()
        layout.addWidget(logo_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addWidget(dev_group)
        layout.addWidget(version_label)
        layout.addStretch()
        
        about_tab.setLayout(layout)
        return about_tab
        
    def create_database_tab(self):
        """إنشاء تبويب مسح قواعد البيانات"""
        database_widget = QWidget()
        layout = QVBoxLayout()
        database_widget.setLayout(layout)
        
        # مجموعة إدخال الأهداف
        target_group = QGroupBox("أهداف المسح")
        target_layout = QVBoxLayout()
        
        self.db_target_input = QTextEdit()
        self.db_target_input.setPlaceholderText("أدخل عناوين IP أو أسماء النطاقات (سطر لكل هدف)...")
        self.db_target_input.setMaximumHeight(100)
        target_layout.addWidget(self.db_target_input)
        
        target_group.setLayout(target_layout)
        layout.addWidget(target_group)
        
        # مجموعة خيارات المسح
        options_group = QGroupBox("خيارات المسح")
        options_layout = QVBoxLayout()
        
        # اختيار أنواع قواعد البيانات
        db_types_layout = QHBoxLayout()
        self.mysql_check = QCheckBox("MySQL")
        self.mysql_check.setChecked(True)
        self.postgresql_check = QCheckBox("PostgreSQL")
        self.postgresql_check.setChecked(True)
        self.mssql_check = QCheckBox("MSSQL")
        self.mssql_check.setChecked(True)
        self.oracle_check = QCheckBox("Oracle")
        self.oracle_check.setChecked(True)
        self.sqlite_check = QCheckBox("SQLite")
        
        db_types_layout.addWidget(self.mysql_check)
        db_types_layout.addWidget(self.postgresql_check)
        db_types_layout.addWidget(self.mssql_check)
        db_types_layout.addWidget(self.oracle_check)
        db_types_layout.addWidget(self.sqlite_check)
        options_layout.addLayout(db_types_layout)
        
        # خيار اختبار كلمات المرور الافتراضية
        self.brute_force_check = QCheckBox("اختبار كلمات المرور الافتراضية")
        self.brute_force_check.setChecked(True)
        options_layout.addWidget(self.brute_force_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # أزرار التحكم
        control_layout = QHBoxLayout()
        
        self.start_db_scan = QPushButton("بدء المسح")
        self.start_db_scan.clicked.connect(self.start_database_scan)
        control_layout.addWidget(self.start_db_scan)
        
        self.stop_db_scan = QPushButton("إيقاف المسح")
        self.stop_db_scan.setEnabled(False)
        self.stop_db_scan.clicked.connect(self.stop_database_scan)
        control_layout.addWidget(self.stop_db_scan)
        
        self.save_db_report = QPushButton("حفظ التقرير")
        self.save_db_report.clicked.connect(self.save_database_report)
        control_layout.addWidget(self.save_db_report)
        
        layout.addLayout(control_layout)
        
        # شريط التقدم
        self.db_progress = QProgressBar()
        layout.addWidget(self.db_progress)
        
        # منطقة عرض النتائج
        self.db_results_table = QTableWidget()
        self.db_results_table.setColumnCount(5)
        self.db_results_table.setHorizontalHeaderLabels([
            "الهدف", "نوع قاعدة البيانات", "المنفذ", "الحالة", "بيانات الاعتماد"
        ])
        self.db_results_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.db_results_table)
        
        # منطقة السجلات
        self.db_log_display = QTextEdit()
        self.db_log_display.setMaximumHeight(150)
        self.db_log_display.setReadOnly(True)
        layout.addWidget(self.db_log_display)
        
        return database_widget

    def create_reports_tab(self):
        """إنشاء تبويب التقارير"""
        reports_widget = QWidget()
        layout = QVBoxLayout()
        reports_widget.setLayout(layout)
        
        # منطقة عرض التقرير
        self.report_display = QTextBrowser()
        layout.addWidget(self.report_display)
        
        # أزرار التحكم
        button_layout = QHBoxLayout()
        
        generate_button = QPushButton("إنشاء تقرير")
        generate_button.clicked.connect(self.generate_report)
        button_layout.addWidget(generate_button)
        
        save_report_button = QPushButton("حفظ التقرير")
        save_report_button.clicked.connect(self.save_report)
        button_layout.addWidget(save_report_button)
        
        layout.addLayout(button_layout)
        
        return reports_widget
        
    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("جاهز")
        
    def start_scan(self):
        """بدء عملية الفحص"""
        target = self.target_input.text().strip()
        if not target:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال هدف للفحص")
            return
            
        scan_type = self.scan_type_combo.currentText()
        
        # تعطيل الزر وتفعيل إيقاف
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        
        # إنشاء خيط الفحص
        self.scan_thread = ScanThread(target, scan_type)
        self.scan_thread.progress_updated.connect(self.update_progress)
        self.scan_thread.result_found.connect(self.add_result)
        self.scan_thread.scan_finished.connect(self.scan_completed)
        self.scan_thread.error_occurred.connect(self.scan_error)
        
        self.scan_thread.start()
        
        self.status_bar.showMessage(f"جاري فحص {target}...")
        self.log_display.append(f"بدء فحص: {target}")
        
    def stop_scan(self):
        """إيقاف الفحص"""
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.terminate()
            self.scan_completed([])
            
    def update_progress(self, value):
        """تحديث شريط التقدم"""
        self.progress_bar.setValue(value)
        
    def add_result(self, result):
        """إضافة نتيجة جديدة"""
        self.results.append(result)
        self.update_results_table()
        
    def scan_completed(self, results):
        """اكتمال الفحص"""
        self.results = results
        self.update_results_table()
        
        # إعادة تفعيل الأزرار
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        self.status_bar.showMessage("اكتمل الفحص")
        self.log_display.append("اكتمل الفحص بنجاح")
        
    def scan_error(self, error):
        """معالجة الخطأ"""
        QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الفحص:\n{error}")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
    def update_results_table(self):
        """تحديث جدول النتائج"""
        self.results_table.setRowCount(len(self.results))
        
        for row, result in enumerate(self.results):
            self.results_table.setItem(row, 0, QTableWidgetItem(result.get('vulnerability', '')))
            self.results_table.setItem(row, 1, QTableWidgetItem(result.get('severity', '')))
            self.results_table.setItem(row, 2, QTableWidgetItem(result.get('description', '')))
            self.results_table.setItem(row, 3, QTableWidgetItem(result.get('target', '')))
            self.results_table.setItem(row, 4, QTableWidgetItem(result.get('status', '')))
            self.results_table.setItem(row, 5, QTableWidgetItem(result.get('action', '')))
            
    def save_results(self):
        """حفظ النتائج"""
        file_path, _ = QFileDialog.getSaveFileName(self, "حفظ النتائج", "", "JSON Files (*.json)")
        if file_path:
            from utils.file_handler import save_json
            save_json(self.results, file_path)
            QMessageBox.information(self, "نجاح", "تم حفظ النتائج بنجاح")
            
    def export_report(self):
        """تصدير التقرير"""
        file_path, _ = QFileDialog.getSaveFileName(self, "تصدير التقرير", "", "PDF Files (*.pdf)")
        if file_path:
            generator = ReportGenerator()
            generator.generate_pdf_report(self.results, file_path)
            QMessageBox.information(self, "نجاح", "تم تصدير التقرير بنجاح")
            
    def refresh_results(self):
        """تحديث النتائج"""
        self.update_results_table()
        
    def export_results(self):
        """تصدير النتائج"""
        self.export_report()
        
    def generate_report(self):
        """إنشاء تقرير"""
        if not self.results:
            QMessageBox.warning(self, "تحذير", "لا توجد نتائج لإنشاء تقرير")
            return
            
        generator = ReportGenerator()
        report = generator.generate_html_report(self.results)
        self.report_display.setHtml(report)
        
    def save_report(self):
        """حفظ التقرير"""
        file_path, _ = QFileDialog.getSaveFileName(self, "حفظ التقرير", "", "HTML Files (*.html)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.report_display.toHtml())
            QMessageBox.information(self, "نجاح", "تم حفظ التقرير بنجاح")
            
    def start_database_scan(self):
        """بدء مسح قواعد البيانات"""
        targets_text = self.db_target_input.toPlainText().strip()
        if not targets_text:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال أهداف للمسح")
            return
            
        targets = [t.strip() for t in targets_text.split('\n') if t.strip()]
        
        # تعطيل الزر وتفعيل إيقاف
        self.start_db_scan.setEnabled(False)
        self.stop_db_scan.setEnabled(True)
        self.db_progress.setValue(0)
        
        # مسح في خيط منفصل
        from core.database_scanner import DatabaseScanner
        self.db_scanner = DatabaseScanner()
        
        def scan_thread():
            try:
                self.db_log_display.append("بدء مسح قواعد البيانات...")
                results = self.db_scanner.comprehensive_database_scan(targets)
                
                # تحديث الجدول بالنتائج
                self.update_database_results(results)
                
                self.db_log_display.append("اكتمل مسح قواعد البيانات")
                
            except Exception as e:
                self.db_log_display.append(f"خطأ في المسح: {str(e)}")
            finally:
                self.start_db_scan.setEnabled(True)
                self.stop_db_scan.setEnabled(False)
        
        import threading
        thread = threading.Thread(target=scan_thread)
        thread.daemon = True
        thread.start()
        
    def stop_database_scan(self):
        """إيقاف مسح قواعد البيانات"""
        # سيتم التعامل مع الإيقاف في الإصدار المستقبل
        self.start_db_scan.setEnabled(True)
        self.stop_db_scan.setEnabled(False)
        self.db_log_display.append("تم إيقاف المسح")
        
    def update_database_results(self, results):
        """تحديث جدول نتائج قواعد البيانات"""
        self.db_results_table.setRowCount(0)
        
        for target_result in results:
            target = target_result['target']
            
            for service in target_result['open_services']:
                row = self.db_results_table.rowCount()
                self.db_results_table.insertRow(row)
                
                self.db_results_table.setItem(row, 0, QTableWidgetItem(target))
                self.db_results_table.setItem(row, 1, QTableWidgetItem(service['type']))
                self.db_results_table.setItem(row, 2, QTableWidgetItem(str(service['port'])))
                self.db_results_table.setItem(row, 3, QTableWidgetItem(service['status']))
                
                creds = service.get('credentials_found', [])
                if creds:
                    cred_text = f"تم العثور على {len(creds)} بيانات اعتماد"
                else:
                    cred_text = "لا توجد بيانات اعتماد"
                self.db_results_table.setItem(row, 4, QTableWidgetItem(cred_text))
                
    def save_database_report(self):
        """حفظ تقرير مسح قواعد البيانات"""
        file_path, _ = QFileDialog.getSaveFileName(self, "حفظ تقرير قواعد البيانات", "", "JSON Files (*.json)")
        if file_path and hasattr(self, 'db_scanner'):
            self.db_scanner.save_report(file_path)
            QMessageBox.information(self, "نجاح", "تم حفظ تقرير قواعد البيانات بنجاح")

    def show_about(self):
        """عرض نافذة حول"""
        about_text = """
        <h2>SaudiHack - أداة البحث عن الثغرات الأمنية</h2>
        <p><strong>الإصدار:</strong> 1.0.0</p>
        <p><strong>المبرمج:</strong> SayerLinux</p>
        <p><strong>الموقع:</strong> <a href="https://github.com/SaudiLinux/">https://github.com/SaudiLinux/</a></p>
        <p><strong>الايميل:</strong> SayerLinux1@gmail.com</p>
        <p><strong>الوصف:</strong> أداة متخصصة في البحث عن الثغرات الأمنية في المواقع السعودية</p>
        """
        QMessageBox.about(self, "حول SaudiHack", about_text)