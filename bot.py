import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

# ================== SOZLAMALAR ==================
import os
BOT_TOKEN = os.getenv"8344495149:AAH_ei-5dHla1qOlgaELJzAv6hM4qMpmKQk"

SPECIALISTS = {
    "EDO.IJRO.UZ": {
        "username": "kmlv_abror",
        "phone": "📞 +998870873669\n📞 +998200140854"
    },
    "E-HUQUQSHUNOS": {
        "username": "kmlv_abror",
        "phone": "📞 +998870873669\n📞 +998200140854"
    },
    "Raqamli Mahalla": {
        "username": "timur0225",
        "phone": "📞 +998932806660"
    },
    "Muddati o‘tgan token va hodim almashtirish": {
        "username": "JDB5959",
        "phone": "📞 +998943235959"
    }
}
# =================================================

class UserState(StatesGroup):
    choose_system = State()

# --------- Klaviaturalar ---------
def phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True
    )

def systems_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗂 EDO.IJRO.UZ")],
            [KeyboardButton(text="⚖️ E-HUQUQSHUNOS")],
            [KeyboardButton(text="🏘 Raqamli Mahalla")],
            [KeyboardButton(text="🔐 Muddati o‘tgan token va hodim almashtirish")]
        ],
        resize_keyboard=True
    )

def actions_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✍️ Mutaxassisga yozish")],
            [KeyboardButton(text="📞 Mutaxassis bilan bog‘lanish")],
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True
    )

# --------- Asosiy bot ---------
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # /start
    @dp.message(F.text == "/start")
    async def start(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Assalomu alaykum!\n"
            "Yordam olish uchun telefon raqamingizni yuboring.",
            reply_markup=phone_keyboard()
        )

    # Telefon qabul qilish
    @dp.message(F.contact)
    async def get_contact(message: Message, state: FSMContext):
        await state.set_state(UserState.choose_system)
        await message.answer(
            "Rahmat!\n\n❓ Qaysi tizim bo‘yicha yordam kerak?",
            reply_markup=systems_keyboard()
        )

    # Barcha tanlovlar shu yerda boshqariladi
    @dp.message(UserState.choose_system)
    async def handle_menu(message: Message, state: FSMContext):
        text = message.text or ""

        # ---- Orqaga ----
        if text == "🔙 Orqaga":
            await message.answer(
                "❓ Qaysi tizim bo‘yicha yordam kerak?",
                reply_markup=systems_keyboard()
            )
            return

        # ---- Tizim tanlash ----
        system = (
            text.replace("🗂 ", "")
                .replace("⚖️ ", "")
                .replace("🏘 ", "")
                .replace("🔐 ", "")
        )

        if system in SPECIALISTS:
            await state.update_data(system=system)
            await message.answer(
                f"✅ {system} bo‘yicha bo‘lim tanlandi.\n"
                "Quyidagilardan birini tanlang:",
                reply_markup=actions_keyboard()
            )
            return

        data = await state.get_data()
        system = data.get("system")

        # ---- Mutaxassisga yozish ----
        if text == "✍️ Mutaxassisga yozish":
            if not system:
                await message.answer("Avval tizimni tanlang.", reply_markup=systems_keyboard())
                return

            username = SPECIALISTS[system]["username"]
            if username:
                await message.answer(f"✍️ Mutaxassisga yozish:\nhttps://t.me/{username}")
            else:
                await message.answer("❗ Bu bo‘lim uchun mutaxassis hali biriktirilmagan.")
            return

        # ---- Mutaxassis bilan bog‘lanish ----
        if text == "📞 Mutaxassis bilan bog‘lanish":
            if not system:
                await message.answer("Avval tizimni tanlang.", reply_markup=systems_keyboard())
                return

            phone = SPECIALISTS[system]["phone"]
            if phone:
                await message.answer(phone)
            else:
                await message.answer("❗ Bu bo‘lim uchun telefon raqam kiritilmagan.")
            return

        await message.answer("Iltimos, menyudagi tugmalardan foydalaning.")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
