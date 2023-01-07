import json

class Vacancy:
    __slots__ = ('name', 'link', 'descrip', 'salary')

    def __init__(self, name, link, salary, descrip):
        self.name = name
        self.link = link
        self.descrip = descrip
        self.salary = salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary

    def __str__(self):
        if self.salary:
            return f'{self.name}, ссылка на вакансию: {self.link}.\nОписание: {self.descrip}\nЗарплата: {self.salary} руб'
        else:
            return f'{self.name}, ссылка на вакансию: {self.link}.\nОписание: {self.descrip}\nЗарплата не указана'

    def __iter__(self):
        self.value = 0
        return self.value

    def __next__(self):
        if self.value < len(self.vacancies):
            self.value += 1
        else:
            raise StopIteration