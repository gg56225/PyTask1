from csv import DictWriter, DictReader
from os.path import exists


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_data():
    flag = False
    while not flag:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Слишком короткое имя")
            last_name = input("Введите имя: ")
            if len(last_name) < 5:
                raise NameError("Слишком короткая фамилия")
        except NameError as err:
            print(err)
        else:
            flag = True
    phone = "+73287282037"
    return [first_name, last_name, phone]


def create_file(filename):
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as data:
        f_r = DictReader(data)
        return list(f_r)


def write_file(filename, lst):
    res = read_file(filename)
    obj = {'Имя': lst[0], 'Фамилия': lst[1], 'Телефон': lst[2]}
    res.append(obj)
    standard_write(filename, res)


def row_search(filename):
    last_name = input("Введите фамилию: ")
    res = read_file(filename)
    for row in res:
        if last_name == row['Фамилия']:
            return row
    return "Запись не найдена"


def delete_row(filename):
    row_number = int(input("Введите номер строки: "))
    res = read_file(filename)
    res.pop(row_number - 1)
    standard_write(filename, res)


def standard_write(filename, res):
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()
        f_w.writerows(res)


def change_row(filename):
    row_number = int(input("Введите номер строки: "))
    res = read_file(filename)
    data = get_data()
    res[row_number-1]["Имя"] = data[0]
    res[row_number-1]["Фамилия"] = data[1]
    res[row_number-1]["Телефон"] = data[2]
    standard_write(filename, res)


def copy_row(source_file, destination_file, row_number):
    """
    Копирует строку с заданным номером из одного файла в другой.

    Args:
        source_file (str): Путь к исходному файлу.
        destination_file (str): Путь к файлу назначения.
        row_number (int): Номер строки, которую необходимо скопировать.
    """
    if not exists(source_file):
        raise FileNotFoundError(f"Файл '{source_file}' не найден.")
    if not exists(destination_file):
        create_file(destination_file)

    source_data = read_file(source_file)
    try:
        row_to_copy = source_data[row_number - 1]
    except IndexError:
        raise ValueError(f"В исходном файле нет строки с номером {row_number}.")

    destination_data = read_file(destination_file)
    destination_data.append(row_to_copy)
    standard_write(destination_file, destination_data)


filename = 'phone.csv'


def main():
    while True:
        command = input("Введите команду: ")
        if command == "q":
            break
        elif command == "w":
            if not exists(filename):
                create_file(filename)
            write_file(filename, get_data())
        elif command == "r":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            print(read_file(filename))
        elif command == "f":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            print(row_search(filename))
        elif command == "d":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            delete_row(filename)
        elif command == "c":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            change_row(filename)
        elif command == "cp":  # Команда для копирования строки
            try:
                source_file = input("Введите путь к исходному файлу: ")
                destination_file = input("Введите путь к файлу назначения: ")
                row_number = int(input("Введите номер строки: "))
                copy_row(source_file, destination_file, row_number)
            except (FileNotFoundError, ValueError) as err:
                print(err)
        else:
            print("Неизвестная команда.")

    if __name__ == "__main__":
        main()