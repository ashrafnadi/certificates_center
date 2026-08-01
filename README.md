# نظام بداية لإدارة مركز الشهادات | Bidaya Certificate Center Management System

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0.7-green?logo=django" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python" alt="Python">
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
- [الترخيص | License](#-الترخيص--license)
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


| الميزة | Feature        | الوصف                                                      | Description                             |
| -------------- | ---------------- | ----------------------------------------------------------------- | ----------------------------------------- |
| 🔐           | Authentication | نظام دخول مخصص بأدوار متعددة            | Custom login system with multiple roles |
| 📱           | Responsive     | تصميم متجاوب يعمل على جميع الأجهزة | Fully responsive design for all devices |
| 🌙           | Dark Mode      | دعم الوضع الليلي والنهاري                 | Light/Dark theme switcher               |
| 🎓           | Graduates      | إدارة بيانات الخريجين                        | Graduate data management                |
| 📄           | Certificates   | طباعة وإصدار الشهادات                        | Certificate printing & issuance         |
| 🏛️         | Faculties      | إدارة الكليات والتخصصات                    | Faculty & specialization management     |
| 📊           | Reports        | تقارير وإحصائيات                                 | Reports & statistics                    |
| 📤           | Export         | تصدير البيانات إلى Excel                        | Excel data export                       |
| 📝           | Audit Trail    | سجل العمليات والتعديلات                    | Operation & modification history        |
| 🖨️         | PDF            | طباعة الشهادات بصيغة PDF                      | PDF certificate generation (WeasyPrint) |

---

## 🛠️ التقنيات المستخدمة | Tech Stack

### Backend

- **Django 6.0.7** — Web framework
- **Python 3.12+** — Programming language
- **PostgreSQL** — Primary database (production)
- **SQLite** — Fallback database (development)
- **Gunicorn** — WSGI HTTP Server
- **WhiteNoise** — Static files serving (production)

### Frontend

- **Bootstrap 5.3** — CSS framework (RTL support)
- **Django Crispy Forms** — Form rendering
- **Django HTMX** — Dynamic UI updates
- **Bootstrap Icons** — Icon library

### Tools & Libraries

- **WeasyPrint** — PDF generation
- **openpyxl** — Excel export
- **python-decouple** — Environment configuration
- **Pillow** — Image processing
- **Django Debug Toolbar** — Development debugging (DEBUG only)
- **Django Extensions** — Development utilities (DEBUG only)

---

## 📦 متطلبات التشغيل | Requirements

### Python & Tools

- Python 3.12 أو أعلى
- Git

### Database

- PostgreSQL 14+ (للإنتاج)
- SQLite (للتطوير — مدمج مع Python)

### متطلبات نظام WeasyPrint | WeasyPrint System Dependencies

> **⚠️ مهم:** WeasyPrint يحتاج مكتبات نظام لتوليد PDF. قبل التثبيت، تأكد من تثبيت:

**Ubuntu / Debian:**

```bash
sudo apt-get install -y libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev
```

**macOS:**

```bash
brew install pango libffi
```

**Windows:**

> قم بتثبيت [GTK3 for Windows](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases) أولاً.

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
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL) — اختياري للتطوير
DB_NAME=certificates_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

> **⚠️ تحذير:** لا تستخدم `DEBUG=True` في بيئة الإنتاج!
> **🛡️ أمان:** أضف `.env` إلى ملف `.gitignore` لعدم رفعه:
>
> ```bash
> echo ".env" >> .gitignore
> ```

> **ملاحظة:** إذا لم تُحدد متغيرات قاعدة البيانات، سيتم استخدام SQLite تلقائيًا.

### 5. تهيئة قاعدة البيانات | Database setup

```bash
# إنشاء ملفات الهجرة (إذا قمت بتعديل النماذج)
python manage.py makemigrations

# تطبيق الهجرات
python manage.py migrate
```

### 6. إنشاء مستخدم مدير Django | Create Django admin user

> **ملاحظة:** هذا يُنشئ مستخدمًا للوصول إلى لوحة تحكم Django Admin فقط.
> **مستخدمي التطبيق** (المدير، المشرف، المدقق، الموظف) يُدخلون عبر نموذج `users_profile` في قاعدة البيانات.

```bash
python manage.py createsuperuser
```

### 7. تشغيل الخادم | Run the development server

```bash
python manage.py runserver
```

افتح المتصفح على: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🏭 الإنتاج | Production Setup

للنشر في بيئة إنتاج، اتبع الخطوات الإضافية:

```bash
# 1. عطل وضع التصحيح
DEBUG=False

# 2. حدد النطاقات المسموحة
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 3. اجمع الملفات الثابتة
python manage.py collectstatic --noinput

# 4. شغل بـ Gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## 🔧 متغيرات البيئة | Environment Variables


| المتغير  | الوصف                                      | الافتراضي | مطلوب |
| ----------------- | ------------------------------------------------- | -------------------- | ------------ |
| `SECRET_KEY`    | مفتاح التشفير السري            | —                 | ✅ نعم  |
| `DEBUG`         | وضع التصحيح                           | `False`            | ❌ لا    |
| `ALLOWED_HOSTS` | النطاقات المسموحة               | `*`                | ❌ لا    |
| `DB_NAME`       | اسم قاعدة البيانات              | —                 | ❌ لا    |
| `DB_USER`       | مستخدم قاعدة البيانات        | —                 | ❌ لا    |
| `DB_PASSWORD`   | كلمة مرور قاعدة البيانات   | —                 | ❌ لا    |
| `DB_HOST`       | عنوان خادم قاعدة البيانات | `localhost`        | ❌ لا    |
| `DB_PORT`       | منفذ الاتصال                         | `5432`             | ❌ لا    |

---

## 📁 هيكل المشروع | Project Structure

```
certificates_center/
├── core/                          # إعدادات المشروع الرئيسية
│   ├── __init__.py
│   ├── settings.py                # الإعدادات الرئيسية
│   ├── urls.py                    # التوجيه الرئيسي
│   ├── wsgi.py                    # WSGI application
│   ├── asgi.py                    # ASGI application
│   └── context_processors.py      # معالجات السياق العام
│
├── apps/
│   ├── administration/            # إدارة المستخدمين والمصادقة
│   │   ├── __init__.py
│   │   ├── apps.py                # تكوين التطبيق
│   │   ├── models.py              # النماذج (users_profile, faculty, ...)
│   │   ├── views.py               # عروض تسجيل الدخول والخروج
│   │   ├── forms.py               # نماذج تسجيل الدخول
│   │   ├── backends.py            # مصادقة مخصصة
│   │   ├── admin.py               # تكوين Django Admin
│   │   ├── urls.py                # روابط التطبيق
│   │   ├── tests.py               # الاختبارات
│   │   └── migrations/            # ملفات الهجرات
│   │
│   └── graduate/                  # إدارة الخريجين والشهادات
│       ├── __init__.py
│       ├── apps.py                # تكوين التطبيق
│       ├── models.py              # النماذج (graduate, certificate, ...)
│       ├── views.py               # العروض
│       ├── admin.py               # تكوين Django Admin
│       ├── urls.py                # الروابط
│       ├── tests.py               # الاختبارات
│       └── migrations/            # ملفات الهجرات
│
├── templates/                     # قوالب HTML
│   ├── base.html                  # القالب الأساسي (Topbar + Sidebar)
│   ├── administration/
│   │   ├── login.html             # صفحة تسجيل الدخول
│   │   └── partials/
│   │       └── login_form.html    # نموذج الدخول (HTMX)
│   └── graduate/
│       └── index.html             # الصفحة الرئيسية (Dashboard)
│
├── static/                        # الملفات الثابتة (CSS/JS/Images)
│   ├── css/
│   │   └── custom.css             # التنسيقات المخصصة
│   └── js/
│       └── custom.js              # السكربتات المخصصة (Theme + Sidebar)
│
├── media/                         # ملفات المستخدمين المرفوعة
├── backups/                       # مجلد النسخ الاحتياطي
├── logs/                          # سجلات النظام (يُنشأ تلقائيًا)
├── staticfiles/                   # ملفات ثابتة مجمعة (collectstatic)
├── manage.py                      # أداة إدارة Django
├── requirements.txt               # متطلبات Python
├── .env                           # متغيرات البيئة (لا تُرفع)
└── .gitignore                     # ملفات مُستبعدة من Git
```

---

## 👥 الأدوار والصلاحيات | Roles & Permissions


| الدور | Role                      | الصلاحيات            | Permissions                             |
| ------------ | --------------------------- | ------------------------------- | ----------------------------------------- |
| 🦸‍♂️   | **مدير** (Director)   | صلاحيات كاملة     | Full access                             |
| 👮‍♂️   | **مشرف** (Supervisor) | إدارة ومراقبة     | Management & monitoring                 |
| 🔍         | **مدقق** (Auditor)    | مراجعة البيانات | Data auditing (requires faculty)        |
| 👨‍💼     | **موظف** (Employee)   | إدخال وتحديث       | Data entry & updates (requires faculty) |

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
| ----------------------- | ----------------------- | ----------------------------- |
| 🖼️ Login            | 🖼️ Dashboard        | 🖼️ Graduates              |

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
يرجى إضافة ملف `LICENSE` إلى المستودع للاطلاع على النص الكامل.

---

## 📞 التواصل | Contact

**شركة بداية لتسويق خدمات جامعة بنها**Bidaya Company for Marketing Banha University Services

- 📧 البريد الإلكتروني: *(لم يُحدد)*
- 🌐 الموقع: *(لم يُحدد)*
- 💻 المطور: [ashrafnadi](https://github.com/ashrafnadi)

---

<p align="center">
  <sub>© 2026 شركة بداية لتسويق خدمات جامعة بنها. جميع الحقوق محفوظة.</sub><br>
  <sub>© 2026 Bidaya Company for Marketing Banha University Services. All rights reserved.</sub>
</p>
