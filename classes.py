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

class CountMixin:

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        with open(self.data_file, 'r') as d:
            data = json.load(d)
            for i in data:
                return len(i)


class HHVacancy(CountMixin, Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """
    data_file = 'res.json'
    vacancies = []

    def __init__(self, name, link, salary, descrip, company_name):
        super().__init__(name, link, descrip, salary)
        self.company_name = company_name
        self.count = CountMixin.get_count_of_vacancy

    @classmethod
    def add_vacancies_list(cls, data_file):
        with open(f'{data_file}') as f:
            d_file = json.load(f)
            for i in d_file:
                for j in i:
                    a = j.get("name")
                    b = j.get('url')
                    c = j.get('snippet').get('responsibility')
                    try:
                        d = j.get('salary').get('from')
                        if d == None:
                            d = 0
                    except AttributeError:
                        d = 0
                    company_name = j.get('employer').get('name')
                    cls.vacancies.append(HHVacancy(a, b, c, d, company_name))



    def __str__(self):
        return f'HH: ' + super().__str__()


class SJVacancy(CountMixin, Vacancy):  # add counter mixin
    """ SuperJob Vacancy """
    data_file = 'sj_res.json'
    vacancies = []

    def __init__(self, name, link, descrip, salary, company_name):
        super().__init__(name, link, salary, descrip)
        self.company_name = company_name


    def __str__(self):
        return f'SJ: ' + super().__str__()

    @classmethod
    def add_vacancies_list(cls, data_file):
        with open(f'{data_file}') as f:
            d_file = json.load(f)
            for i in d_file:
                for j in i:
                    a = j.get("profession")
                    b = j.get("link")
                    c = j.get('candidat')
                    try:
                        d = j.get("payment_from")
                        if d == None:
                            d = 0
                    except AttributeError:
                        d = 0

                    company_name = j.get("firm_name")
                    cls.vacancies.append(SJVacancy(a, b, c, d, company_name))
