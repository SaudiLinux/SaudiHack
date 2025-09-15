# 🚀 دليل التثبيت السريع - SaudiHack

## 📥 التثبيت في 3 خطوات

### الخطوة 1: تثبيت Python
- **Windows**: حمل من [python.org](https://python.org) ✅
- **Linux**: `sudo apt install python3 python3-pip`
- **macOS**: `brew install python3`

### الخطوة 2: تثبيت المشروع
```bash
git clone https://github.com/your-repo/saudihack.git
cd saudihack
pip install -r requirements.txt
```

### الخطوة 3: التشغيل
```bash
# للمبتدئين
python run_all_simple.py

# للمحترفين
python auto_run.py --mode full --report
```

## 🎯 الأدوات المتوفرة

| الأداة | الوظيفة | الأمر |
|--------|----------|--------|
| `show_infected_sites.py` | فحص المواقع المصابة | `python show_infected_sites.py` |
| `show_vulnerability_links.py` | عرض روابط الثغرات | `python show_vulnerability_links.py` |
| `security_summary.py` | ملخص الأمان الشامل | `python security_summary.py` |
| `config_security_scanner.py` | فحص التكوين الأمني | `python core/config_security_scanner.py` |

## 🔧 الأوامر السريعة

### فحص موقع محدد:
```bash
python show_infected_sites.py --sites saudi.gov.sa
```

### تصدير النتائج:
```bash
python show_vulnerability_links.py --export --format txt
```

### فحص شامل:
```bash
python auto_run.py --mode full --output results/
```

## 📁 الملفات الناتجة
- `infected_sites_report.json` - تقرير المواقع
- `vulnerability_links.txt` - روابط الثغرات
- `security_summary.txt` - ملخص الأمان

## 🆘 حل المشاكل السريع

| المشكلة | الحل |
|---------|------|
| "Python not found" | استخدم `py` بدلاً من `python` |
| خطأ في الحزم | `pip install --upgrade pip` |
| صلاحيات | شغل كمسؤول |

## 📞 للمساعدة
- تحقق من: `INSTALLATION_GUIDE.md` للتفاصيل الكاملة
- سجلات الأخطاء: `logs/`
- الوثائق: `docs/`

**جاهز للاستخدام! 🎉**