#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaudiHack - تشغيل تلقائي لجميع الأوامر
هذا الملف يقوم بتشغيل جميع أدوات المشروع تلقائيًا
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def run_command(command, description):
    """تشغيل أمر مع عرض حالة التنفيذ"""
    print(f"\n{'='*60}")
    print(f"🚀 تشغيل: {description}")
    print(f"📝 الأمر: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ {description} - تم بنجاح")
            if result.stdout:
                print(f"📊 النتائج:\n{result.stdout}")
        else:
            print(f"❌ {description} - فشل")
            if result.stderr:
                print(f"⚠️ الخطأ:\n{result.stderr}")
                
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ خطأ في تنفيذ الأمر: {e}")
        return False

def main():
    """الدالة الرئيسية للتشغيل التلقائي"""
    print("🎯 بدء تشغيل جميع أدوات SaudiHack...")
    print(f"📅 الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # قائمة الأوامر التي سيتم تشغيلها
    commands = [
        ("python show_infected_sites.py", "عرض المواقع المصابة"),
        ("python show_vulnerability_links.py", "عرض روابط الثغرات الأمنية"),
        ("python main.py --scan-all", "فحص شامل لجميع المواقع"),
        ("python core/vulnerability_analyzer.py", "تحليل الثغرات الأمنية"),
    ]
    
    # إحصائيات
    total_commands = len(commands)
    successful_commands = 0
    
    # تشغيل الأوامر واحدًا تلو الآخر
    for command, description in commands:
        success = run_command(command, description)
        if success:
            successful_commands += 1
        
        # تأخير قصير بين الأوامر
        time.sleep(2)
    
    # عرض النتائج النهائية
    print(f"\n{'='*60}")
    print("📊 ملخص التنفيذ:")
    print(f"📋 إجمالي الأوامر: {total_commands}")
    print(f"✅ الأوامر الناجحة: {successful_commands}")
    print(f"❌ الأوامر الفاشلة: {total_commands - successful_commands}")
    print(f"📈 نسبة النجاح: {(successful_commands/total_commands)*100:.1f}%")
    print(f"{'='*60}")
    
    # عرض الخيارات المتاحة
    print("\n🎯 الخيارات المتاحة:")
    print("1. python run_all.py --quick (تشغيل سريع)")
    print("2. python run_all.py --full (فحص كامل)")
    print("3. python run_all.py --report (إنشاء تقارير)")
    print("4. python run_all.py --help (عرض المساعدة)")

if __name__ == "__main__":
    # إعداد اللغة العربية
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # التحقق من وجود الملفات المطلوبة
    required_files = [
        'show_infected_sites.py',
        'show_vulnerability_links.py',
        'main.py',
        'core/vulnerability_analyzer.py'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("❌ الملفات التالية غير موجودة:")
        for file in missing_files:
            print(f"   - {file}")
        sys.exit(1)
    
    # تشغيل البرنامج
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف التشغيل بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")