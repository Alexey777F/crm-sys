 # CRM-sys
 ![horoscope_bot](https://github.com/Alexey777F/Horoscope_bot/blob/master/6.png)
 * Демо версия crm системы, обращаю Ваше внимание что доступен только урезанный функционал!
 ___
 * Demo version of the CRM system, please note that only reduced functionality is available!
   
## Технологии - Technologies
 * Docker-compose
 * Python:3.9.18-bullseye
 * Postgresql(container) - postgres:14.8-alpine3.18
 * Flask==2.3.2
 * Flask-SQLAlchemy==3.0.4
 * psycopg2==2.9.3
 * WTForms==3.0.1
 * email-validator==2.0.0.post2
 * aiosmtplib==2.0.2
 
## Установка с помощью Docker-compose
 * Установите Docker Desktop под вашу ОС
 * Необходимо скопировать все содержимое репозитория в отдельный каталог.
 * Установите виртульное окружение на вашей ОС, на Mac OS python3 -m venv my_env
 * Активируйте виртульаное окружение на вашей ОС, на Mac OS source my_env/bin/activate
 * Установить все библиотеки из requirements.txt 
 * Важно! Установить именно те версии которые указаны в requirements.txt иначе возможны ошибки при работе бота.
 * Откройте файл docker-compose.yml и заполните необходимыми данными(секретный ключ, хост, порт и настройки базы данных).
 * Запустите сборку образа и создания контейнера с помощью команды: docker-compose up --build
 * Приложение запущено в контейнере app_container 
 ___
 * Install Docker Desktop on your OS
 * It is necessary to copy all important repositories to a separate directory.
 * Install a virtual environment on your OS, on Mac OS python3 -m venv my_env
 * Activate the virtual environment in your OS, in the Mac OS source my_env/bin/activate.
 * Install all libraries from the requirements.txt file.
 * Important! Install exactly the version specified in the require.txt file, otherwise errors may occur when the bot operates.
 * Open the docker-compose.yml file and fill in the necessary data (secret key, host, port and database settings).
 * Start building the image and creating the container using the command: docker-compose up --build
 * The application is running in the app_container container
   
## Как работает - How does it works
  * Примеры работы приложения
  * Application examples
  ![horoscope_bot](https://github.com/Alexey777F/Horoscope_bot/blob/master/1.png)
  ![horoscope_bot](https://github.com/Alexey777F/Horoscope_bot/blob/master/2.png)
  ![horoscope_bot](https://github.com/Alexey777F/Horoscope_bot/blob/master/3.png)
  ![horoscope_bot](https://github.com/Alexey777F/Horoscope_bot/blob/master/4.png)
  ![horoscope_bot](https://github.com/Alexey777F/Horoscope_bot/blob/master/5.png)