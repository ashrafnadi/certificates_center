# نظام بداية لإدارة مركز الشهادات | Bidaya Certificate Center Management System

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0.7-green?logo=django" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap" alt="Bootstrap">
  <img src="https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

<p align="center">
  <strong>نظام متكامل لإدارة مركز الشهادات والخريجين بجامعة بنها</strong><br>
  <em>An integrated system for managing the Certificate Center and Graduates at Banha University</em>
</p>

---

## 📋 المحتويات | Table of Contents

- [نظرة عامة | Overview](#-نظرة-عامة--overview)
- [المميزات | Features](#-المميزات--features)
- [التقنيات المستخدمة | Tech Stack](#-التقنيات-المستخدمة--tech-stack)
- [متطلبات التشغيل | Requirements](#-متطلبات-التشغيل--requirements)
- [التثبيت والتشغيل | Installation](#-التثبيت-والتشغيل--installation)
- [متغيرات البيئة | Environment Variables](#-متغيرات-البيئة--environment-variables)
- [هيكل المشروع | Project Structure](#-هيكل-المشروع--project-structure)
- [الأدوار والصلاحيات | Roles & Permissions](#-الأدوار-والصلاحيات--roles--permissions)
- [الاستخدام | Usage](#-الاستخدام--usage)
- [الشاشات | Screenshots](#-الشاشات--screenshots)
- [المساهمة | Contributing](#-المساهمة--contributing)
- [التواصل | Contact](#-التواصل--contact)

---

## 🔭 نظرة عامة | Overview

**نظام بداية** هو تطبيق ويب متكامل مبني على إطار عمل Django، مصمم خصيصًا لإدارة مركز الشهادات بجامعة بنها. يتيح النظام:

- إدارة بيانات الخريجين والشهادات
- طباعة الشهادات بصيغة PDF
- التحكم في الوصول بناءً على الأدوار الوظيفية
- إدارة الكليات والتخصصات والدرجات العلمية
- تتبع العمليات والتعديلات (Audit Trail)
- تصدير البيانات إلى Excel

**Bidaya** is a comprehensive Django web application designed specifically for managing the Certificate Center at Banha University.

---

## ✨ المميزات | Features

| الميزة | Feature | الوصف | Description |
|--------|---------|-------|-------------|
| 🔐 | Authentication | نظام دخول مخصص بأدوار متعددة | Custom login system with multiple roles |
| 📱 | Responsive | تصميم متجاوب يعمل على جميع الأجهزة | Fully responsive design for all devices |
| 🌙 | Dark Mode | دعم الوضع الليلي والنهاري | Light/Dark theme switcher |
| 🎓 | Graduates | إدارة بيانات الخريجين | Graduate data management |
| 📄 | Certificates | طباعة وإصدار الشهادات | Certificate printing & issuance |
| 🏛️ | Faculties | إدارة الكليات والتخصصات | Faculty & specialization management |
| 📊 | Reports | تقارير وإحصائيات | Reports & statistics |
| 📤 | Export | تصدير البيانات إلى Excel | Excel data export |
| 📝 | Audit Trail | سجل العمليات والتعديلات | Operation & modification history |
| 🖨️ | PDF | طباعة الشهادات بصيغة PDF | PDF certificate generation (WeasyPrint) |

---

## 🛠️ التقنيات المستخدمة | Tech Stack

### Backend
- **Django 6.0.7** — Web framework
- **Python 3.12+** — Programming language
- **PostgreSQL** — Primary database (production)
- **SQLite** — Fallback database (development)
- **Gunicorn** — WSGI HTTP Server

### Frontend
- **Bootstrap 5.3** — CSS framework (RTL support)
- **Django Crispy Forms** — Form rendering
- **Django HTMX** — Dynamic UI updates
- **Bootstrap Icons** — Icon library

### Tools & Libraries
- **WeasyPrint** — PDF generation
- **openpyxl** — Excel export
- **python-decouple** — Environment configuration
- **WhiteNoise** — Static files serving
- **Django Debug Toolbar** — Development debugging

---

## 📦 متطلبات التشغيل | Requirements

- Python 3.12 أو أعلى
- PostgreSQL 14+ (للإنتاج) أو SQLite (للتطوير)
- Git

---

## 🚀 التثبيت والتشغيل | Installation

### 1. استنساخ المستودع | Clone the repository

```bash
git clone https://github.com/ashrafnadi/certificates_center.git
cd certificates_center
```

### 2. إنشاء بيئة افتراضية | Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. تثبيت المتطلبات | Install requirements

```bash
pip install -r requirements.txt
```

### 4. إنشاء ملف البيئة | Create environment file

أنشئ ملف `.env` في المجلد الرئيسي:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL) - Optional for development
DB_NAME=certificates_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

> **ملاحظة:** إذا لم تُحدد متغيرات قاعدة البيانات، سيتم استخدام SQLite تلقائيًا.

### 5. تهيئة قاعدة البيانات | Database setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. جمع الملفات الثابتة | Collect static files

```bash
python manage.py collectstatic
```

### 7. تشغيل الخادم | Run the server

```bash
python manage.py runserver
```

افتح المتصفح على: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔧 متغيرات البيئة | Environment Variables

| المتغير | الوصف | الافتراضي | Required |
|---------|-------|-----------|----------|
| `SECRET_KEY` | مفتاح التشفير | — | ✅ نعم |
| `DEBUG` | وضع التصحيح | `False` | ❌ لا |
| `ALLOWED_HOSTS` | النطاقات المسموحة | `*` | ❌ لا |
| `DB_NAME` | اسم قاعدة البيانات | — | ❌ لا |
| `DB_USER` | مستخدم قاعدة البيانات | — | ❌ لا |
| `DB_PASSWORD` | كلمة مرور قاعدة البيانات | — | ❌ لا |
| `DB_HOST` | عنوان الخادم | `localhost` | ❌ لا |
| `DB_PORT` | منفذ الاتصال | `5432` | ❌ لا |

---

## 📁 هيكل المشروع | Project Structure

```
certificates_center/
├── core/                      # إعدادات المشروع الرئيسية
│   ├── settings.py            # الإعدادات
│   ├── urls.py                # التوجيه الرئيسي
│   ├── wsgi.py                # WSGI
│   ├── asgi.py                # ASGI
│   └── context_processors.py  # معالجات السياق
│
├── apps/
│   ├── administration/        # إدارة المستخدمين والمصادقة
│   │   ├── models.py          # النماذج (users_profile, faculty, ...)
│   │   ├── views.py           # عرض تسجيل الدخول/الخروج
│   │   ├── forms.py           # نماذج الدخول
│   │   ├── backends.py        # مصادقة مخصصة
│   │   └── urls.py            # روابط التطبيق
│   │
│   └── graduate/              # إدارة الخريجين والشهادات
│       ├── models.py          # النماذج (graduate, certificate, ...)
│       ├── views.py           # العروض
│       └── urls.py            # الروابط
│
├── templates/                 # قوالب HTML
│   ├── base.html              # القالب الأساسي
│   ├── administration/
│   │   ├── login.html         # صفحة الدخول
│   │   └── partials/
│   └── graduate/
│       └── index.html         # الصفحة الرئيسية
│
├── static/                    # الملفات الثابتة
│   ├── css/
│   │   └── custom.css         # التنسيقات المخصصة
│   └── js/
│       └── custom.js          # السكربتات المخصصة
│
├── manage.py                  # أداة إدارة Django
├── requirements.txt           # المتطلبات
└── .env                       # متغيرات البيئة (لا تُرفع)
```

---

## 👥 الأدوار والصلاحيات | Roles & Permissions

| الدور | Role | الصلاحيات | Permissions |
|-------|------|-----------|-------------|
| 🦸‍♂️ | **مدير** (Director) | صلاحيات كاملة | Full access |
| 👮‍♂️ | **مشرف** (Supervisor) | إدارة ومراقبة | Management & monitoring |
| 🔍 | **مدقق** (Auditor) | مراجعة البيانات | Data auditing (requires faculty) |
| 👨‍💼 | **موظف** (Employee) | إدخال وتحديث | Data entry & updates (requires faculty) |

> **ملاحظة:** المدققون والموظفون ملزمون باختيار الكلية عند تسجيل الدخول.

---

## 📖 الاستخدام | Usage

### تسجيل الدخول
1. افتح `/login/`
2. أدخل اسم المستخدم وكلمة المرور
3. اختر الكلية (إذا كان الدور يتطلب ذلك)
4. اضغط "تسجيل الدخول"

### تبديل المظهر
- اضغط على أيقونة 🌙/☀️ في الشريط العلوي للتبديل بين الوضع الليلي والنهاري.

### إخفاء/إظهار القائمة
- **الجوال:** اضغط على ☰ لفتح/إغلاق القائمة الجانبية.
- **سطح المكتب:** اضغط على ☰ لطي/توسيع القائمة.

---

## 📸 الشاشات | Screenshots

> *سيتم إضافة لقطات الشاشة قريبًا...*

| صفحة الدخول | لوحة التحكم | إدارة الخريجين |
|-------------|-------------|----------------|
| 🖼️ Login | 🖼️ Dashboard | 🖼️ Graduates |

---

## 🤝 المساهمة | Contributing

نرحب بالمساهمات! يرجى اتباع الخطوات التالية:

1. Fork المستودع
2. أنشئ فرعًا جديدًا (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

---

## 📄 الترخيص | License

هذا المشروع مرخص بموجب **MIT License**.  
انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

## 📞 التواصل | Contact

**شركة بداية لتسويق خدمات جامعة بنها**  
Bidaya Company for Marketing Banha University Services

- 📧 البريد الإلكتروني: *(لم يُحدد)*
- 🌐 الموقع: *(لم يُحدد)*
- 💻 المطور: [ashrafnadi](https://github.com/ashrafnadi)

---

<p align="center">
  <sub>© 2026 شركة بداية لتسويق خدمات جامعة بنها. جميع الحقوق محفوظة.</sub><br>
  <sub>© 2026 Bidaya Company for Marketing Banha University Services. All rights reserved.</sub>
</p>
