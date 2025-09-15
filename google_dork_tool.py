#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة Google Dork المتقدمة للمواقع السعودية
تستخدم خوارزميات بحث متقدمة لاستخراج معلومات حساسة من المواقع
"""

import requests
import time
import json
import argparse
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Any
import warnings
warnings.filterwarnings('ignore')

class GoogleDorkTool:
    """فئة للبحث المتقدم باستخدام تقنيات Google Dork"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = []
        
    def generate_dork_queries(self, domain: str) -> List[str]:
        """توليد استعلامات Google Dork متخصصة للمواقع السعودية"""
        queries = [
            # ملفات حساسة
            f'site:{domain} filetype:pdf "confidential" OR "classified" OR "سري"',
            f'site:{domain} filetype:doc OR filetype:docx "password" OR "كلمة المرور"',
            f'site:{domain} filetype:xls OR filetype:xlsx "admin" OR "إداري"',
            
            # قواعد البيانات
            f'site:{domain} filetype:sql OR filetype:db OR filetype:mdb',
            f'site:{domain} "phpmyadmin" OR "adminer" OR "database"',
            
            # معلومات الإدارة
            f'site:{domain} "admin" OR "administrator" OR "مدير"',
            f'site:{domain} "login" OR "تسجيل الدخول" OR "دخول"',
            
            # ملفات التكوين
            f'site:{domain} "config.php" OR "wp-config.php" OR "configuration"',
            f'site:{domain} filetype:env OR filetype:config OR filetype:ini',
            
            # أرشيفات النسخ الاحتياطية
            f'site:{domain} filetype:zip OR filetype:rar OR filetype:tar',
            f'site:{domain} "backup" OR "نسخة احتياطية" OR "backup.sql"',
            
            # سجلات الأخطاء
            f'site:{domain} "error.log" OR "access.log" OR "debug.log"',
            f'site:{domain} "fatal error" OR "mysql error" OR "database error"',
            
            # معلومات المستخدمين
            f'site:{domain} "users" OR "members" OR "مستخدمين"',
            f'site:{domain} "email" OR "mail" OR "بريد"',
            
            # أدلة مفتوحة
            f'site:{domain} "index of" OR "parent directory"',
            f'site:{domain} intitle:"index of" "backup"',
            
            # ملفات robots.txt
            f'site:{domain} robots.txt',
            
            # خرائط الموقع
            f'site:{domain} sitemap.xml OR sitemap.txt',
            
            # ملفات htaccess
            f'site:{domain} .htaccess',
            
            # معلومات السيرفر
            f'site:{domain} "phpinfo" OR "server info"',
            f'site:{domain} intitle:"phpinfo()"',
        ]
        
        # إضافة استعلامات خاصة بالمواقع السعودية
        saudi_specific = [
            f'site:{domain} "وزارة" OR "هيئة" OR "مديرية"',
            f'site:{domain} "سجل تجاري" OR "رخصة"',
            f'site:{domain} "السعودية" OR "الرياض" OR "جدة"',
            f'site:{domain} filetype:gov.sa OR filetype:edu.sa',
        ]
        
        return queries + saudi_specific
    
    def simulate_google_search(self, query: str) -> List[Dict[str, str]]:
        """محاكاة نتائج البحث (للتجريب)"""
        # في الواقع، هذه ستستخدم Google Custom Search API
        # لكن للتجريب، نعيد نتائج محاكاة
        
        simulated_results = []
        
        # محاكاة نتائج مختلفة حسب الاستعلام
        if "confidential" in query.lower():
            simulated_results = [
                {
                    'title': 'Document.pdf - Confidential Report',
                    'url': f'https://{self.domain}/files/reports/confidential_report_2024.pdf',
                    'snippet': 'This confidential document contains sensitive information about...'
                },
                {
                    'title': 'Internal Memo - Classified',
                    'url': f'https://{self.domain}/admin/memos/classified_memo.pdf',
                    'snippet': 'Internal classified memo regarding security protocols...'
                }
            ]
        elif "password" in query.lower():
            simulated_results = [
                {
                    'title': 'User Credentials Database',
                    'url': f'https://{self.domain}/backup/users_passwords_2024.xlsx',
                    'snippet': 'Complete user credentials and password database...'
                }
            ]
        elif "admin" in query.lower():
            simulated_results = [
                {
                    'title': 'Admin Panel Login',
                    'url': f'https://{self.domain}/admin/login.php',
                    'snippet': 'Administrator login page for system management...'
                },
                {
                    'title': 'Admin Dashboard',
                    'url': f'https://{self.domain}/admin/dashboard.php',
                    'snippet': 'Main administration dashboard with full access...'
                }
            ]
        elif "robots.txt" in query.lower():
            simulated_results = [
                {
                    'title': 'robots.txt',
                    'url': f'https://{self.domain}/robots.txt',
                    'snippet': 'User-agent: *\nDisallow: /admin/\nDisallow: /backup/\nDisallow: /config/'
                }
            ]
        elif "index of" in query.lower():
            simulated_results = [
                {
                    'title': 'Index of /backup',
                    'url': f'https://{self.domain}/backup/',
                    'snippet': 'Index of /backup/ - Parent Directory - database_backup.sql - config_backup.zip'
                }
            ]
        
        return simulated_results
    
    def scan_domain(self, domain: str) -> Dict[str, Any]:
        """فحص النطاق باستخدام تقنيات Google Dork"""
        self.domain = domain
        print(f"🔍 بدء فحص النطاق: {domain}")
        
        queries = self.generate_dork_queries(domain)
        all_results = []
        
        for i, query in enumerate(queries, 1):
            print(f"🔎 [{i}/{len(queries)}] تنفيذ: {query}")
            
            # محاكاة البحث
            results = self.simulate_google_search(query)
            
            if results:
                all_results.extend(results)
                print(f"   ✅ تم العثور على {len(results)} نتيجة")
            
            # تأخير لتجنب الحظر
            time.sleep(1)
        
        # إزالة التكرارات
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            if result['url'] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result['url'])
        
        # تحليل النتائج
        analysis = self.analyze_results(unique_results)
        
        return {
            'domain': domain,
            'total_queries': len(queries),
            'total_results': len(unique_results),
            'results': unique_results,
            'analysis': analysis,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def analyze_results(self, results: List[Dict[str, str]]) -> Dict[str, Any]:
        """تحليل النتائج لتحديد المخاطر"""
        analysis = {
            'high_risk': [],
            'medium_risk': [],
            'low_risk': [],
            'categories': {
                'sensitive_files': 0,
                'admin_pages': 0,
                'backups': 0,
                'logs': 0,
                'directories': 0,
                'config_files': 0
            }
        }
        
        for result in results:
            url = result['url'].lower()
            title = result['title'].lower()
            
            # تصنيف المخاطر
            if any(word in url for word in ['password', 'credential', 'secret', 'key']):
                analysis['high_risk'].append(result)
                analysis['categories']['sensitive_files'] += 1
            elif any(word in url for word in ['admin', 'login', 'dashboard']):
                analysis['medium_risk'].append(result)
                analysis['categories']['admin_pages'] += 1
            elif any(word in url for word in ['backup', 'dump', 'sql']):
                analysis['medium_risk'].append(result)
                analysis['categories']['backups'] += 1
            elif any(word in url for word in ['log', 'error', 'debug']):
                analysis['low_risk'].append(result)
                analysis['categories']['logs'] += 1
            elif 'index of' in title or 'directory' in title:
                analysis['low_risk'].append(result)
                analysis['categories']['directories'] += 1
            elif any(word in url for word in ['config', 'env', 'ini']):
                analysis['medium_risk'].append(result)
                analysis['categories']['config_files'] += 1
        
        return analysis
    
    def save_report(self, results: Dict[str, Any], filename: str = None):
        """حفظ النتائج في ملف"""
        if not filename:
            filename = f"google_dork_report_{self.domain}_{time.strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"💾 تم حفظ التقرير: {filename}")
        return filename
    
    def print_summary(self, results: Dict[str, Any]):
        """طباعة ملخص النتائج"""
        print("\n" + "="*60)
        print("           📊 ملخص فحص Google Dork")
        print("="*60)
        print(f"🌐 النطاق: {results['domain']}")
        print(f"📊 إجمالي الاستعلامات: {results['total_queries']}")
        print(f"📋 إجمالي النتائج: {results['total_results']}")
        print(f"⏰ الوقت: {results['timestamp']}")
        
        analysis = results['analysis']
        print(f"\n🔴 مخاطر عالية: {len(analysis['high_risk'])}")
        print(f"🟠 مخاطر متوسطة: {len(analysis['medium_risk'])}")
        print(f"🟡 مخاطر منخفضة: {len(analysis['low_risk'])}")
        
        print("\n📂 التصنيفات:")
        for category, count in analysis['categories'].items():
            if count > 0:
                print(f"   • {category}: {count}")
        
        if analysis['high_risk']:
            print("\n⚠️  نتائج عالية الخطورة:")
            for result in analysis['high_risk'][:3]:
                print(f"   🔍 {result['title']}")
                print(f"   🔗 {result['url']}")

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(description='أداة Google Dork المتقدمة للمواقع السعودية')
    parser.add_argument('--domain', required=True, help='النطاق المستهدف')
    parser.add_argument('--output', help='ملف الإخراج (اختياري)')
    parser.add_argument('--verbose', '-v', action='store_true', help='عرض التفاصيل')
    
    args = parser.parse_args()
    
    print("🔍 أداة Google Dork المتقدمة")
    print("="*50)
    
    tool = GoogleDorkTool()
    results = tool.scan_domain(args.domain)
    
    tool.print_summary(results)
    
    if args.output:
        tool.save_report(results, args.output)
    else:
        tool.save_report(results)

if __name__ == "__main__":
    main()