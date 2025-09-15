# دليل التثبيت والاستخدام - SaudiHack Security Scanner

## 🚀 نظرة عامة
SaudiHack هو نظام متكامل لفحص الأمان يكتشف الثغرات الأمنية في المواقع والتطبيقات، بما في ذلك ثغرات التكوين، أخطاء البرمجة، وثغرات النظام.

## 📋 المتطلبات

### المتطلبات الأساسية
- **نظام التشغيل**: Windows 10/11, Linux, macOS
- **Python**: الإصدار 3.7 أو أحدث
- **ذاكرة**: 4GB RAM كحد أدنى
- **مساحة القرص**: 100MB للتثبيت الكامل

### المتطلبات الإضافية (اختياري)
- **اتصال إنترنت** لتحديث قواعد البيانات
- **صلاحيات المسؤول** لبعض أنواع الفحص المتقدمة

## 🔧 خطوات التثبيت

### 1. تثبيت Python

#### على Windows:
1. تحميل Python من [python.org](https://python.org)
2. تشغيل المثبت وتحديد "Add Python to PATH"
3. التحقق من التثبيت:
   ```bash
   python --version
   pip --version
   ```

#### على Linux/macOS:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# macOS
brew install python3
```

### 2. تحميل المشروع
```bash
# باستخدام Git (إن كان متاحاً)
git clone https://github.com/your-repo/saudihack.git
cd saudihack

# أو تحميل الملفات مباشرة
# قم بفك الضغط عن الملفات في المجلد المطلوب
```

### 3. تثبيت المتطلبات
```bash
# تثبيت الحزم المطلوبة
pip install -r requirements.txt

# إذا واجهت مشاكل، استخدم:
pip install --upgrade pip
pip install -r requirements.txt --user
```

### 4. التحقق من التثبيت
```bash
# اختبار التثبيت
python --version
python -c "import sys; print('Python is ready:', sys.version)"
```

## 🎯 طرق الاستخدام

### الطريقة 1: التشغيل السريع (مستحسن للمبتدئين)
```bash
# على Windows
python run_all_simple.py
# أو انقر مرتين على run.bat

# على Linux/macOS
python3 run_all_simple.py
```

### الطريقة 2: التشغيل المتقدم مع خيارات
```bash
# تشغيل شامل مع تقارير
python auto_run.py --mode full --report --output results/

# فحص مواقع محددة
python show_infected_sites.py --sites saudi.gov.sa,moh.gov.sa

# عرض روابط الثغرات
python show_vulnerability_links.py --export
```

### الطريقة 3: استخدام الأدوات المنفصلة

#### فحص المواقع المصابة:
```bash
python show_infected_sites.py
```

#### عرض ثغرات التكوين والبرمجة:
```bash
python show_vulnerability_links.py
```

#### ملخص الأمان الشامل:
```bash
python security_summary.py
```

#### فحص التكوين الأمني المتقدم:
```bash
python core/config_security_scanner.py --target localhost --port 80
```

## 📊 أنواع الفحص المتوفرة

### 1. فحص المواقع المصابة
- **الوظيفة**: فحص توفر المواقع السعودية
- **النتائج**: تقرير JSON مع تفاصيل الأخطاء
- **الملف**: `show_infected_sites.py`

### 2. فحص الثغرات الأمنية
- **الوظيفة**: اكتشاف ثغرات SQL Injection, XSS, RCE, LFI
- **النتائج**: روابط اختبار جاهزة
- **الملف**: `show_vulnerability_links.py`

### 3. فحص التكوين الأمني
- **الوظيفة**: اكتشاف ثغرات التكوين والبرمجة
- **النتائج**: تقرير شامل بالتوصيات
- **الملف**: `core/config_security_scanner.py`

### 4. الملخص الشامل
- **الوظيفة**: عرض ملخص لجميع الثغرات
- **النتائج**: تقرير نصي بالتوصيات
- **الملف**: `security_summary.py`

## ⚙️ الخيارات المتقدمة

### خيارات auto_run.py
```bash
--mode MODE        : وضع التشغيل (quick, full, custom)
--report          : إنشاء تقارير مفصلة
--output DIR      : مجلد حفظ النتائج
--target HOST     : استهداف خادم محدد
--ports PORTS     : فحص منافذ محددة
--verbose         : عرض تفاصيل إضافية
```

### أمثلة على الاستخدام المتقدم:
```bash
# فحص شامل مع تقارير مخصصة
python auto_run.py --mode full --report --output my_results/

# فحص خادم محدد
python core/config_security_scanner.py --target 192.168.1.100 --ports 80,443,3306

# تصدير روابط الثغرات
python show_vulnerability_links.py --export --format txt
```

## 📁 ملفات النتائج

### أنواع الملفات الناتجة:
- **JSON**: `vulnerability_report_*.json` - تقارير مفصلة
- **TXT**: `security_summary_*.txt` - ملخصات نصية
- **CSV**: `scan_results_*.csv` - نتائج قابلة للتحليل
- **LOG**: `scan_log_*.log` - سجلات التشغيل

### مواقع حفظ النتائج:
```
SaudiHack/
├── results/                    # نتائج الفحص
│   ├── json_reports/          # تقارير JSON
│   ├── txt_summaries/         # ملخصات نصية
│   └── logs/                  # سجلات التشغيل
├── infected_sites_report_*.json
├── vulnerability_links_*.txt
└── security_summary_*.txt
```

## 🔍 استكشاف الأخطاء وحلها

### مشاكل شائعة وحلولها:

#### 1. خطأ "Python not found"
```bash
# الحل على Windows
# أضف Python إلى PATH أو استخدم:
py -m pip install -r requirements.txt

# الحل على Linux/macOS
which python3
python3 -m pip install -r requirements.txt
```

#### 2. خطأ في تثبيت الحزم
```bash
# تحديث pip
python -m pip install --upgrade pip

# تثبيت بالوضع التوافقي
pip install --user -r requirements.txt

# استخدام مرآة مختلفة
pip install -r requirements.txt -i https://pypi.org/simple/
```

#### 3. خطأ "Permission denied"
```bash
# على Linux/macOS
chmod +x *.py
sudo python3 script.py

# على Windows (تشغيل كمسؤول)
# انقر يميناً على Command Prompt -> Run as administrator
```

#### 4. خطأ في استيراد المكتبات
```bash
# التحقق من المكتبات المثبتة
pip list

# إعادة تثبيت المتطلبات
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 🛡️ الأمان والخصوصية

### نصائح الأمان:
- لا تقم بفحص مواقع لا تمتلك الصلاحية لها
- استخدم VPN عند الفحص من شبكات عامة
- احفظ التقارير في مواقع آمنة
- قم بمسح سجلات الفحص الحساسة

### حماية البيانات:
- التقارير محلية ولا تُرسل لخوادم خارجية
- يمكن تشفير التقارير الحساسة
- إعدادات الخصوصية قابلة للتخصيص

## 📞 الدعم والمساعدة

### موارد الدعم:
- **الوثائق**: ملفات README في كل مجلد
- **الأمثلة**: مجلد examples/
- **الأسئلة الشائعة**: FAQ.md
- **التحديثات**: تحقق من repository بانتظام

### الإبلاغ عن المشاكل:
1. تحقق من سجلات الأخطاء
2. قم بإنشاء تقرير مفصل
3. أرفق ملفات التسجيل ذات الصلة

## 🔄 التحديثات

### التحقق من التحديثات:
```bash
# تحديث المستودع
git pull origin main

# تحديث المتطلبات
pip install -r requirements.txt --upgrade

# التحقق من الإصدارات
python -c "import sys; print(sys.version)"
```

### النسخ الاحتياطي:
```bash
# نسخ احتياطي للإعدادات
cp config/settings.json config/settings_backup.json

# نسخ احتياطي للنتائج
cp -r results/ results_backup_$(date +%Y%m%d)/
```

## 🎓 تعلم أكثر

### الموارد التعليمية:
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web Application Security Testing](https://owasp.org/www-project-web-security-testing-guide/)
- [Network Security Assessment](https://www.nsa.gov/Press-Room/Press-Releases-Statements/)

### الشهادات المقترحة:
- CEH (Certified Ethical Hacker)
- OSCP (Offensive Security Certified Professional)
- CISSP (Certified Information Systems Security Professional)

---

## 🎯 ملخص سريع

```bash
# للمبتدئين - تشغيل سريع
python run_all_simple.py

# للمحترفين - تشغيل متقدم
python auto_run.py --mode full --report

# فحص محدد
python security_summary.py
```

**تم التحديث آخر مرة**: 2024
**الإصدار**: 2.0
**التوافق**: Python 3.7+