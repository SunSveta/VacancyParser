import requests
from abc import ABC, abstractmethod
import json
from connector import Connector
from classes import HHVacancy, SJVacancy
from classes import get_top, sorting

class Engine(ABC):
    @abstractmethod
    def get_request(self):
        raise NotImplementedError("Необходимо определить метод get_request")

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        connector = Connector(f'{file_name}')
        return connector

class HH(Engine):
    __url = 'https://api.hh.ru/'
    __per_page = 20

    def get_vacancies(self, search_word, page):
        response = requests.get(f'{self.__url}vacancies?text={search_word}&page={page}')
        #print(response.status_code)
        if response.status_code == 200:
            return response.json()
        return None

    def get_request(self, search_word, vacancies_count):
        page = 0
        result = []
        while self.__per_page * page < vacancies_count:
            tmp_result = self.get_vacancies(search_word, page)
            if tmp_result:
                result += tmp_result.get('items')
                page += 1
            else:
                break
        return result

class Superjob(Engine):
    __url = 'https://api.superjob.ru/2.0'
    __secret = 'v3.r.137227839.a9b3149e3d9c178985e98b7e5a4b73aed59ced95.227f35e168274cb8b8039180e051bc6dadb7b361'
    __per_page = 20

    def _send_request(self,search_word, page):
        url = f'{self.__url}/vacancies/?page={page}&keyword={search_word}'
        headers = {
            'X-Api-App-Id': self.__secret,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.get(
            url=url,
            headers=headers
        )
        if response.status_code == 200:
            return response.json()

        return None

    def get_request(self, search_word,vacancies_count):
        page = 0
        result = []
        while self.__per_page * page < vacancies_count:
            tmp_result = self._send_request(search_word, page)
            if tmp_result:
                result += tmp_result.get('objects')
                page += 1
            else:
                break
        return result

if __name__ =='__main__':
    website = int(
        input('Выберете сайт, на котором будет производиться поиск: \n1 - https://hh.ru\n2 - https://superjob.ru\n'))
    search_word = input('Введите ключевое слово для поиска: ')
    top_count = int(input('Сколько вакансий нужно вывести?  '))
    is_sorting = int(input('Сортировать вакансии по уменьшению зарплаты? Да - 1, нет - 0: '))

    while True:
        vacancies_count = 100
        if website == 1:
            hh_engine = HH()
            resHH = hh_engine.get_request(search_word, vacancies_count)
            a = HH.get_connector('res.json')
            a.insert(resHH)
            HHVacancy.add_vacancies_list('res.json')
            if is_sorting:
                sort_list = sorting(HHVacancy.vacancies)
                get_top(sort_list, top_count)
                print(HHVacancy.get_count_of_vacancy)
            else:
                get_top(HHVacancy.vacancies, top_count)
                print(HHVacancy.get_count_of_vacancy)

        if website == 2:
            sj_engine = Superjob()
            resSJ = sj_engine.get_request(search_word, vacancies_count)
            b = Superjob.get_connector('sj_res.json')
            b.insert(resSJ)
            SJVacancy.add_vacancies_list('sj_res.json')
            if is_sorting:
                sort_list = sorting(SJVacancy.vacancies)
                get_top(sort_list, top_count)
                print(SJVacancy.get_count_of_vacancy)
            else:
                get_top(SJVacancy.vacancies, top_count)
                print(SJVacancy.get_count_of_vacancy)
        break
