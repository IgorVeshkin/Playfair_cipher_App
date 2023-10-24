import tkinter as tk


# Приложения кодирования и декодирования текста с помощью шифра Плейфера

# Функция, переводящая секретный ключ (какое - либо слово или фраза) в диаграммк Плейфера, на основе которой будет
# происходить кодирование и декодирование


def convertPlainTextToDiagraphs(plainText):
    # append X if Two letters are being repeated

    diagrams = []

    # Преобразуем текст в формат, с которым нам будет удобно работать

    plainText = list(plainText.lower().replace(" ", ""))

    # Проходим буквы в цикле через одну
    for s in range(0, len(plainText) + 1, 2):

        # Если на текущей итерации индекс не достиг конца цикла

        if s < len(plainText):

            if s != 0:

                # Если следующий элемент не достиг конца текста

                if s + 1 < len(plainText):

                    # и если текущий и последующий элемент равны

                    if plainText[s + 1] == plainText[s]:
                        # при построении пар букв из шифруемого предложения,
                        # во избежании ошибок вводится стороний элемент x
                        # чтобы на квадрате Плейфера создать пространство для шифрования

                        plainText.insert(s + 1, 'x')

            # Если последующие два элемента не вышли за пределы предложения

            if s + 1 <= len(plainText):

                # спокойно формируем пару из 2 букв

                current_diagrams = ''.join(plainText[s:s + 2])
                diagrams.append(current_diagrams.upper())

            # Иначе, добавляет дополнительный элемент в пару

            else:
                current_diagrams = ''.join(plainText[s:]) + 'x'
                diagrams.append(current_diagrams.upper())

    return diagrams


# Класс, в котором происходит построение интерфейса приложения и логика его изменения


class GUI:
    def __init__(self, gui, alphabet):

        # Задание базовой информации

        self.gui_root = gui
        self.gui_root.title('Playfair cipher v1.0.0 by Igor Veshkin')
        self.gui_root.geometry('520x300')
        self.gui_root.resizable(False, False)

        # Setting up elements on the screen - Построение виджетов в окне

        self.MainFrame = tk.LabelFrame(self.gui_root, text='Playfair cipher')
        self.AlphabetFrame = tk.LabelFrame(self.MainFrame, text='Alphabet')

        # Отдельная переменная класса для хранения английского алфавита

        self.alphabet = alphabet

        # Отдельная переменная класса для хранения сообщения

        self.Message_to_decode = ''
        self.Buttons = []

        iter = 0
        x, y = 0, 0

        # Построение матрицы Плейфера, состоящей из неактивных кнопок библиотеки Tkinter

        for letter in alphabet:
            self.Buttons.append(
                [tk.Button(self.AlphabetFrame, text=letter, state=tk.DISABLED, padx=5, pady=5), x, y, letter, iter])
            self.Buttons[iter][0].place(x=40 * x, y=40 * y, width=40, height=40)
            iter += 1
            x += 1

            # Если ряд заполнен, переходим на следующий

            if x > 4:
                x = 0
                y += 1

        self.SecretKeyFrame = tk.LabelFrame(self.MainFrame, text='Secret key')

        self.number_select_label = tk.Label(self.SecretKeyFrame, text='Key to insert: ')
        self.number_select_entry = tk.Entry(self.SecretKeyFrame)
        self.number_select_entry.insert(tk.END, 'KEYWORD')

        self.EncodeText_Frame = tk.LabelFrame(self.SecretKeyFrame, text='Text to encode: ')
        self.encode_text_Text = tk.Text(self.EncodeText_Frame)
        self.encode_text_Text.insert(tk.END, 'SECRET MESSAGE')

        self.EncodeButton_btn = tk.Button(self.gui_root, text='Encode', state=tk.ACTIVE, padx=5, pady=5,
                                          command=self.Playfair_Cipher_execution)

        self.DecodeButton_btn = tk.Button(self.gui_root, text='Decode', state=tk.ACTIVE, padx=5, pady=5,
                                          command=self.Playfair_Cipher_decode_execution)

        # Placing and showing elements on the screen

        self.MainFrame.place(relx=0.01, rely=0.01, width=510, height=250)
        self.AlphabetFrame.place(relx=0.01, rely=0.01, width=207, height=222)
        self.SecretKeyFrame.place(relx=0.01, rely=0.01, x=207 + 10, width=280, height=222)
        self.EncodeText_Frame.place(relx=0.01, rely=0.01, x=0, y=30, width=260, height=165)

        self.number_select_label.place(relx=0.01, rely=0.01, width=70)
        self.number_select_entry.place(relx=0.01, rely=0.01, x=70 + 10, width=190)

        self.encode_text_Text.place(relx=0.01, rely=0.01, width=250, height=140)
        self.EncodeButton_btn.place(relx=0.805, rely=0.87, width=95)
        self.DecodeButton_btn.place(relx=0.620, rely=0.87, width=95)

    # Функция, отвечающая за подготовку интерфейса и запуск выполнения шифра Плейфера

    def Playfair_Cipher_execution(self):
        # Получаем данные секретного ключа

        key = self.number_select_entry.get()

        # Удаляем пробелы в секретном ключе

        key = ''.join(key.split())

        # Переводим в вверхний регистр

        key = key.upper()

        # Поскольку в матрице построенной из кнопок выше размерность 5x5, а в английском алфавите 26 букв
        # мы заменяем J на I, поскольку эти буквы близки по написанию

        key = key.replace('J', 'I')

        # Создаем модефицированный алфавит

        modified_alphabet = key.upper() + self.alphabet

        # Создаем контрольный алфавит, который будет использоваться при шифрование

        control_alphabet = []

        iter = 0

        # Формируем контрольный алфавит
        # пробегам все элементы модифицированого алфавита

        for letter in modified_alphabet:

            # Если текущей буквы нет в контрольном алфавите, то она будет добавлена
            # Это необходимо для того, чтобы избавиться от повторений в modified_alphabet

            if letter not in control_alphabet:
                control_alphabet.append(letter)
                self.Buttons[iter][0].config(state=tk.NORMAL, text=letter)
                self.Buttons[iter][3] = letter
                self.Buttons[iter][0].config(state=tk.DISABLED)
                iter += 1

        # Считываем сообщение для шифрования из соответсвующего поля интерфейса программы

        Message_to_encode = self.encode_text_Text.get("1.0", 'end-1c')

        # Разбиваем его на пары, диаграмы Плейфера

        DIAGRAPHS = convertPlainTextToDiagraphs(Message_to_encode)

        elem1, elem2 = None, None

        # Пробегаем все пары диаграм

        for current_pair in DIAGRAPHS:

            # Пробегаем все элементы квадрата Плейфера

            for btn_data in self.Buttons:

                # Если первый элемент пары совпал с элементам квадрата (матрицы)

                if btn_data[3] == current_pair[0]:

                    # Выделяем данные в отдельную переменную

                    elem1 = btn_data

                # Если второй элемент пары совпал с элементам квадрата (матрицы)

                elif btn_data[3] == current_pair[1]:

                    # Выделяем данные в отдельную переменную

                    elem2 = btn_data

                if elem1 is not None and elem2 is not None:

                    # Подразделяем каждый элемент на координаты x и y

                    elem1_x = elem1[1]
                    elem1_y = elem1[2]

                    elem2_x = elem2[1]
                    elem2_y = elem2[2]

                    elem1, elem2 = None, None

                    # Если оба элемента не совпали ни по x, ни по y, то получаем квадрат

                    if elem1_x != elem2_x:
                        if elem1_y != elem2_y:

                            # 'SQUARE'

                            # Check 1

                            # Проверяем какой из элементов правее и какой левее, выше и ниже
                            # Если первый элемент находится в вверхнем правом углу квадрата

                            if elem1_x > elem2_x:

                                if elem1_y > elem2_y:

                                    # Буква, которая заменит текущую букву находиться в верхнем левом углу квадрата
                                    # То есть в противоположной стороне того же ряда

                                    new_elem1_x, new_elem1_y = elem2_x, elem1_y

                                    # Путем использования цикла находим данный элемент в матрице Плейфера
                                    # btn_data[1] - координата x,
                                    # btn_data[2] - координата y,
                                    # btn_data[3] - текстовое обозначение буквы,

                                    for btn_data in self.Buttons:
                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:
                                            self.Message_to_decode += btn_data[3]
                                            continue

                                    # Цифруем второй элемент диаграммы

                                    # Второй шифрованый элемент будет в правом нижнем углу квадрата
                                    # То есть в противоположной стороне того же ряда

                                    new_elem2_x, new_elem2_y = elem1_x, elem2_y

                                    # Находим тот же элемент в матрице Плейфера

                                    for btn_data in self.Buttons:
                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:
                                            self.Message_to_decode += btn_data[3]
                                            continue

                                # Если элемент находится в правом нижнем углу квадрата

                                elif elem1_y < elem2_y:

                                    # Первый шифрованный элемент будет в левом нижнем углу
                                    # тот же ряд, противоположная сторона

                                    new_elem1_x, new_elem1_y = elem2_x, elem1_y

                                    # Находим тот же элемент в матрице Плейфера

                                    for btn_data in self.Buttons:
                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:
                                            self.Message_to_decode += btn_data[3]
                                            continue

                                    # Второй шифрованный элемент будет в правом верхнем углу
                                    # тот же ряд, противоположная сторона

                                    new_elem2_x, new_elem2_y = elem1_x, elem2_y

                                    # Находим тот же элемент в матрице Плейфера

                                    for btn_data in self.Buttons:
                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:
                                            self.Message_to_decode += btn_data[3]
                                            continue
                            # Check 2

                            # Дальнейшие вычисления для квадрата идентичны
                            # Каждый элемент из пары получает элемент
                            # из противоположной границы по оси X (на том же ряду)

                            elif elem1_x < elem2_x:

                                if elem1_y > elem2_y:

                                    new_elem1_x, new_elem1_y = elem2_x, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem1_x, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                                elif elem1_y < elem2_y:

                                    new_elem1_x, new_elem1_y = elem2_x, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem1_x, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                        else:
                            # 'HORIZONTAL LINE'

                            # Check 1

                            # В случае если пара образует горизонтальную линию

                            # И следующая x-координата первого элемента пары
                            # И следующая x-координата второго элемента пары не вышли за пределы квадрата 5x5
                            # То есть горизонтальную линию можно сместить на одну координату влево

                            if elem1_x + 1 <= 4:
                                if elem2_x + 1 <= 4:

                                    # То зашифрованный первый элемент - это следующий элемент в матрице Плейфера
                                    # по горизонтали

                                    new_elem1_x, new_elem1_y = elem1_x + 1, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    # То зашифрованный второй элемент - это следующий элемент в матрице Плейфера
                                    # по горизонтали также

                                    new_elem2_x, new_elem2_y = elem2_x + 1, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                                # Если смещение вправо для второго элемента по горизонтали невозможно, тогда
                                # Элемент выходит за пределы матрицы 5x5 по горизонтали

                                elif elem2_x + 1 > 4:

                                    # Первый элемент все также смещается вправо, поскольку ему ничего не мешает

                                    new_elem1_x, new_elem1_y = elem1_x + 1, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    # А второй элемент перемещается в начало матрицы (влево)

                                    new_elem2_x, new_elem2_y = elem2_x + 1 - 5, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                            # Check 2

                            # Аналогичная ситуация происходит в случае, если первый элемент
                            # выходит за пределы по горизонтали, а второй нет

                            elif elem1_x + 1 > 4:

                                if elem2_x + 1 <= 4:

                                    # Смещение с левой стороны используется для первого элемента

                                    new_elem1_x, new_elem1_y = elem1_x + 1 - 5, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    # Второй элемент смещается вправо

                                    new_elem2_x, new_elem2_y = elem2_x + 1, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                                # Иначе, если оба элемента не могут смещены в право,
                                # то оба элемента смещаются относительно начала, то есть с левой стороны

                                elif elem2_x + 1 > 4:

                                    new_elem1_x, new_elem1_y = elem1_x + 1 - 5, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x + 1 - 5, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:
                                            self.Message_to_decode += btn_data[3]

                                            continue

                        break

                    # Если из пары букв получается вертикальная линия

                    elif elem1_x == elem2_x:

                        if elem1_y != elem2_y:

                            # 'VERTICAL LINE'

                            # Check 1

                            # То смещение происходит сверху вниз,
                            # если выходят за пределы, то элементы появляются сверху матрицы Плейфера

                            # Оба элемента могут быть смещены вниз

                            if elem1_y + 1 <= 4:

                                if elem2_y + 1 <= 4:

                                    new_elem1_x, new_elem1_y = elem1_x, elem1_y + 1

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x, elem2_y + 1

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                elif elem2_y + 1 > 4:

                                    new_elem1_x, new_elem1_y = elem1_x, elem1_y + 1

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x, elem2_y + 1 - 5

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                            # Check 2

                            elif elem1_y + 1 > 4:

                                if elem2_y + 1 <= 4:

                                    new_elem1_x, new_elem1_y = elem1_x, elem1_y + 1 - 5

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x, elem2_y + 1

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                elif elem2_y + 1 > 4:

                                    new_elem1_x, new_elem1_y = elem1_x, elem1_y + 1 - 5

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x, elem2_y + 1 - 5

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                        break

        # Вывод закодированого сообщения в соответствующее поле

        self.encode_text_Text.insert(tk.END, '\n\n' + self.Message_to_decode)
        self.Message_to_decode = ''

    # Функция, запускает декодирование сообщения на шифре Плейфера

    def Playfair_Cipher_decode_execution(self):
        # Первоначальные действия аналогичны функции кодирования текста

        key = self.number_select_entry.get()
        key = ''.join(key.split())
        key = key.upper()
        key = key.replace('J', 'I')
        modified_alphabet = key.upper() + self.alphabet

        control_alphabet = []
        iter = 0

        for letter in modified_alphabet:

            if letter not in control_alphabet:

                control_alphabet.append(letter)

                self.Buttons[iter][0].config(state=tk.NORMAL, text=letter)
                self.Buttons[iter][3] = letter
                self.Buttons[iter][0].config(state=tk.DISABLED)
                iter += 1

        Message_to_encode = self.encode_text_Text.get("1.0", 'end-1c')

        DIAGRAPHS = convertPlainTextToDiagraphs(Message_to_encode)

        elem1, elem2 = None, None

        # Происходит такое же разбиение элементов на первый и второй
        # В данном случае все последующие действия совершенно аналогичны тем, что были применены в кодировании
        # За исключением того, что они отзеркалены
        # Квадрат - выбераются элементы противоположных сторон на одном ряду
        # Горизонтальная линия - смещение влево, если вышли за левый предел, перемещаем вправо
        # Вертикальная линия - смещение вверх, если вышли за верхний предел, перемещаем вниз

        for current_pair in DIAGRAPHS:
            for btn_data in self.Buttons:
                if btn_data[3] == current_pair[0]:
                    elem1 = btn_data

                elif btn_data[3] == current_pair[1]:
                    elem2 = btn_data

                if elem1 is not None and elem2 is not None:

                    elem1_x = elem1[1]
                    elem1_y = elem1[2]

                    elem2_x = elem2[1]
                    elem2_y = elem2[2]

                    elem1, elem2 = None, None

                    if elem1_x != elem2_x:

                        if elem1_y != elem2_y:

                            # 'SQUARE'

                            # Check 1

                            if elem1_x > elem2_x:

                                if elem1_y > elem2_y:

                                    new_elem1_x, new_elem1_y = elem2_x, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem1_x, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                elif elem1_y < elem2_y:

                                    new_elem1_x, new_elem1_y = elem2_x, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem1_x, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue
                            # Check 2

                            elif elem1_x < elem2_x:

                                if elem1_y > elem2_y:

                                    new_elem1_x, new_elem1_y = elem2_x, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem1_x, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                elif elem1_y < elem2_y:

                                    new_elem1_x, new_elem1_y = elem2_x, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem1_x, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                        else:
                            # 'HORIZONTAL LINE'

                            # Check 1

                            if elem1_x - 1 >= 0:

                                if elem2_x - 1 >= 0:

                                    new_elem1_x, new_elem1_y = elem1_x - 1, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x - 1, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                elif elem2_x - 1 < 0:

                                    new_elem1_x, new_elem1_y = elem1_x - 1, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x - 1 + 5, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                            # Check 2

                            elif elem1_x - 1 < 0:

                                if elem2_x - 1 >= 0:

                                    new_elem1_x, new_elem1_y = elem1_x - 1 + 5, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x - 1, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                elif elem2_x - 1 < 0:

                                    new_elem1_x, new_elem1_y = elem1_x - 1 + 5, elem1_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x - 1 + 5, elem2_y

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                        break

                    elif elem1_x == elem2_x:

                        if elem1_y != elem2_y:

                            # 'VERTICAL LINE'

                            # Check 1

                            if elem1_y - 1 >= 0:

                                if elem2_y - 1 >= 0:

                                    new_elem1_x, new_elem1_y = elem1_x, elem1_y - 1

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x, elem2_y - 1

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                elif elem2_y - 1 < 0:

                                    new_elem1_x, new_elem1_y = elem1_x, elem1_y - 1

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x, elem2_y - 1 + 5

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                            # Check 2

                            elif elem1_y - 1 < 0:

                                if elem2_y - 1 >= 0:

                                    new_elem1_x, new_elem1_y = elem1_x, elem1_y - 1 + 5

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x, elem2_y - 1

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                elif elem2_y - 1 < 0:

                                    new_elem1_x, new_elem1_y = elem1_x, elem1_y - 1 + 5

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem1_x and btn_data[2] == new_elem1_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                                    new_elem2_x, new_elem2_y = elem2_x, elem2_y - 1 + 5

                                    for btn_data in self.Buttons:

                                        if btn_data[1] == new_elem2_x and btn_data[2] == new_elem2_y:

                                            self.Message_to_decode += btn_data[3]

                                            continue

                        break

        # Вывод декодированого сообщения в соответствующее поле

        self.encode_text_Text.insert(tk.END, '\n\n' + self.Message_to_decode)

        self.Message_to_decode = ''


# Запуск программы шифра Плейфера


if __name__ == '__main__':
    root = tk.Tk()
    Playfair_Cipher_App = GUI(root, 'ABCDEFGHIKLMNOPQRSTUVWXYZ')
    root.mainloop()
