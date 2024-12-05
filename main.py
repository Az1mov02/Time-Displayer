import psycopg2
from config import host, user, password, db_name

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()

    while True:
        try:
            phone_id = int(input("Введите id телефона: "))
            break
        except ValueError:
            print("id должен быть числом")

    brand = input("Введите бренд телефона: ")
    model = input("Введите модель телефона: ")

    while True:
        try:
            price = int(input("Введите цену телефона: "))
            break
        except ValueError:
            print("Цена должна быть числом")

    try:
        insert_query = """INSERT INTO phones (phone_id, brand, model, price) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insert_query, (phone_id, brand, model, price))
        connection.commit()
        print("Данные добавлены!")
    except psycopg2.IntegrityError as e:
        print(f"Ошибка при добавлении данных: {e}")
        connection.rollback()

    with connection.cursor() as cursor:
        query = """SELECT * FROM phones"""
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)

except psycopg2.OperationalError as e:
    print(f"Ошибка при подключении к базе данных: {e}")
    exit()

finally:
    # Проверка, существует ли курсор и соединение перед их закрытием
    if cursor:
        cursor.close()
    if connection:
        connection.close()
