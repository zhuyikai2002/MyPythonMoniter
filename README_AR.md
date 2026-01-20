<div dir="rtl" lang="ar">

# 📡 Rik's Blog Monitor (مراقب تحديثات المدونة)

[![GitHub Actions Status](https://github.com/zhuyikai2002/MyPythonMoniter/actions/workflows/daily_check.yml/badge.svg)](https://github.com/zhuyikai2002/MyPythonMoniter/actions)

---

**🌍 اللغات / Languages / 语言 / 言語:**

[English](./README_EN.md) | [简体中文](./README.md) | [日本語](./README_JA.md) | [العربية](./README_AR.md)

---

> 💡 مشروع بارز في الانتقال من Linux/C المدمج إلى أتمتة Python

مشروع أتمتة Python مستوحى من "لوحة Qinglong + إشعارات DingTalk"، تم تطويره على Mac Mini. يحقق مراقبة تحديثات المدونة بدون خادم من خلال GitHub Actions، مع دمج ServerChan لإشعارات WeChat الفورية.

## ✨ الميزات الأساسية

- 🎯 **مراقبة ذكية**: اكتشاف تلقائي للتحديثات على مدونة [qzkj.ltd](https://qzkj.ltd/blog)
- 🛡️ **تجاوز جدار الحماية**: استخدام `cloudscraper` لتجاوز حماية Cloudflare (يحل مشكلة 403)
- ⏰ **مهام مجدولة**: يعمل GitHub Actions تلقائيًا كل ساعة، دون الحاجة لصيانة خادم
- 📲 **إشعارات WeChat**: متكامل مع ServerChan لإشعارات WeChat الفورية عند تحديث المدونة
- 🔒 **منع الأعطال**: معالجة الاستثناءات المدمجة لمنع أخطاء Git commit

## 🛠️ المجموعة التقنية

| التقنية | الإصدار | الغرض |
|---------|---------|-------|
| **Python** | 3.9+ | بيئة التشغيل الأساسية |
| **cloudscraper** | الأحدث | تجاوز حماية Cloudflare |
| **BeautifulSoup4** | الأحدث | تحليل HTML واستخراج البيانات |
| **GitHub Actions** | - | جدولة المهام التلقائية |
| **ServerChan** | API v3 | دفع رسائل WeChat |

## 📦 هيكل المشروع

</div>

```
MyPythonMoniter/
├── monitor.py         # برنامج المراقبة الرئيسي (الإنتاج)
├── spider.py          # سكريبت اختبار الزاحف
├── notify.py          # سكريبت اختبار ServerChan
├── last_title.txt     # تخزين العنوان الأخير المكتشف
└── README.md          # وثائق المشروع
```

<div dir="rtl" lang="ar">

## 🚀 البدء السريع

### 1. إعداد البيئة

تأكد من تثبيت Python 3.9 أو أحدث:

</div>

```bash
python --version
```

<div dir="rtl" lang="ar">

### 2. تثبيت التبعيات

</div>

```bash
pip install cloudscraper beautifulsoup4 requests
```

<div dir="rtl" lang="ar">

### 3. الاختبار المحلي

</div>

```bash
# تشغيل برنامج المراقبة الرئيسي
python monitor.py

# اختبار وظيفة الزاحف
python spider.py

# اختبار إشعارات WeChat
python notify.py
```

<div dir="rtl" lang="ar">

### 4. نشر GitHub Actions

#### 4.1 تكوين Secret

أضف Secret في مستودع GitHub:

- انتقل إلى `Settings` ← `Secrets and variables` ← `Actions`
- أضف `SERVER_KEY` مع قيمة SCKEY الخاصة بـ ServerChan

#### 4.2 إنشاء Workflow

قم بإنشاء `.github/workflows/daily_check.yml` في جذر المشروع:

</div>

```yaml
name: Blog Monitor

on:
  schedule:
    - cron: '0 * * * *'  # تشغيل كل ساعة
  workflow_dispatch:      # دعم التشغيل اليدوي

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install Dependencies
        run: |
          pip install cloudscraper beautifulsoup4 requests
      
      - name: Run Monitor
        env:
          SERVER_KEY: ${{ secrets.SERVER_KEY }}
        run: |
          python monitor.py
      
      - name: Commit Changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add last_title.txt
          git diff --quiet && git diff --staged --quiet || git commit -m "Update last_title.txt"
          git push || true
```

<div dir="rtl" lang="ar">

## 🎨 المنطق الأساسي

### آلية تجاوز جدار الحماية

</div>

```python
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)
```

<div dir="rtl" lang="ar">

تجاوز التحقق من تحدي JavaScript الخاص بـ Cloudflare بنجاح من خلال التنكر كمتصفح Chrome.

### تدفق اكتشاف التحديثات

1. جلب الصفحة الرئيسية للمدونة باستخدام `cloudscraper`
2. تحليل عنوان المقال الأحدث باستخدام BeautifulSoup
3. المقارنة مع السجل في `last_title.txt`
4. دفع إشعار WeChat عبر ServerChan عند اكتشاف التحديث
5. تحديث ملف السجل المحلي

## 📝 التكوين

قم بتحرير قسم التكوين في `monitor.py`:

</div>

```python
BLOG_URL = "https://qzkj.ltd/blog"        # عنوان URL للمدونة المراقبة
SERVER_KEY = os.getenv("SERVER_KEY")      # ServerChan SCKEY
RECORD_FILE = "last_title.txt"            # مسار ملف السجل
```

<div dir="rtl" lang="ar">

## 🔧 الأسئلة الشائعة

### س: مواجهة أخطاء 403؟
**ج**: هذا بالضبط ما يحله `cloudscraper`. تأكد من تثبيت المكتبة بشكل صحيح.

### س: لا تستلم إشعارات WeChat؟
**ج**: تحقق من تكوين متغير البيئة `SERVER_KEY` بشكل صحيح.

### س: GitHub Actions لا يعمل؟
**ج**: تحقق من صحة تعبير cron، أو قم بتشغيل workflow_dispatch يدويًا.

## 📊 حالة التشغيل

عرض أحدث نتائج المراقبة:
- ✅ المقال المراقب حاليًا: `كنت أريد فقط كتابة سيرة ذاتية، لكنني انتهيت بإعادة هيكلة الموقع بالكامل`

## 🎯 الخطط المستقبلية

- [ ] دعم مراقبة مصادر مدونات متعددة
- [ ] إضافة قنوات دفع DingTalk و WeCom وغيرها
- [ ] تنفيذ لوحة تحكم ويب
- [ ] دعم تردد مراقبة مخصص

## 📄 الترخيص

هذا المشروع للاستخدام الشخصي والبحثي فقط.

---

</div>

<div align="center">
  <strong>Created by Rik in 2026</strong>
  <br>
  <sub>🚀 من مهندس الأنظمة المدمجة إلى رحلة أتمتة Python</sub>
</div>
