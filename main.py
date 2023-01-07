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
