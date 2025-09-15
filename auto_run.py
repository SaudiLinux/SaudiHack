#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaudiHack Auto Runner - تشغيل تلقائي ذكي
يدعم معلمات مختلفة للتشغيل التلقائي
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
from colorama import init, Fore, Style

# تهيئة الألوان
init(autoreset=True)

class AutoRunner:
    def __init__(self):
        self.start_time = datetime.now()
        self.results = []
        
    def log(self, message, color=Fore.WHITE):
        """طباعة رسائل ملونة"""
        print(f"{color}{message}{Style.RESET_ALL}")
        
    def run_command(self, command, description, timeout=60):
        """تشغيل أمر مع إدارة الأخطاء"""
        self.log(f"🚀 تشغيل: {description}", Fore.CYAN)
        self.log(f"📝 الأمر: {command}", Fore.YELLOW)
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                cwd=os.getcwd(),
                encoding='utf-8',
                errors='ignore'
            )
            
            success = result.returncode == 0
            
            if success:
                self.log(f"✅ {description} - تم بنجاح", Fore.GREEN)
            else:
                self.log(f"❌ {description} - فشل", Fore.RED)
                
            return {
                'command': command,
                'description': description,
                'success': success,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            self.log(f"⏰ {description} - انتهت المهلة", Fore.ORANGE)
            return {'command': command, 'description': description, 'success': False, 'error': 'timeout'}
        except Exception as e:
            self.log(f"💥 {description} - خطأ: {str(e)}", Fore.RED)
            return {'command': command, 'description': description, 'success': False, 'error': str(e)}
    
    def quick_scan(self):
        """فحص سريع"""
        commands = [
            ("python show_infected_sites.py", "عرض المواقع المصابة"),
            ("python show_vulnerability_links.py", "عرض روابط الثغرات"),
        ]
        return commands
    
    def full_scan(self):
        """فحص شامل"""
        commands = [
            ("python show_infected_sites.py", "عرض المواقع المصابة"),
            ("python show_vulnerability_links.py", "عرض روابط الثغرات"),
            ("python main.py --scan-all", "فحص شامل لجميع المواقع"),
            ("python core/vulnerability_analyzer.py", "تحليل الثغرات الأمنية"),
        ]
        return commands
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        report_file = f"auto_run_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("📊 تقرير تشغيل SaudiHack التلقائي\n")
            f.write("=" * 60 + "\n")
            f.write(f"🕐 وقت البدء: {self.start_time}\n")
            f.write(f"🏁 وقت الانتهاء: {datetime.now()}\n")
            f.write(f"📋 إجمالي الأوامر: {len(self.results)}\n")
            
            success_count = sum(1 for r in self.results if r.get('success', False))
            f.write(f"✅ الأوامر الناجحة: {success_count}\n")
            f.write(f"❌ الأوامر الفاشلة: {len(self.results) - success_count}\n")
            f.write("=" * 60 + "\n\n")
            
            for result in self.results:
                f.write(f"🎯 {result['description']}\n")
                f.write(f"📝 الأمر: {result['command']}\n")
                f.write(f"📊 النتيجة: {'✅ ناجح' if result.get('success') else '❌ فشل'}\n")
                if result.get('stdout'):
                    f.write(f"📤 المخرجات:\n{result['stdout']}\n")
                if result.get('stderr'):
                    f.write(f"⚠️ الأخطاء:\n{result['stderr']}\n")
                f.write("-" * 40 + "\n\n")
        
        self.log(f"📝 تم إنشاء التقرير: {report_file}", Fore.GREEN)
        return report_file
    
    def check_requirements(self):
        """التحقق من المتطلبات"""
        required_files = [
            'show_infected_sites.py',
            'show_vulnerability_links.py',
            'main.py',
            'core/vulnerability_analyzer.py'
        ]
        
        missing_files = [f for f in required_files if not os.path.exists(f)]
        
        if missing_files:
            self.log("❌ الملفات التالية غير موجودة:", Fore.RED)
            for file in missing_files:
                self.log(f"   - {file}", Fore.RED)
            return False
        
        return True
    
    def run(self, mode='quick', report=False):
        """تشغيل الأوامر حسب الوضع"""
        if not self.check_requirements():
            return False
        
        self.log("🎯 بدء تشغيل SaudiHack Auto Runner", Fore.MAGENTA)
        self.log(f"📅 الوقت: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"🎮 الوضع: {mode}")
        
        # اختيار الأوامر حسب الوضع
        if mode == 'quick':
            commands = self.quick_scan()
        elif mode == 'full':
            commands = self.full_scan()
        else:
            self.log("❌ وضع غير معروف", Fore.RED)
            return False
        
        # تشغيل الأوامر
        for command, description in commands:
            result = self.run_command(command, description)
            self.results.append(result)
        
        # إنشاء التقرير إذا طلب
        if report:
            self.generate_report()
        
        # عرض النتائج
        self.show_summary()
        
        return True
    
    def show_summary(self):
        """عرض ملخص النتائج"""
        success_count = sum(1 for r in self.results if r.get('success', False))
        
        self.log("\n" + "=" * 60, Fore.MAGENTA)
        self.log("📊 ملخص التنفيذ:", Fore.MAGENTA)
        self.log("=" * 60, Fore.MAGENTA)
        self.log(f"📋 إجمالي الأوامر: {len(self.results)}")
        self.log(f"✅ الأوامر الناجحة: {success_count}", Fore.GREEN)
        self.log(f"❌ الأوامر الفاشلة: {len(self.results) - success_count}", Fore.RED)
        self.log(f"📈 نسبة النجاح: {(success_count/len(self.results)*100):.1f}%")
        self.log(f"⏱️ الوقت الكلي: {datetime.now() - self.start_time}")
        self.log("=" * 60, Fore.MAGENTA)

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(description='SaudiHack Auto Runner')
    parser.add_argument('--mode', choices=['quick', 'full'], default='quick',
                       help='وضع التشغيل: quick أو full (افتراضي: quick)')
    parser.add_argument('--report', action='store_true',
                       help='إنشاء تقرير مفصل')
    parser.add_argument('--no-color', action='store_true',
                       help='تعطيل الألوان')
    
    args = parser.parse_args()
    
    runner = AutoRunner()
    
    try:
        runner.run(mode=args.mode, report=args.report)
    except KeyboardInterrupt:
        runner.log("\n⚠️ تم إيقاف التشغيل بواسطة المستخدم", Fore.YELLOW)
    except Exception as e:
        runner.log(f"❌ خطأ غير متوقع: {e}", Fore.RED)

if __name__ == "__main__":
    main()