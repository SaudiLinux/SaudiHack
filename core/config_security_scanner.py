#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة فحص أمن التكوين والثغرات التكوينية - SaudiHack
تهدف إلى الكشف عن:
- الثغرات الناتجة عن تكوينات غير صحيحة
- أخطاء البرمجة الأمنية
- الإعدادات الافتراضية الخاطئة
- نقاط الضعف في أنظمة التشغيل
"""

import os
import json
import socket
import subprocess
import platform
import re
from datetime import datetime
from pathlib import Path

class ConfigSecurityScanner:
    def __init__(self):
        self.vulnerabilities = []
        self.config_issues = []
        self.misconfigurations = []
        
    def scan_all(self):
        """فحص شامل لجميع أنواع الثغرات التكوينية"""
        print("🔍 بدء فحص الثغرات التكوينية والأمنية...")
        
        # فحص أنظمة التشغيل
        self.scan_os_vulnerabilities()
        
        # فحص الإعدادات الافتراضية
        self.scan_default_configs()
        
        # فحص أخطاء البرمجة
        self.scan_coding_errors()
        
        # فحص التكوينات الخاطئة
        self.scan_misconfigurations()
        
        # فحص المنافذ المفتوحة
        self.scan_open_ports()
        
        # فحص الأذونات
        self.scan_file_permissions()
        
        return self.generate_report()
    
    def scan_os_vulnerabilities(self):
        """فحص ثغرات أنظمة التشغيل"""
        system_info = {
            'platform': platform.system(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
        
        # ثغرات Windows شائعة
        if system_info['platform'] == 'Windows':
            self.check_windows_vulnerabilities(system_info)
        
        # ثغرات Linux شائعة
        elif system_info['platform'] == 'Linux':
            self.check_linux_vulnerabilities(system_info)
    
    def check_windows_vulnerabilities(self, system_info):
        """فحص ثغرات Windows"""
        common_windows_issues = [
            {
                'type': 'Windows Defender Configuration',
                'severity': 'high',
                'description': 'التحقق من إعدادات Windows Defender',
                'check_command': 'Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled',
                'remediation': 'تفعيل الحماية الحية لـ Windows Defender'
            },
            {
                'type': 'Firewall Configuration',
                'severity': 'medium',
                'description': 'التحقق من إعدادات جدار الحماية',
                'check_command': 'netsh advfirewall show allprofiles',
                'remediation': 'تكوين جدار الحماية بشكل صحيح'
            },
            {
                'type': 'User Account Control',
                'severity': 'medium',
                'description': 'التحقق من مستوى UAC',
                'check_command': 'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v EnableLUA',
                'remediation': 'تفعيل UAC على أعلى مستوى'
            }
        ]
        
        for issue in common_windows_issues:
            self.misconfigurations.append(issue)
    
    def check_linux_vulnerabilities(self, system_info):
        """فحص ثغرات Linux"""
        common_linux_issues = [
            {
                'type': 'SSH Configuration',
                'severity': 'high',
                'description': 'التحقق من إعدادات SSH',
                'check_file': '/etc/ssh/sshd_config',
                'checks': [
                    'PermitRootLogin',
                    'PasswordAuthentication',
                    'Port'
                ]
            },
            {
                'type': 'File Permissions',
                'severity': 'medium',
                'description': 'التحقق من أذونات الملفات الحساسة',
                'check_files': ['/etc/passwd', '/etc/shadow', '/etc/sudoers']
            }
        ]
        
        for issue in common_linux_issues:
            self.misconfigurations.append(issue)
    
    def scan_default_configs(self):
        """فحص الإعدادات الافتراضية الخاطئة"""
        default_config_issues = [
            {
                'type': 'Default Passwords',
                'severity': 'critical',
                'description': 'التحقق من كلمات المرور الافتراضية',
                'common_defaults': ['admin:admin', 'admin:password', 'root:root', 'user:user']
            },
            {
                'type': 'Default Ports',
                'severity': 'medium',
                'description': 'التحقق من المنافذ الافتراضية',
                'common_ports': [21, 22, 23, 80, 135, 139, 445, 1433, 3306, 5432]
            },
            {
                'type': 'Default Configurations',
                'severity': 'high',
                'description': 'التحقق من الإعدادات الافتراضية في ملفات التكوين',
                'config_files': [
                    'config.php', 'config.json', 'config.xml', '.env',
                    'database.yml', 'settings.py', 'application.properties'
                ]
            }
        ]
        
        for issue in default_config_issues:
            self.config_issues.append(issue)
    
    def scan_coding_errors(self):
        """فحص أخطاء البرمجة الأمنية"""
        code_patterns = [
            {
                'type': 'SQL Injection',
                'severity': 'high',
                'patterns': [
                    r'.*SELECT.*FROM.*WHERE.*\+.*',
                    r'.*INSERT.*INTO.*VALUES.*\+.*',
                    r'.*UPDATE.*SET.*WHERE.*\+.*'
                ]
            },
            {
                'type': 'XSS Vulnerability',
                'severity': 'medium',
                'patterns': [
                    r'.*echo.*\$_GET\[.*\].*',
                    r'.*print.*\$_POST\[.*\].*',
                    r'.*innerHTML.*=.*user.*'
                ]
            },
            {
                'type': 'Command Injection',
                'severity': 'high',
                'patterns': [
                    r'.*system\(.*\$_GET.*',
                    r'.*exec\(.*\$_POST.*',
                    r'.*shell_exec\(.*\$.*'
                ]
            },
            {
                'type': 'File Inclusion',
                'severity': 'high',
                'patterns': [
                    r'.*include.*\$_GET.*',
                    r'.*require.*\$_POST.*',
                    r'.*file_get_contents.*\$_REQUEST.*'
                ]
            }
        ]
        
        # فحص ملفات الكود في المشروع
        self.scan_code_files(code_patterns)
    
    def scan_code_files(self, patterns):
        """فحص ملفات الكود للبحث عن أنماط خطرة"""
        code_extensions = ['.php', '.py', '.js', '.java', '.cs', '.rb', '.go']
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                if any(file.endswith(ext) for ext in code_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern_info in patterns:
                                for pattern in pattern_info['patterns']:
                                    matches = re.findall(pattern, content, re.IGNORECASE)
                                    if matches:
                                        self.vulnerabilities.append({
                                            'type': pattern_info['type'],
                                            'severity': pattern_info['severity'],
                                            'file': file_path,
                                            'matches': len(matches),
                                            'description': f'تم العثور على {pattern_info["type"]} في {file_path}'
                                        })
                    except Exception as e:
                        pass
    
    def scan_misconfigurations(self):
        """فحص التكوينات الخاطئة في الخادم"""
        config_checks = [
            {
                'type': 'Directory Listing',
                'severity': 'medium',
                'description': 'التحقق من إمكانية تصفح المجلدات',
                'test_path': '/',
                'expected': 'Directory listing should be disabled'
            },
            {
                'type': 'Security Headers',
                'severity': 'medium',
                'description': 'التحقق من وجود رؤوس الأمان',
                'headers': ['X-Frame-Options', 'X-Content-Type-Options', 'X-XSS-Protection', 'Strict-Transport-Security']
            },
            {
                'type': 'SSL/TLS Configuration',
                'severity': 'high',
                'description': 'التحقق من تكوين SSL/TLS',
                'weak_protocols': ['SSLv2', 'SSLv3', 'TLSv1.0', 'TLSv1.1']
            }
        ]
        
        for check in config_checks:
            self.misconfigurations.append(check)
    
    def scan_open_ports(self):
        """فحص المنافذ المفتوحة"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1433, 3306, 3389, 5432, 8080]
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                if result == 0:
                    self.vulnerabilities.append({
                        'type': 'Open Port',
                        'severity': 'low',
                        'port': port,
                        'description': f'المنفذ {port} مفتوح محلياً'
                    })
                sock.close()
            except:
                pass
    
    def scan_file_permissions(self):
        """فحص أذونات الملفات الحساسة"""
        sensitive_files = [
            'config.php', 'config.json', '.env', 'database.yml',
            'settings.py', 'application.properties', 'web.config'
        ]
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file in sensitive_files:
                    file_path = os.path.join(root, file)
                    try:
                        stat = os.stat(file_path)
                        mode = oct(stat.st_mode)[-3:]
                        
                        if mode != '600' and mode != '644':
                            self.vulnerabilities.append({
                                'type': 'File Permissions',
                                'severity': 'medium',
                                'file': file_path,
                                'permissions': mode,
                                'description': f'أذونات غير آمنة للملف: {file_path}'
                            })
                    except Exception as e:
                        pass
    
    def generate_report(self):
        """إنشاء تقرير شامل بالثغرات"""
        report = {
            'scan_date': datetime.now().isoformat(),
            'total_vulnerabilities': len(self.vulnerabilities),
            'total_config_issues': len(self.config_issues),
            'total_misconfigurations': len(self.misconfigurations),
            'vulnerabilities': self.vulnerabilities,
            'config_issues': self.config_issues,
            'misconfigurations': self.misconfigurations,
            'summary': {
                'critical': len([v for v in self.vulnerabilities if v.get('severity') == 'critical']),
                'high': len([v for v in self.vulnerabilities if v.get('severity') == 'high']),
                'medium': len([v for v in self.vulnerabilities if v.get('severity') == 'medium']),
                'low': len([v for v in self.vulnerabilities if v.get('severity') == 'low'])
            }
        }
        
        # حفظ التقرير
        filename = f'config_security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 تم إنشاء تقرير أمن التكوين: {filename}")
        return report

def main():
    """الدالة الرئيسية"""
    scanner = ConfigSecurityScanner()
    return scanner.scan_all()

if __name__ == "__main__":
    main()