# LIDER update

The menu remains Ulanish / Brend / Pul yechish. Existing payout contact details and all original template files are retained. There is no region selection, Spectre, brand approval or Google Sheets. Brand remains a plain text application.

Driver applications read the licence (surname 1, given name 2 without patronymic, birth date/place 3, PINFL 4d, number 5, expiry 4b), and registration certificate series. The passport back is not requested. Missing/conflicting readings remain marked for operator verification. Neither perfect accuracy nor a fixed response time is guaranteed for blurry images or under load.

Applications have a persistent LD-000001 sequence (drivers only), structured copyable fields and a ZIP download button. ZIP contains a driver-named folder. Telegram sends the ZIP as a document; automatic placement into a computer's Downloads folder is controlled by Telegram/client settings. Preparation runs in the background with bounded memory/queues. All source ZIP messages are included in cleanup when moving/deleting/archiving an application.

Main controls: Tayyor, Jarayonda (toggle), Chala rasm, Boshqa park, O‘chirish, ZIP. Review queues: Tayyor, Jarayonda, O‘chirish. Destructive actions require an identifiable group administrator. A complete destination copy must be confirmed before source cleanup. Chala / Boshqa park notices are sent after successful source cleanup. If a driver cannot receive a message (for example, has blocked the bot), the operator group is warned. If Telegram loses a ZIP upload acknowledgement, /zip_boglash (reply to the received ZIP) or /zip_qayta (reply to the card after verifying no ZIP arrived) resolves its uncertain status.

## Existing applications

UUID-keyed LIDER app_messages are normalized on startup without changing message IDs or user IDs. Existing unfinished legacy transfers keep their original checkpoint/handler until cleanup completes. Old UUID buttons remain supported. Old applications did not store reusable photo file IDs, so ZIP/OCR is available for new applications; old archive and queue actions still work. A missing old message can also be subject to Telegram's deletion/edit limitations.

State is migrated from trusted local pickle to authenticated encryption. Keep bot_persistence.pkl AND bot_persistence.key together in private backups; losing the key makes the encrypted state unreadable. OCR subprocesses receive a scrubbed environment and Linux network restrictions. Telegram still transports the submitted documents; group administrators and server access must be controlled.

## Deployment (after reviewing groups)

1. Stop only liderbot-new and privately back up its existing state, environment file(s), and routes. Locate the real state directory via the service's PERSIST_DIR. Do not delete existing state.
2. Pull main into /opt/liderbot-test. Preserve its original template images, token, group IDs and payout contacts.
3. Install system libraries if absent: libseccomp2 libgl1 libglib2.0-0. Install .venv dependencies with `python -m pip install -r requirements.txt -r requirements-ocr.txt`.
4. Run `.venv/bin/python scripts/check_neural_ocr.py`. This uses fictional generated text, not a driver's document.
5. Set DOCUMENT_AI_ENABLED=1, DOCUMENT_OCR_BACKEND=rapid and DOCUMENT_OCR_WORKERS=1 in the service's actual environment file. No AI API key is needed. Keep existing PERSIST_DIR.
6. Configure the six existing route names (DRIVER_GROUP_1, DRIVER_GROUP_2, BRAND_GROUP, CHALA_RASM_GROUP, OTHER_PARK_GROUP, ARCHIVE_GROUP). `python -m bot.configure set --chala_rasm_group=-...` saves local overrides under PERSIST_DIR. `python -m bot.configure check --offline` validates distinct IDs; without --offline it also checks Telegram access using the environment token. The actual service environment must be loaded when running these commands.
7. Restart liderbot-new, confirm Application started, then test one new driver application in each 01/02 group, both review moves, archive, progress toggle and ZIP cleanup. Test Brand separately. Do not launch a second polling process.

Never overwrite group settings or copy another bot's persistence/token/voice ID. The update does not require a counter reset or new regions.
