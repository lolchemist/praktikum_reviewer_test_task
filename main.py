import datetime as dt


class Record:
    # здесь и ниже не помешало бы использовать докстринги для описания класса
    # здесь и ниже непонятно, какие типы данных у параметров классов и функций
    # лучше определить дефолтное значение даты через None
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # в python c заглавной буквы принято именовать классы, а такие переменные как Record - с маленькой
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # условие можно записать в виде 0 <=(today - record.date).days < 7
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # в целом название функции хорошо отражает, хачем она нужна, комментарий излишен
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # стоит использовать более описывающий нейминг
        # например calories_remained вместо х
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Бэкслеши для переносов не применяются.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # else здесь не обязателен, если условие в if будет выполнено, то return, иначе попадет сюда
        else:
            # скобки излишни, лучше убрать
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Лучше изначально задать константу вещественной, ничего же не мешает?)
    # Комментарии здесь по сути перевод имен перемнных, поэтому излишни
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                # это же метод класса, значит можно обратиться через self.USD_RATE, self.EURO_RATE
                                # не стоит передавать эти константы как аргументы
                                # так же в python принято именовать аргументы в lowercase
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # а нельзя ли здесь обойтись без новой переменной? будет проще читать код
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # чтобы не перегружать функцию, лучше вынести обработку валюты в отдельную
        # и рассмотреть случай, когда в нее приходит что-то неизвестное вроде "руб"
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # == возврщает булево значение, которое далее не используется
            cash_remained == 1.00
            currency_type = 'руб'
            # тут бы пустую строку для логического разделения блоков
        if cash_remained > 0:
            # для консистентности стоит определеться будем возвращать обычные или же f-строки
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # можно заменить на else, так ка остальные случаи уже были рассмотрены
        elif cash_remained < 0:
            # вместо взятия отрицательного значения лучше использовать abs()
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # а нужно ли переопределять метод, если он будет работать так же, как родительский? - не стоит
    def get_week_stats(self):
        # тогда уж return:)
        super().get_week_stats()
