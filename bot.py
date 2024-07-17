from vkbottle.bot import Bot, Message
import json
from os import path

bot = Bot(token="t")

data_path = "data.json"

@bot.on.message(text="Добавить <item>")
async def add_task(message: Message, item: str):
    try:
        if path.getsize(data_path) == 0:
            with open(data_path, "w") as data_file:
                json.dump({message.from_id : [item]}, data_file)
        else:
            with open(data_path, "r") as data_file:
                data = json.load(data_file)
            if not(str(message.from_id) in data.keys()):
                data[str(message.from_id)] = [item]
            else:
                data[str(message.from_id)].append(item)
            with open(data_path, "w") as data_file:
                json.dump(data, data_file)
        await message.answer(f"Вы добавили задачу: {item}")
    except:
        return "Ошибка при добавлении"

@bot.on.message(text="Удалить <item>")
async def delete_task(message: Message, item: str):
    try:
        if path.getsize(data_path) == 0:
            return "У вас нет активных задач"
        ntask = int(item)
        with open(data_path, "r") as data_file:
                data = json.load(data_file)
        if not(str(message.from_id) in data.keys()):
            await message.answer("У вас нет активных задач")
        elif ntask < 0 or len(data[str(message.from_id)]) <= ntask or len(data[str(message.from_id)]) < 0:
            await message.answer("У вас нет задачи под таким номером")
        else:
            task = data[str(message.from_id)][ntask]
            data[str(message.from_id)].pop(ntask)
            await message.answer(f"Вы удалили задачу под номером {ntask}: {task}")
            with open(data_path, "w") as data_file:
                json.dump(data, data_file)
    except:
        return "Ошибка при удалении"

@bot.on.message(text="Показать")
async def get_tast(message: Message):
    await message.answer("Выводим список ваших задач:")
    if path.getsize(data_path) == 0:
        return "У вас нет активных задач. Вернитесь к началу"
    with open(data_path, "r") as data_file:
        data = json.load(data_file)
    if not(str(message.from_id) in data.keys()):
        await message.answer("У вас нет активных задач. Вернитесь к началу")
    else:
        await message.answer('\n'.join([f"{str(ntask)}) {data[str(message.from_id)][ntask]}"  for ntask in range(len(data[str(message.from_id)]))]))

@bot.on.message(text="Помощь")
async def help(message: Message):
    await message.answer("Доступные команды:\nДобавить [Содержимое задачи] - добавляет новую задачу в ваш список\nУдалить [Номер задачи] - удаляет задачу под указанным номером из вашего списка\nПоказать - выводит список всех ваших задач\nПомощь - выводит описания всех доступных команд")

bot.run_forever()
