import psycopg2

# Функция для проверки наличия пользователя в базе данных
def check_user_existence(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM public.users WHERE user_id = %s;", (user_id,))
        result = cursor.fetchone()
        return result[0] > 0
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False
    finally:
        cursor.close()

# Функция для регистрации пользователя в базе данных
def register_user(conn, user_id,city):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, city) VALUES (%s, %s);", (user_id,city))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False
    finally:
        cursor.close()

# Пример использования




    conn.close()
