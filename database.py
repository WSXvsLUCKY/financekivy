import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window

#  размер окна
Window.size = (400, 600)

# База данных
conn = sqlite3.connect('finance_app.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT,
    type TEXT
)
''')
conn.commit()


def add_transaction(amount, category, date, type_):
    cursor.execute('''
    INSERT INTO transactions (amount, category, date, type)
    VALUES (?, ?, ?, ?)
    ''', (amount, category, date, type_))
    conn.commit()

def get_balance():
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE type = "income"')
    income = cursor.fetchone()[0] or 0
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE type = "expense"')
    expense = cursor.fetchone()[0] or 0
    return income - expense

def get_transactions():
    cursor.execute('SELECT amount, category, date, type FROM transactions')
    return cursor.fetchall()

# Интерфейс 
class TransactionApp(App):
    def build(self):
        
        root = FloatLayout()

        #  фон
        background = Image(source='back.webp', allow_stretch=True, keep_ratio=False)
        root.add_widget(background

        #
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.9, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # баланс
        self.balance_label = Label(text=f"Баланс: {get_balance()}", font_size=24)
        self.layout.add_widget(self.balance_label)

        # ввод суммы
        self.amount_input = TextInput(hint_text="Введите сумму", multiline=False)
        self.layout.add_widget(self.amount_input)

        # ввод категории
        self.category_input = TextInput(hint_text="Введите категорию", multiline=False)
        self.layout.add_widget(self.category_input)

        # ввод даты
        self.date_input = TextInput(hint_text="Введите дату (ГГГГ-ММ-ДД)", multiline=False)
        self.layout.add_widget(self.date_input)

       
        buttons_layout = BoxLayout(size_hint_y=None, height=50)

        income_button = Button(text="Добавить доход", on_press=self.add_income)
        buttons_layout.add_widget(income_button)

        expense_button = Button(text="Добавить расход", on_press=self.add_expense)
        buttons_layout.add_widget(expense_button)

        # истории транзакций
        history_button = Button(text="Показать историю транзакций", on_press=self.show_history)
        buttons_layout.add_widget(history_button)

        self.layout.add_widget(buttons_layout)

        # макет на экран
        root.add_widget(self.layout)

        
        developer_label = Label(text="Разработчик: Ифтихор Хайдаралиев", font_size=14, size_hint=(0.2, 0.1), pos_hint={'right': 1, 'bottom': 1}, color=(1, 1, 1, 1))
        root.add_widget(developer_label)

        return root

    def add_income(self, instance):
        self.add_transaction('income')

    def add_expense(self, instance):
        self.add_transaction('expense')

    def add_transaction(self, type_):
        amount = float(self.amount_input.text)
        category = self.category_input.text
        date = self.date_input.text
        add_transaction(amount, category, date, type_)
        self.update_balance()
        self.clear_inputs()

    def update_balance(self):
        self.balance_label.text = f"Баланс: {get_balance()}"

    def show_history(self, instance):
        
        transactions = get_transactions()

        # окно с историей
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        for t in transactions:
            transaction_text = f"{t[3].capitalize()} - {t[0]} {t[1]}: {t[2]}"
            content.add_widget(Label(text=transaction_text))

        
        close_button = Button(text="Закрыть", size_hint_y=None, height=50)
        content.add_widget(close_button)

       
        popup = Popup(title='История транзакций', content=content, size_hint=(0.9, 0.9))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def clear_inputs(self):
        self.amount_input.text = ''
        self.category_input.text = ''
        self.date_input.text = ''

if __name__ == '__main__':
    TransactionApp().run()
