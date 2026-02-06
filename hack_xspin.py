from telethon import TelegramClient, events
import asyncio

# ================= TELEGRAM SOZLAMALARI =================
api_id = 38288862
api_hash = "8cf6fe5caf01d81cc363c3278572f6a7"
session_name = "userbot_session"

TARGET_GROUP = "xspin_razgon_gruppa"

# ================= O‘YIN SOZLAMALARI ==================
START_BALANCE = 44_384_506
TARGET_BALANCE = 10_000_000_000
MAX_LOSSES = 10
PROGRESSION = 3

# ================= GLOBAL HOLAT =======================
balance = START_BALANCE
current_bet = None
losses = 0
round_counter = 0
cycle_active = False

# =====================================================

def calculate_start_bet(balance: int) -> int:
    total_multiplier = (PROGRESSION ** MAX_LOSSES - 1) // (PROGRESSION - 1)
    bet = balance // total_multiplier
    return max(bet, 1)


client = TelegramClient(session_name, api_id, api_hash)


async def start_cycle():
    global current_bet, losses, cycle_active, round_counter
    current_bet = calculate_start_bet(balance)
    losses = 0
    round_counter = 0
    cycle_active = True
    print(f"✅ Avtomatik sikl boshlandi | Boshlang‘ich stavka: {current_bet:,} | Balans: {balance:,}")

    # Guruhga !б [summa] yozish
    await client.send_message(TARGET_GROUP, f"!б {current_bet}")


@client.on(events.NewMessage(chats=TARGET_GROUP))
async def dice_reader(event):
    global balance, current_bet, losses, round_counter, cycle_active

    if not cycle_active:
        return

    # Faqat reply bo‘lsa va dice bo‘lsa
    if not event.reply_to_msg_id or not event.dice:
        return

    original = await event.get_reply_message()
    if not original or not original.text:
        return

    # Faqat !б reply bo‘lsa
    if not original.text.startswith("!б"):
        return

    roll = event.dice.value
    round_counter += 1

    # Stavkani yechish
    if current_bet > balance:
        print("[STOP] Balans yetarli emas. Sikl to‘xtatildi.")
        cycle_active = False
        return

    balance -= current_bet

    # Natija
    if roll in (1, 2, 3):
        losses += 1
        result = "YUTQAZDI"
        print(
            f"[RAUND {round_counter}] Dice: {roll} | {result} | "
            f"Yutqazishlar: {losses}/{MAX_LOSSES} | "
            f"Stavka: {current_bet:,} | Balans: {balance:,}"
        )

        if losses >= MAX_LOSSES:
            print("[SIKL RESET] Maksimal yutqazishlar yetildi.")
            current_bet = calculate_start_bet(balance)
            losses = 0
        else:
            current_bet *= PROGRESSION

    elif roll == 4:
        win = current_bet * 2
        balance += win
        result = "YUTDI (2x)"
        print(f"[RAUND {round_counter}] Dice: {roll} | {result} | Yutuq: {win:,} | Balans: {balance:,}")
        current_bet = calculate_start_bet(balance)
        losses = 0
    else:  # roll == 5
        win = current_bet * 3
        balance += win
        result = "YUTDI (3x)"
        print(f"[RAUND {round_counter}] Dice: {roll} | {result} | Yutuq: {win:,} | Balans: {balance:,}")
        current_bet = calculate_start_bet(balance)
        losses = 0

    # Agar balans target ga yetgan bo‘lsa
    if balance >= TARGET_BALANCE:
        print(f"[MAQSAD] TARGET ga yetildi: {balance:,}")
        cycle_active = False
        return

    # Keyingi stavka uchun 2 sekund kutib !б [summa] yuborish
    await asyncio.sleep(2)
    await client.send_message(TARGET_GROUP, f"!б {current_bet}")


async def main():
    await client.start()
    print("Userbot ishga tushdi. Avtomatik stavkalar boshlanishi kutilyapti...")
    await start_cycle()
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
