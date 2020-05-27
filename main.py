import kivy.app
import kivy.uix.button
import kivy.uix.label
import  kivy.uix.boxlayout
import kivy.uix.gridlayout
import kivy.uix.textinput
import math
from kivy.core.window import Window
import kivy.uix.dropdown
import time
import datetime
import kivy.uix.popup

class MyApp(kivy.app.App):


    def build(self):
        Window.clearcolor = (.88, .53, .0, 1)
        self.P_input = kivy.uix.textinput.TextInput()
        self.dot1_input = kivy.uix.textinput.TextInput()
        self.dot2_input = kivy.uix.textinput.TextInput()
        self.learning_input = kivy.uix.textinput.TextInput()
        global bl
        bl = kivy.uix.boxlayout.BoxLayout(orientation="vertical", padding = 20, spacing=3)
        bl.add_widget(kivy.uix.label.Label(text=" Лабораторна робота №3.2. Модель Perceptron"))
        bl.add_widget(kivy.uix.label.Label(text="Введіть поріг спрацювання P: "))
        bl.add_widget(self.P_input)
        bl.add_widget(kivy.uix.label.Label(text="Введіть координати першої точки: "))
        bl.add_widget(self.dot1_input)
        bl.add_widget(kivy.uix.label.Label(text="Введіть координати другої точки: "))
        bl.add_widget(self.dot2_input)
        bl.add_widget(kivy.uix.label.Label(text="Введіть швидкість навчання δ: "))
        bl.add_widget(self.learning_input)
        bl.add_widget(kivy.uix.label.Label(text="Оберіть дедлайн "))
        self.drop = kivy.uix.dropdown.DropDown()
        self.drop1 = kivy.uix.button.Button(text = "Часовий", size_hint_y=None, height=30)
        self.drop1.bind(on_release=lambda btn: self.drop.select(self.drop1.text))
        self.drop.add_widget(self.drop1)
        self.drop2 = kivy.uix.button.Button(text="Кількість ітерацій", size_hint_y=None, height=30)
        self.drop2.bind(on_release=lambda btn: self.drop.select(self.drop2.text))
        self.drop.add_widget(self.drop2)
        self.choose_button = kivy.uix.button.Button(text="Натисніть, щоб обрати дедлайн", size_hint=(0.4, 0.8))
        self.choose_button.bind(on_release=self.drop.open)
        self.drop.bind(on_select=lambda instance, x: setattr(self.choose_button, 'text', x))
        bl.add_widget(self.choose_button)
        bl.add_widget(kivy.uix.label.Label(text = "Введіть час виконання або кількість ітерацій"))
        self.deadline = kivy.uix.textinput.TextInput()
        bl.add_widget(self.deadline)
        bl.add_widget(kivy.uix.button.Button(text = " Почати виконання", on_press = self.Perceptron))
        self.result_label = kivy.uix.label.Label(text = "Результат виконання")
        bl.add_widget(self.result_label)
        #bl.add_widget(kivy.uix.button.Button(text="Вивести кількість ітерацій", on_press = self.show_popup))



        return bl


    def Perceptron(self, r):
        P = int(self.P_input.text)
        dot1 = self.dot1_input.text
        dot1_1, dot1_2 = dot1.split(",")
        dot1_1, dot1_2 = int(dot1_1), int(dot1_2)
        dot2 = self.dot2_input.text
        dot2_1, dot2_2 = dot2.split(",")
        dot2_1, dot2_2 = int(dot2_1), int(dot2_2)
        G = float(self.learning_input.text)
        deadline = float(self.deadline.text)
        deadline_type = getattr(self.choose_button, 'text')
        print(P,dot1,dot2,G,deadline_type,deadline, dot1_1, dot1_2,dot2_1,dot2_2)

        W1, W2 = 0, 0

        if deadline_type == 'Часовий':
            self.deadline = datetime.timedelta(seconds=deadline)
            self.deadline_type = deadline_type
        elif deadline_type == 'Кількість ітерацій':
            self.deadline = deadline
            self.deadline_type = deadline_type



        start_exec_time = time.time()
        if self.deadline_type == 'time':
            start = datetime.datetime.start()
            end = start + self.deadline
        else:
            start = 0
            end = self.deadline
        count = 1
        success = 0
        y = W1 * dot1_1 + W2 * dot1_2
        if y > P:
            success += 1
        delta = P - y
        W1 = W1 + delta * dot1_1 * G
        W2 = W2 + delta * dot1_2 * G

        while start != end:
            if count % 2 != 0:
                y = W1 * dot1_1 + W2 * dot1_2
                delta = P - y
                W1 = W1 + delta * dot1_1 * G
                W2 = W2 + delta * dot1_2 * G
                if y > P:
                    success += 1
                if success == 2:
                    break
                count+=1
            elif count %2 == 0:
                y = W1 * dot2_1 + W2 * dot2_2
                delta = P - y
                W1 = W1 + delta * dot2_1 * G
                W2 = W2 + delta * dot2_2 * G
                if y > P:
                    success += 1
                if success == 2:
                    break
                count+=1
        print(count)
        end_exec_time = time.time()
        self.exec_time = end_exec_time - start_exec_time
        self.result_label.text = "Для точок ({},{}) ({},{}).\n Поріг спрацювання P = {}, швидкість навчання δ = {}, W1 = {}, W2= {}".format(dot1_1,dot1_2,dot2_1,dot2_2,P,G,W1,W2)





        popup = kivy.uix.popup.Popup(title='Кількість ітерацій',
                                     content=kivy.uix.label.Label(text='Кількість ітерацій: {}'.format(count)),
                                     size_hint=(None, None), size=(400, 400))
        popup.open()




if __name__ == "__main__":
    app = MyApp()
    app.run()