# 🔒 SaudiHack Security Scanner - نظام فحص الأمان السعودي

## 📋 نظرة عامة
نظام متكامل لفحص الأمان الرقمي يكتشف الثغرات الأمنية في المواقع والتطبيقات السعودية، بما في ذلك ثغرات التكوين، أخطاء البرمجة، وثغرات النظام.

## ✨ المميزات

### 🎯 تغطية شاملة
- ✅ فحص المواقع الحكومية السعودية
- ✅ اكتشاف ثغرات SQL Injection و XSS
- ✅ فحص ثغرات التكوين والإعدادات الخاطئة
- ✅ اكتشاف أخطاء البرمجة الأمنية
- ✅ فحص المنافذ المفتوحة والخدمات

### 🔧 سهولة الاستخدام
- ✅ واجهة عربية كاملة
- ✅ تشغيل بنقرة واحدة
- ✅ تقارير مفصلة بالعربية
- ✅ متوافق مع Windows/Linux/macOS

## 🚀 التثبيت السريع

### الخطوة 1: تثبيت Python
```bash
# Windows: حمل من python.org
# Linux: sudo apt install python3 python3-pip
# macOS: brew install python3
```

### الخطوة 2: تثبيت المشروع
```bash
git clone [repository-url]
cd saudihack
pip install -r requirements.txt
```

### الخطوة 3: التشغيل الفوري
```bash
# للمبتدئين - تشغيل بنقرة واحدة
python run_all_simple.py

# أو استخدام ملف التشغيل على Windows
双击 run.bat

# للمحترفين - تشغيل متقدم
python auto_run.py --mode full --report
```

## 🎯 استخدام الأدوات

### 1️⃣ فحص المواقع المصابة
```bash
python show_infected_sites.py
```
**الوظيفة**: فحص توفر المواقع السعودية المهمة
**النتائج**: تقرير JSON + عرض شاشة

### 2️⃣ عرض روابط الثغرات
```bash
python show_vulnerability_links.py
```
**الوظيفة**: توليد روابط اختبار للثغرات
**الأنواع**: SQL Injection, XSS, RCE, LFI, Configuration

### 3️⃣ الملخص الشامل
```bash
python security_summary.py
```
**الوظيفة**: عرض ملخص شامل لجميع الثغرات
**المخرجات**: تقرير نصي بالعربية مع التوصيات

### 4️⃣ فحص التكوين المتقدم
```bash
python core/config_security_scanner.py --target localhost
```
**الوظيفة**: فحص تكوين النظام والخدمات
**الفحص**: المنافذ، الإعدادات، الأذونات

## 📊 أنواع الثغرات المكتشفة

### ثغرات الويب
- 🔍 **SQL Injection** - حقن قواعد البيانات
- 🎭 **XSS** - البرمجة عبر المواقع
- 📂 **LFI/RFI** - تضمين الملفات
- ⚡ **RCE** - تنفيذ الأوامر عن بعد

### ثغرات التكوين
- ⚙️ **إعدادات افتراضية غير آمنة**
- 🔑 **كلمات مرور ضعيفة**
- 🌐 **منافذ مفتوحة غير ضرورية**
- 📄 **ملفات حساسة ظاهرة**

### أخطاء البرمجة
- 🐛 **أخطاء في التحقق من المدخلات**
- 🔓 **معلومات حساسة في الكود**
- 🛡️ **مشاكل في التشفير**
- 📊 **تسرب المعلومات**

## 📁 الملفات والمجلدات

```
SaudiHack/
├── 📋 ملفات التثبيت:
│   ├── INSTALLATION_GUIDE.md - دليل التثبيت الكامل
│   ├── README_INSTALL.md - دليل سريع
│   ├── requirements.txt - المتطلبات
│   └── run.bat - تشغيل Windows
├── 🎯 أدوات التشغيل:
│   ├── run_all_simple.py - تشغيل سهل
│   ├── auto_run.py - تشغيل متقدم
│   └── run_all.py - تشغيل شامل
├── 🔍 أدوات الفحص:
│   ├── show_infected_sites.py - فحص المواقع
│   ├── show_vulnerability_links.py - عرض الثغرات
│   ├── security_summary.py - الملخص الشامل
│   └── core/ - أدوات النواة
├── 📊 بيانات الفحص:
│   ├── data/misconfig_payloads.txt - حمولات التكوين
│   └── data/vulnerability_patterns.json - أنماط الثغرات
└── 📁 نتائج الفحص:
    ├── *.json - تقارير JSON
    ├── *.txt - ملخصات نصية
    └── logs/ - سجلات التشغيل
```

## 🔧 خيارات التشغيل المتقدمة

### auto_run.py - التشغيل الذكي
```bash
# وضع سريع
python auto_run.py --mode quick

# وضع شامل مع تقارير
python auto_run.py --mode full --report --output results/

# استهداف محدد
python auto_run.py --target saudi.gov.sa --ports 80,443
```

### خيارات إضافية
```bash
--verbose      عرض تفاصيل إضافية
--export       تصدير النتائج
--format txt/json/csv
--threads N    عدد المواضيع المستخدمة
```

## 🛡️ الأمان والخصوصية

### 🎯 مبادئ الأخلاقيات
- ✅ فقط للمواقع التي تمتلك الصلاحية
- ✅ لا يستخدم للهجمات الضارة
- ✅ يحترم خصوصية البيانات
- ✅ يحفظ النتائج محلياً فقط

### 🔒 التوصيات الأمنية
- استخدم VPN عند الفحص من شبكات عامة
- احفظ التقارير في مواقع آمنة
- قم بتحديث الأدوات بانتظام
- راجع التقارير بعناية قبل اتخاذ إجراءات

## 🆘 استكشاف الأخطاء

### مشاكل شائعة
| المشكلة | الحل |
|---------|------|
| Python not found | تأكد من تثبيت Python وإضافته للPATH |
| pip install فشل | استخدم: `pip install --user -r requirements.txt` |
| تشغيل بطيء | قلل عدد المواضيع بـ `--threads 1` |
| خطأ في الأذونات | شغل كمسؤول أو استخدم sudo |

### الدعم الفني
- 📧 راسلنا عبر البريد الإلكتروني
- 💬 انضم لمجموعة الدعم على Telegram
- 📖 راجع ملفات README التفصيلية
- 🔍 استخدم أمر `python script.py --help`

## 📞 التواصل والدعم

### 📱 قنوات التواصل
- **الموقع الرسمي**: [saudihack-security.com](https://saudihack-security.com)
- **Telegram**: @SaudiHackSupport
- **البريد**: support@saudihack.com
- **GitHub**: [github.com/saudihack/scanner](https://github.com/saudihack/scanner)

### 🎯 المساهمة في المشروع
نرحب بالمساهمات من المجتمع:
- 🐛 الإبلاغ عن الأخطاء
- 💡 اقتراح ميزات جديدة
- 📖 تحسين الوثائق
- 🔧 إضافة أدوات جديدة

## 🔄 التحديثات

### التحقق من التحديثات
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### النسخ الاحتياطي
```bash
# نسخ احتياطي للإعدادات
cp config/settings.json config/settings_backup.json

# نسخ احتياطي للنتائج
cp -r results/ results_backup_$(date +%Y%m%d)/
```

---

## 🎉 البدء السريع

**في 3 خطوات فقط:**

1. **تحميل**: `git clone [url]`
2. **تثبيت**: `pip install -r requirements.txt`
3. **تشغيل**: `python run_all_simple.py`

**أو ببساطة:** انقر مرتين على `run.bat` في Windows

---

**⚡ تم تطوير هذا المشروع بواسطة فريق SaudiHack Security**
**🎯 هدفنا: تعزيز الأمن الرقمي في المملكة العربية السعودية**