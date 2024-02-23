import random
from openai import OpenAI
from simple_votings.settings import USE_AI, OPENAI_API_KEY

db_string = '1: "Кружка", 2: "Набор чая", 3: "Оленьи рожки", 4: "Тёплая шапка", 5: "Шарф", 6: "Мармелад", 7: "Имбирные пряники", 8: "Шопер", 9: "Новогодняя открытка", 10: "Свитер", 11: "Букет", 12: "Конфеты с алкоголем", 13: "Браслет", 14: "Кресло-мешок", 15: "Духи", 16: "Сертификат в магазин косметики", 17: "Сироп для кофе", 18: "Халат", 19: "Шёлковая наволочка", 20: "Ароматическая свеча", 21: "Парные украшения", 22: "Валентинка", 23: "Шоколад", 24: "Парные толстовки", 25: "3D светильник", 26: "Мягкая игрушка", 27: "Астропланетарий", 28: "Ортопедическая подушка", 29: "Фрукты в шоколаде", 30: "Мастер‑класс бармена", 31: "Носки", 32: "Пена для бритья", 33: "Бритва", 34: "Ящик кваса", 35: "Шахматы", 36: "Повербанк", 37: "Беспроводная колонка", 38: "Наушники", 39: "Кухонный нож", 40: "Набор отвёрток", 41: "Бенто-торт", 42: "Столик для завтрака", 43: "Набор для выращивания «Лаванда»", 44: "Фотокристалл", 45: "Банка для коктейлей", 46: "Мельница для специй", 47: "Тетрадь на кольцах", 48: "Будильник с пистолетом и мишенью", 49: "Диспенсер для чайных пакетиков", 50: "Перчатки для сенсорного экрана", 51: "Столик для ноутбука", 52: "Плед с рукавами", 53: "Домашние тапочки с подогревом", 54: "USB подогреватель для кружки", 55: "Сумка для ноутбука", 56: "Маска для сна", 57: "Компьютерное кресло", 58: "Гамак для ног под рабочий стол с USB-подогревом", 59: "Абонемент на массаж", 60: "Очки для компьютера", 61: "Валерьянка", 62: "Обложка для зачетки", 63: "Копилка", 64: "Мини-принтер", 65: "Набор кофе", 66: "Картхолдер", 67: "Набор мыла ручной работы", 68: "Ограничитель для книг", 69: "Настольная лампа", 70: "Поход к психологу", 71: "Набор для покера", 72: "Скалка", 73: "Галстук из пупырчатой пленки", 74: "Чайная виселица", 75: "Краски холли", 76: "Игра «Сладкая рулетка»", 77: "Ручка с исчезающими чернилами", 78: "Резиновая змея", 79: "Жвачка-шокер", 80: "Скорпион на пульте управления", 81: "Набор канцелярии", 82: "Планшет", 83: "Посещение аквапарка", 84: "Брелок для поиска ключей", 85: "Умные часы", 86: "Калькулятор", 87: "Доска для рисования светом", 88: "Термос", 89: "Рюкзак", 90: "Пенал"'


def get_random_ans():
    """
    Функция для получения случайных подарков при проблемах с ChatGPT
    :return: Список номеров случайных подарков.
    """
    gifts = db_string.split(', ')
    gift_numbers = [i + 1 for i in range(len(gifts))]
    num_gifts_to_recommend = random.randint(2, min(5, len(gift_numbers)))
    recommended_gifts = random.sample(gift_numbers, num_gifts_to_recommend)
    return recommended_gifts


def recommend_gifts(question_answers):
    """
    Функция для получения рекомендаций подарков с использованием OpenAI ChatGPT
    :param question_answers: Строка с вопросами и ответами
    :return: Список номеров рекомендуемых подарков
    """
    try:
        prompt = f"You are a model that exists to give people happiness. According to the results of the survey, you must find the best gift for a person, you must specify from 2 to 8 varieties of numbers (gift numbers) that best suit this person, based on his answers in the survey. Here are all the existing gifts (numbers: the name of the gifts) {db_string}.\n Where is the result of the survey: {question_answers}. I expect to see a line like '1, 40, 11' from you, if the survey results are empty then answer ' '"
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url="https://api.proxyapi.ru/openai/v1"
        )
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        content = chat_completion['choices'][0]['message']['content']
        recommended_gifts = [int(s.strip()) for s in content.split(',') if s.isdigit()]
        return list(set(recommended_gifts[:]))
    except Exception:
        return get_random_ans()


def chatGPT(text):
    """
    При USE_AI == True вернет список подарков сгенерированным ChatGPT в противном случае результат будет рандомным
    :param text: Строка с вопросами и ответами.
    :return: Список номеров рекомендуемых подарков.
    """
    if USE_AI:
        return recommend_gifts(text)
    else:
        return get_random_ans()


if __name__ == '__main__':
    question_answers = """
    "Вопрос: Что любит получать в подарок?
    Ответ: Любит уютные вещи и чай.
     
    Вопрос: Какие увлечения у этого человека?
    Ответ: Увлекается чтением и садоводством.
     
     
    Вопрос: Какой стиль одежды предпочитает?
    Ответ: Предпочитает классический и комфортный стиль.
     
    Вопрос: Есть ли любимые ароматы или цвета?
    Ответ: Обожает аромат лаванды и синий цвет.
     
     
    Вопрос: Как проводит свободное время?
    Ответ: Любит прогулки на свежем воздухе и встречи с друзьями."
    """
    print(chatGPT(question_answers))
