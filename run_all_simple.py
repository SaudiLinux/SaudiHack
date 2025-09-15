#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaudiHack Simple Auto Runner - تشغيل تلقائي بسيط
"""

import os
import sys
import importlib.util
from datetime import datetime

class SimpleRunner:
    def __init__(self):
        self.start_time = datetime.now()
        
    def print_header(self, text):
        print("\n" + "="*60)
        print(f"🎯 {text}")
        print("="*60)
    
    def print_success(self, text):
        print(f"✅ {text}")
    
    def print_error(self, text):
        print(f"❌ {text}")
    
    def run_script(self, script_name, description):
        """تشغيل سكربت مباشرة بدون subprocess"""
        try:
            self.print_header(description)
            
            if not os.path.exists(script_name):
                self.print_error(f"الملف {script_name} غير موجود")
                return False
            
            # تشغيل السكربت مباشرة
            spec = importlib.util.spec_from_file_location("module", script_name)
            module = importlib.util.module_from_spec(spec)
            
            # حفظ sys.argv الأصلي
            original_argv = sys.argv.copy()
            
            # تعيين sys.argv جديد للسكربت
            sys.argv = [script_name]
            
            try:
                spec.loader.exec_module(module)
                self.print_success(f"تم تشغيل {description} بنجاح")
                return True
            except SystemExit:
                # تجاهل sys.exit() من السكربت
                self.print_success(f"تم تشغيل {description} بنجاح")
                return True
            except Exception as e:
                self.print_error(f"خطأ في {description}: {str(e)}")
                return False
            finally:
                # استعادة sys.argv
                sys.argv = original_argv
                
        except Exception as e:
            self.print_error(f"خطأ عام في {description}: {str(e)}")
            return False
    
    def run_all(self):
        """تشغيل جميع السكربتات"""
        self.print_header("بدء تشغيل جميع أدوات SaudiHack")
        print(f"📅 الوقت: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        scripts = [
            ("show_infected_sites.py", "عرض المواقع المصابة"),
            ("show_vulnerability_links.py", "عرض روابط الثغرات الأمنية"),
        ]
        
        success_count = 0
        total_count = len(scripts)
        
        for script, description in scripts:
            if self.run_script(script, description):
                success_count += 1
            print("\n" + "-"*60)
        
        # عرض النتائج
        self.print_header("ملخص التنفيذ")
        print(f"📋 إجمالي السكربتات: {total_count}")
        print(f"✅ الناجحة: {success_count}")
        print(f"❌ الفاشلة: {total_count - success_count}")
        print(f"📈 نسبة النجاح: {(success_count/total_count)*100:.1f}%")
        print(f"⏱️ الوقت الكلي: {datetime.now() - self.start_time}")

if __name__ == "__main__":
    try:
        runner = SimpleRunner()
        runner.run_all()
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف التشغيل بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")