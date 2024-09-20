# ASGI API

## Эндпойнты

**GET /factorial**
   Вычисляет факториал параметра.

**GET /fibonacci/{n}**
   Вычисляет n-ое число Фибоначчи. n в пути запроса.

**GET /mean**
   Вычисляет среднее значение массива. Массив в теле запроса в формате JSON.

- main.py — основной файл
- requirements.txt — зависимости.
- test_homework_1.py — тест

## Требования
- Установленный uvicorn для запуска ASGI-приложения
- Библиотеки pytest и requests для запуска тестов

## Установка
1. Клонируйте репозиторий:

git clone https://github.com/mr-kushnir/py_backend_itmo.git

2. Перейдите в каталог проекта:

cd homework1


4. **Установите зависимости:**


pip install -r requirements.txt

## Запуск приложения
1. Из каталога homework1 запустите приложение:


uvicorn main:app --reload

 
## Тестирование приложения

1. Установите зависимости:
   
   pip install -r requirements.txt
  

2. Запустите тесты:

   pytest test_homework_1.py

