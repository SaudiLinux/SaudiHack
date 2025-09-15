#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
قائمة المواقع السعودية الجاهزة للفحص الأمني
"""

SAUDI_SITES = {
    "government": [
        "moi.gov.sa", "mofa.gov.sa", "mod.gov.sa", "mof.gov.sa", 
        "moh.gov.sa", "moe.gov.sa", "moj.gov.sa", "municipal.gov.sa",
        "mot.gov.sa", "mcit.gov.sa", "zakat.gov.sa", "stats.gov.sa",
        "sdaia.gov.sa", "gaca.gov.sa", "customs.gov.sa", "sfda.gov.sa",
        "tourism.gov.sa", "saso.gov.sa", "absher.sa", "balady.gov.sa",
        "muqeem.sa", "my.gov.sa"
    ],
    
    "commercial": [
        "sabic.com.sa", "aramco.com.sa", "stc.com.sa", "alrajhibank.com.sa",
        "alinma.com", "bankalbilad.com", "banquefransi.com.sa", "alahli.com",
        "riyadbank.com", "samba.com", "mobily.com.sa", "sa.zain.com",
        "virginmobile.sa", "souq.com.sa", "noon.com.sa", "aldawaa.com",
        "nahdi.sa", "extra.com.sa", "arabianoud.com", "tamara.com"
    ],
    
    "news_media": [
        "alarabiya.net", "alikhbariya.net", "alwatan.com.sa", "alriyadh.com",
        "okaz.com.sa", "aawsat.com", "al-madina.com", "albilad.net",
        "sabq.org.sa", "alyaum.com", "almowaten.net", "almowaten.sa",
        "almrsd.com", "al-ain.com"
    ],
    
    "military_security": [
        "mod.gov.sa", "af.mod.gov.sa", "rsaf.mod.gov.sa", "rsnf.mod.gov.sa",
        "rsa.mod.gov.sa", "998.gov.sa", "999.gov.sa", "990.gov.sa",
        "traffic.gov.sa", "passports.gov.sa"
    ],
    
    "banking_financial": [
        "sama.gov.sa", "alahli.com", "riyadbank.com", "samba.com",
        "alrajhibank.com.sa", "alinma.com", "bankalbilad.com", "banquefransi.com.sa",
        "sabb.com", "alarabibank.com.sa", "baj.com.sa", "tadawul.com.sa",
        "saudicapital.com.sa", "pif.gov.sa", "gosi.gov.sa", "redf.gov.sa",
        "sidf.gov.sa", "adf.gov.sa"
    ],
    
    "education": [
        "ksu.edu.sa", "kau.edu.sa", "kfupm.edu.sa", "iu.edu.sa",
        "kku.edu.sa", "tu.edu.sa", "jazanu.edu.sa", "ut.edu.sa",
        "nu.edu.sa", "uhb.edu.sa", "pnu.edu.sa", "dhu.edu.sa",
        "uj.edu.sa", "yamamah.edu.sa", "fu.edu.sa", "tvtc.gov.sa",
        "ipm.edu.sa", "elc.edu.sa"
    ],
    
    "healthcare": [
        "moh.gov.sa", "sfda.gov.sa", "medical.mil.sa", "kfshrc.edu.sa",
        "kkuh.med.sa", "ngha.med.sa", "afh.med.sa", "ncc.org.sa",
        "nch.med.sa", "sehha.sa"
    ]
}

def get_all_sites():
    """الحصول على جميع المواقع"""
    all_sites = []
    for category, sites in SAUDI_SITES.items():
        all_sites.extend(sites)
    return list(set(all_sites))

def get_sites_by_category(category):
    """الحصول على المواقع حسب الفئة"""
    return SAUDI_SITES.get(category, [])

def print_summary():
    """طباعة ملخص المواقع"""
    print("="*50)
    print("           📊 قائمة المواقع السعودية")
    print("="*50)
    
    total = 0
    category_names = {
        "government": "المواقع الحكومية",
        "commercial": "المواقع التجارية", 
        "news_media": "المواقع الإخبارية",
        "military_security": "المواقع العسكرية",
        "banking_financial": "البنوك والمصارف",
        "education": "الجامعات والتعليم",
        "healthcare": "القطاع الصحي"
    }
    
    for category, sites in SAUDI_SITES.items():
        count = len(sites)
        total += count
        print(f"📂 {category_names[category]}: {count} موقع")
    
    print(f"\n🎯 إجمالي المواقع: {total} موقع")

if __name__ == "__main__":
    print_summary()
    
    # عرض جميع المواقع
    all_sites = get_all_sites()
    print(f"\n📋 إجمالي المواقع الفريدة: {len(all_sites)}")
    
    # حفظ في ملف
    with open("saudi_sites.txt", "w", encoding="utf-8") as f:
        for site in sorted(all_sites):
            f.write(f"{site}\n")
    print("💾 تم حفظ المواقع في ملف saudi_sites.txt")