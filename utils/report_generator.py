#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مولد التقارير الأمنية - Report Generator
يستخدم لإنشاء تقارير مفصلة بالعربية والإنجليزية
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any

class ReportGenerator:
    """فئة لإنشاء تقارير أمنية متعددة الصيغ"""
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """التأكد من وجود مجلد النتائج"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_json_report(self, data: Dict[str, Any], filename: str = None) -> str:
        """إنشاء تقرير JSON"""
        if not filename:
            filename = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def generate_txt_report(self, data: Dict[str, Any], filename: str = None) -> str:
        """إنشاء تقرير نصي بالعربية"""
        if not filename:
            filename = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("           تقرير الأمان الشامل\n")
            f.write("=" * 60 + "\n")
            f.write(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for category, vulnerabilities in data.items():
                f.write(f"📊 {category}:\n")
                f.write("-" * 40 + "\n")
                
                if isinstance(vulnerabilities, list):
                    for vuln in vulnerabilities:
                        if isinstance(vuln, dict):
                            f.write(f"🔍 {vuln.get('name', 'غير معروف')}\n")
                            f.write(f"📋 الوصف: {vuln.get('description', '')}\n")
                            f.write(f"⚠️ الخطورة: {vuln.get('severity', 'غير محدد')}\n")
                            f.write("-" * 30 + "\n")
                        else:
                            f.write(f"• {vuln}\n")
                else:
                    f.write(f"{vulnerabilities}\n")
                
                f.write("\n")
        
        return filepath
    
    def generate_csv_report(self, data: List[Dict], filename: str = None) -> str:
        """إنشاء تقرير CSV"""
        if not filename:
            filename = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        if not data:
            return filepath
        
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        return filepath
    
    def create_summary_report(self, scan_results: Dict[str, Any]) -> Dict[str, str]:
        """إنشاء تقارير متعددة الصيغ"""
        reports = {}
        
        # JSON
        reports['json'] = self.generate_json_report(scan_results)
        
        # TXT
        reports['txt'] = self.generate_txt_report(scan_results)
        
        # CSV (إذا كانت البيانات مناسبة)
        if 'vulnerabilities' in scan_results and isinstance(scan_results['vulnerabilities'], list):
            reports['csv'] = self.generate_csv_report(scan_results['vulnerabilities'])
        
        return reports