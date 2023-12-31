 # CRM-sys
 ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm2.png)
 * Демо версия crm системы, обращаю Ваше внимание что доступен только урезанный функционал!
 * Полная версия приложения позволяет отправлять отчёт на почту сотрудника.
 * В полной версии есть функции добавления клиентов и расширенный отчёт по месяцам и за всё время.
 ___
 * Demo version of the CRM system, please note that only reduced functionality is available!
 * The full version of the application allows you to send a report to an employee’s email.
 * The full version has functions for adding clients and an extended report by month and for all time.
   
## Технологии - Technologies
 * Docker-compose
 * Python(image): 3.9.18-bullseye
 * Postgresql(image): postgres:14.8-alpine3.18
 * Nginx(image)
 * Flask(v. 2.3.2)
 * Flask-SQLAlchemy(v. 3.0.4)
 * psycopg2(v. 2.9.3)
 * WTForms(v. 3.0.1)
 * email-validator(v. 2.0.0.post2)
 * aiosmtplib(v. 2.0.2)
 
## Установка с помощью Docker-compose - Install with Docker-compose
 * Установите Docker Desktop под вашу ОС
 * Необходимо скопировать все содержимое репозитория в отдельный каталог.
 * Установите виртуальное окружение на вашей ОС, на Mac OS python3 -m venv my_env
 * Активируйте виртуальное окружение на вашей ОС, на Mac OS source my_env/bin/activate
 * Откройте файл docker-compose.yml и заполните необходимыми данными(секретный ключ, хост, порт и настройки базы данных).
 * Запустите сборку образа и создания контейнера с помощью команды: docker-compose up --build
 * Приложение запущено в контейнере app_container 
 ___
 * Install Docker Desktop on your OS
 * It is necessary to copy all important repositories to a separate directory.
 * Install a virtual environment on your OS, on Mac OS python3 -m venv my_env
 * Activate the virtual environment in your OS, in the Mac OS source my_env/bin/activate.
 * Open the docker-compose.yml file and fill in the necessary data (secret key, host, port and database settings).
 * Start building the image and creating the container using the command: docker-compose up --build
 * The application is running in the app_container container
   
## Как работает - How does it works
  * Примеры работы приложения
  * Application examples
  ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm1.png)
  ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm2.png)
  ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm3.png)
  ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm4.png)
  ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm5.png)
  ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm6.png)
  ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm7.png)
  ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm8.png)

## Контейнеры в Docker Desktop - Containers in Docker Desktop
  ![CRM-sys](https://github.com/Alexey777F/crm-sys/blob/main/crm9.png)

