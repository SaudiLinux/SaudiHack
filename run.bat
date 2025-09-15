@echo off
chcp 65001 >nul
echo.
echo ================================================
echo 🎯 SaudiHack - تشغيل تلقائي لجميع الأوامر
echo ================================================
echo.

echo 📅 التاريخ: %date% %time%
echo.

echo 🚀 بدء تشغيل أدوات SaudiHack...
echo.

echo 1️⃣ عرض المواقع المصابة...
python show_infected_sites.py
echo.

timeout /t 2 >nul

echo 2️⃣ عرض روابط الثغرات الأمنية...
python show_vulnerability_links.py
echo.

timeout /t 2 >nul

echo 3️⃣ الفحص الشامل...
python main.py --scan-all
echo.

timeout /t 2 >nul

echo 4️⃣ تحليل الثغرات...
python core/vulnerability_analyzer.py
echo.

echo ================================================
echo ✅ تم إكمال جميع الأوامر بنجاح!
echo 📅 الوقت: %date% %time%
echo ================================================
echo.
pause