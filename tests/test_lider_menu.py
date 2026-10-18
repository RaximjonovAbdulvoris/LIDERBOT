from datetime import datetime, timezone
import os
import unittest
from unittest.mock import patch
from telegram import Chat, Message, Update
from bot.handlers import start, driver, brand
from bot.premium_emoji import premium_keyboard


class LiderMenuTests(unittest.TestCase):
    def test_premium_button_labels_reach_all_three_original_handlers(self):
        with patch.dict(os.environ, {f'PREMIUM_ICON_{key}': '12345' for key in ('DRIVER', 'BRAND', 'PAYOUT')}):
            # The keyboard is built once at import; build buttons under the same
            # runtime icon configuration, then test the actual serialized labels.
            from bot.presentation import menu_button
            from telegram import ReplyKeyboardMarkup
            keyboard = ReplyKeyboardMarkup([[menu_button(text, icon=icon)] for text, icon in [
                (start.MENU_DRIVER, 'DRIVER'), (start.MENU_BRAND, 'BRAND'), (start.MENU_PAYOUT, 'PAYOUT')]])
            payload = premium_keyboard(keyboard)['keyboard']
        handlers = [driver.build_driver_conversation().entry_points[0],
                    brand.build_brand_conversation().entry_points[0], start.build_payout_handler()]
        for row, handler in zip(payload, handlers):
            msg = Message(1, datetime.now(timezone.utc), Chat(123, 'private'), text=row[0]['text'])
            self.assertTrue(handler.check_update(Update(1, message=msg)))

    def test_startup_constructs_all_handlers_without_network(self):
        from telegram.ext import Application, DictPersistence
        from bot.main import register_handlers
        from bot.premium_emoji import PremiumEmojiBot
        app = Application.builder().bot(PremiumEmojiBot('123:offline')).persistence(DictPersistence()).build()
        register_handlers(app)
        self.assertTrue(app.handlers)
        self.assertEqual(app.handlers[0][0].name, 'application_form')

    def test_private_forms_never_capture_operator_group_messages(self):
        msg = Message(1, datetime.now(timezone.utc), Chat(-1001, 'supergroup'), text=start.MENU_DRIVER)
        self.assertFalse(driver.build_driver_conversation().entry_points[0].check_update(Update(1, message=msg)))
