import json
import os

dir = os.getcwd()

class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, df):
        self.__data_file = os.path.join(dir, df)
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        try:
            fp = open(self.__data_file, 'r', encoding='utf-8')
        except FileNotFoundError:
            fp = open(self.__data_file, 'w', encoding='utf-8')
            data = []
            json.dump(data, fp)
        else:
            data = json.load(fp)
            print(data)
        finally:
            fp.close()

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        fp = open(self.__data_file, 'r', encoding='utf-8')
        new_data = json.load(fp)
        new_data.append(data)
        fp.close()

        fp = open(self.__data_file, 'w', encoding='utf-8')
        json.dump(new_data, fp)
        fp.close()

    def select(self, query):

        fp = open(self.__data_file, 'r', encoding='utf-8')
        data = json.load(fp)
        fp.close()

        if not len(query):  return data

        query_data = []
        for k in data[query.keys()]:
            if data[k] == query.values():
                query_data.append(data[k])

        return query_data

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запросу,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not len(query): return

        fp = open(self.__data_file, 'r', encoding='utf-8')
        data = json.load(fp)
        fp.close()

        count = 0
        for k in data:
            if k.get(list(query.keys())[0]) == list(query.values())[0]:
                del data[count]
            count += 1

        fp = open(self.__data_file, 'w', encoding='utf-8')
        json.dump(data, fp)
        fp.close()

        return

if __name__ == '__main__':
    df = Connector('df.json')

    data_for_file = {'id': 1, 'title': 'tet'}

    df.insert(data_for_file)
    data_from_file = df.select(dict())
    assert data_from_file == [data_for_file]

    df.delete({'id':1})
    data_from_file = df.select(dict())
    assert data_from_file == []