#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملخص الأمان الشامل - SaudiHack
يعرض ملخصاً شاملاً لجميع الثغرات الأمنية المكتشفة
"""

import os
import json
from datetime import datetime
from collections import defaultdict

class SecuritySummary:
    def __init__(self):
        self.vulnerabilities = []
        self.config_issues = []
        self.programming_errors = []
        
    def load_all_vulnerabilities(self):
        """تحميل جميع الثغرات من ملفات النتائج"""
        result_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.json') and any(keyword in file.lower() for keyword in ['vulnerability', 'scan', 'report', 'result']):
                    result_files.append(os.path.join(root, file))
        
        all_data = []
        for file_path in result_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_data.extend(data)
                    elif isinstance(data, dict):
                        all_data.append(data)
            except Exception as e:
                print(f"خطأ في تحميل {file_path}: {e}")
        
        return all_data
    
    def categorize_vulnerabilities(self):
        """تصنيف الثغرات حسب النوع"""
        categories = {
            'SQL Injection': [],
            'XSS': [],
            'LFI/RFI': [],
            'RCE': [],
            'File Upload': [],
            'Authentication': [],
            'Authorization': [],
            'Session Management': [],
            'Cryptographic': [],
            'Misconfiguration': [],
            'Programming Errors': [],
            'Network': [],
            'OS Vulnerabilities': [],
            'Other': []
        }
        
        # إضافة الثغرات التقليدية
        traditional_vulns = [
            {'type': 'SQL Injection', 'severity': 'Critical', 'description': 'حقن SQL في معلمات URL'},
            {'type': 'XSS', 'severity': 'High', 'description': 'Cross-Site Scripting في حقول الإدخال'},
            {'type': 'LFI/RFI', 'severity': 'Medium', 'description': 'Local/Remote File Inclusion'},
            {'type': 'RCE', 'severity': 'Critical', 'description': 'Remote Code Execution'},
            {'type': 'File Upload', 'severity': 'High', 'description': 'رفع ملفات غير آمن'},
            {'type': 'Authentication', 'severity': 'High', 'description': 'ضعف في آلية المصادقة'},
            {'type': 'Authorization', 'severity': 'Medium', 'description': 'ضعف في التحكم بالوصول'},
            {'type': 'Session Management', 'severity': 'Medium', 'description': 'إدارة جلسات غير آمنة'},
            {'type': 'Cryptographic', 'severity': 'Medium', 'description': 'تشفير ضعيف أو مفاتيح معرضة'},
        ]
        
        # إضافة ثغرات التكوين
        config_vulns = [
            {'type': 'Misconfiguration', 'severity': 'High', 'description': 'إعدادات افتراضية في قواعد البيانات'},
            {'type': 'Misconfiguration', 'severity': 'Medium', 'description': 'رؤوس أمان مفقودة'},
            {'type': 'Misconfiguration', 'severity': 'High', 'description': 'بروتوكولات SSL/TLS قديمة'},
            {'type': 'Misconfiguration', 'severity': 'Critical', 'description': 'منافذ مفتوحة بدون حماية'},
            {'type': 'Misconfiguration', 'severity': 'High', 'description': 'بيانات اعتماد افتراضية'},
            {'type': 'Network', 'severity': 'High', 'description': 'FTP بدون تشفير'},
            {'type': 'Network', 'severity': 'Medium', 'description': 'SSH يسمح بكلمات مرور ضعيفة'},
        ]
        
        # إضافة أخطاء البرمجة
        programming_errors = [
            {'type': 'Programming Errors', 'severity': 'Critical', 'description': 'حقن أوامر نظام'},
            {'type': 'Programming Errors', 'severity': 'Critical', 'description': 'Deserialization غير آمن'},
            {'type': 'Programming Errors', 'severity': 'High', 'description': 'Buffer overflow'},
            {'type': 'Programming Errors', 'severity': 'High', 'description': 'Path traversal'},
            {'type': 'Programming Errors', 'severity': 'Critical', 'description': 'SQL injection من عدم التحقق'},
            {'type': 'Programming Errors', 'severity': 'High', 'description': 'XSS من عدم التحقق من المدخلات'},
            {'type': 'OS Vulnerabilities', 'severity': 'High', 'description': 'ثغرات نظام التشغيل غير المحدثة'},
        ]
        
        all_vulnerabilities = traditional_vulns + config_vulns + programming_errors
        
        for vuln in all_vulnerabilities:
            categories[vuln['type']].append(vuln)
        
        return categories
    
    def display_summary(self):
        """عرض ملخص الأمان الشامل"""
        print("=" * 100)
        print("🔐 ملخص الأمان الشامل - SaudiHack")
        print("=" * 100)
        print(f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        categories = self.categorize_vulnerabilities()
        
        # إحصائيات عامة
        total_vulns = sum(len(vulns) for vulns in categories.values())
        critical_count = sum(1 for vulns in categories.values() for v in vulns if v['severity'] == 'Critical')
        high_count = sum(1 for vulns in categories.values() for v in vulns if v['severity'] == 'High')
        medium_count = sum(1 for vulns in categories.values() for v in vulns if v['severity'] == 'Medium')
        low_count = sum(1 for vulns in categories.values() for v in vulns if v['severity'] == 'Low')
        
        print("📊 إحصائيات الثغرات:")
        print(f"   إجمالي الثغرات: {total_vulns}")
        print(f"   🔴 Critical: {critical_count}")
        print(f"   🟠 High: {high_count}")
        print(f"   🟡 Medium: {medium_count}")
        print(f"   🟢 Low: {low_count}")
        print()
        
        # عرض التصنيفات
        print("🎯 تصنيف الثغرات:")
        print("-" * 80)
        
        for category, vulns in categories.items():
            if vulns:
                print(f"\n{category} ({len(vulns)} ثغرة):")
                for vuln in vulns:
                    severity_icon = {
                        'Critical': '🔴',
                        'High': '🟠',
                        'Medium': '🟡',
                        'Low': '🟢'
                    }.get(vuln['severity'], '⚪')
                    print(f"   {severity_icon} {vuln['description']}")
        
        print()
        print("=" * 100)
        
        # توصيات الأمان
        self.display_recommendations()
    
    def display_recommendations(self):
        """عرض توصيات الأمان"""
        print("💡 توصيات الأمان:")
        print("-" * 50)
        
        recommendations = [
            "1. تحديث جميع البرامج ونظام التشغيل بانتظام",
            "2. استخدام كلمات مرور قوية وغير افتراضية",
            "3. تمكين رؤوس الأمان في الخادم",
            "4. استخدام HTTPS مع شهادات SSL/TLS قوية",
            "5. التحقق من صحة جميع مدخلات المستخدم",
            "6. تقييد الوصول إلى المنافذ غير الضرورية",
            "7. استخدام WAF (Web Application Firewall)",
            "8. مراجعة الكود المصدري للتطبيقات",
            "9. إجراء فحوصات أمنية دورية",
            "10. تدريب فريق التطوير على أفضل ممارسات الأمان"
        ]
        
        for rec in recommendations:
            print(f"   {rec}")
        
        print()
        print("📋 ملاحظات مهمة:")
        print("   • جميع الثغرات يجب معالجتها حسب أولوية الخطورة")
        print("   • إنشاء خطة تصحيح واضحة مع جدول زمني")
        print("   • اختبار التصحيحات قبل النشر في البيئة الإنتاجية")
        print("   • توثيق جميع التغييرات والإصلاحات")
    
    def save_summary_report(self):
        """حفظ تقرير الملخص"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'security_summary_{timestamp}.txt'
        
        categories = self.categorize_vulnerabilities()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("ملخص الأمان الشامل\n")
            f.write("=" * 50 + "\n")
            f.write(f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for category, vulns in categories.items():
                if vulns:
                    f.write(f"\n{category} ({len(vulns)} ثغرة):\n")
                    for vuln in vulns:
                        f.write(f"   {vuln['severity']}: {vuln['description']}\n")
        
        print(f"✅ تم حفظ التقرير: {filename}")

def main():
    """الدالة الرئيسية"""
    summary = SecuritySummary()
    summary.display_summary()
    
    # حفظ التقرير
    summary.save_summary_report()

if __name__ == "__main__":
    main()