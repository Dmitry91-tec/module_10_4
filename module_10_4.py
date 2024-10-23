from threading import Thread
import queue
from time import sleep
import random

class Table:

    def __init__(self,number,guest=None):                            #создаем объект стол
        self.number=number                                           #number-номер стола
        self.guest=guest                                             #guest-гость, который сидит за этим столом
        # print('созданы столы')
class Guest(Thread):

    def __init__(self,name):                                         #создаем объект гость - поток
        super().__init__()                                           #создание потоков
        self.name=name                                               #имя гостя
        # print('созданы гости-потоки')

    def run(self):                                                    #ожидание случайным образом от 3 до 10 секунд
        i = random.randrange(3, 10)
        sleep(i)

class Cafe:

    tables_ = []

    def __init__(self, *args):                                        #Cafe(Table(1), Table(2),....
        self.args = args

    def guest_arrival(self,*guests):                                   #прибытие гостей
        self.guests=guests                                             #создаем общий список гостей
        # print('прибыли гости')
        for guest in self.guests:                                      #работаем с каждым гостем поочереди
            for table in tables:                                       #перебираем столы в кафе под каждого гостя
                tables.remove(table)                                   #убираем стол из списка за который сел гость
                if table.guest is None:                                #если за столом нет гостя, то...
                    table.guest = guest                                #сажаем гостя за стол
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    table.guest.start()                                 #запускаем обслуживание гостя
                    Cafe.tables_.append(table)                          #добавлем стол с гостем в новый список
                    table.guest.join()
                    break
                break
            if table.guest != guest:                                     #если стол занят,то
                q.put(guest)                                             #гость встает в очередь
                print(f'{guest.name} в очереди')

    def discuss_guests(self):                                            #обслужить гостей
        # print("обслужить гостей")
        while q.empty() == False or table.guest.name==None:                                        #пока очередь не пустая
            for table in Cafe.tables_:                                   #перебираем столы для поиска освободившегося
                table.guest.join()                                       #ожидаем завершения обслуживания гостя
                if table.guest.is_alive() == False:                      #если гость покушал
                    print(f'{table.guest.name} покушал(а) и ушел(ушла)')
                    table.guest.name=None
                    print(f'Стол номер {table.number} свободен')
                    if q.empty() == False:
                        table.guest = q.get()
                        table.guest.start()
                        print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    table.guest.join()


tables = [Table(number) for number in range(1, 6)]                          #tables - столы
q=queue.Queue()                                                             #создание очереди
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
            'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra']
guests = [Guest(name) for name in guests_names]                              #создание объекта гостей
cafe = Cafe(*tables)                                                         #заполнение кафе столами
cafe.guest_arrival(*guests)                                                  #заполнение столов гостями
cafe.discuss_guests()