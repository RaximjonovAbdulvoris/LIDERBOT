# LIDER TAXI Telegram bot

Python 3.11+ va python-telegram-bot 21.6.

## Ishga tushirish

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .env ichiga BotFather tokenini kiriting.
mkdir -p runtime
set -a
. ./.env
set +a
python -m bot.main
```

Hostingda Build command: `pip install -r requirements.txt`.
Start command: `python -m bot.main`. Bot long polling bilan ishlaydi:
bitta token uchun faqat bitta process/worker ishlating. HTTP port talab
qiluvchi web service o'rniga background worker ishlating.

Hosting environment sozlamalariga `.env.example` dagi qiymatlar va
`TELEGRAM_BOT_TOKEN` ni kiriting. `.env` avtomatik o'qilmaydi.
`PERSIST_DIR` mavjud, yozish mumkin bo'lgan doimiy disk papkasi bo'lsin.
GitHub orqali token va eski bot holati tarqatilmaydi.

## Guruhlardagi boshqaruv

- Arizalar 01 va 02 guruhlariga navbat bilan tushadi.
- Asosiy guruhlar: Tayyor, Chala rasm, Boshqa park, Jarayonda.
- Chala rasm / Boshqa park: Tayyor, O'chirish, Jarayonda.
- Jarayonda avval qizil, bosilganda sariq; boshqa guruhga o'tganda qizil.
- Tayyor: arxivga tugmalarsiz ko'chirish, keyin eski xabarlarni o'chirish.
- O'chirish: maxsus guruhdagi arizani arxivlamasdan o'chirish.
- To'liq ko'chirish tasdiqlanmasa, asl ariza o'chirilmaydi.
- Bot barcha tegishli guruhlarda xabar/rasm yuborish va xabarlarni o'chirish
  huquqiga ega bo'lishi kerak. Telegram eski xabarlarni o'chirishni cheklashi mumkin.

## Tekshirish

```bash
python -m unittest discover -s tests -v
```

Testlar Telegramga ulanmaydi. Ommaviy ishga tushirishdan oldin har ikkala
asosiy guruhga sinov arizasi yuborib, Chala rasm, Boshqa park, Jarayonda,
Tayyor va O'chirish yo'llarini haqiqiy guruhlarda tekshiring.

## Updated driver workflow

Local document OCR, encrypted state migration, ZIP downloads, progress toggles and administrator-only controls are included. The menu remains Ulanish / Brend / Pul yechish; Brand stays a plain message. See [LIDER_UPGRADE.md](LIDER_UPGRADE.md) for deployment, existing-record compatibility and privacy/accuracy limits.
