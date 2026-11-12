# Manufacturing Production Planning System

Ishlab chiqarish jarayonlarini rejalashtirish va boshqarish uchun Flask asosidagi akademik MVP.

## Imkoniyatlar
- Dashboard statistikasi
- Mahsulotlar katalogi (qo‘shish/o‘chirish)
- Ishlab chiqarish rejalari va bajarilgan miqdorni yangilash
- Xomashyo qoldiqlari va minimal zaxira ogohlantirishi
- Buyurtmalarni ro‘yxatga olish
- Scikit-learn Linear Regression yordamida namunaviy prognoz

## Texnologiyalar
Python, Flask, SQLite, HTML5, CSS3, JavaScript, Chart.js, NumPy, Scikit-learn.

## O‘rnatish
Python 3.10 yoki undan yangisini o‘rnating.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Brauzerda `http://127.0.0.1:5000` manzilini oching.

## Muhim izoh
Bu boshlang‘ich MVP. Prognoz moduli namoyish uchun sun’iy ma’lumotdan foydalanadi; haqiqiy korxona prognozi uchun tekshirilgan tarixiy ishlab chiqarish ma’lumotlari bilan qayta o‘qitish zarur. Production muhitida `secret_key`, autentifikatsiya, CSRF himoyasi, migratsiyalar, audit log va PostgreSQL sozlanishi kerak.

## Keyingi rivojlantirish bosqichlari
- Login va rollarga asoslangan ruxsatlar
- Ombor kirim-chiqim tranzaksiyalari
- Xomashyo sarfini BOM (Bill of Materials) asosida avtomatik hisoblash
- Ishchilar va uskunalar modullari
- PDF/Excel hisobotlari
- PlantUML diagrammalari va bulutga joylashtirish
