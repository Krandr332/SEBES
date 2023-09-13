

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


def check_user_city(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT city FROM users WHERE user_id = %s;", (user_id,))
        result = cursor.fetchone()
        print("Result from database:", result)
        return result
    except Exception as e:
        print(f"Error checking user city: {e}")
        return False
    finally:
        cursor.close()


# Функция для регистрации пользователя в базе данных
def register_user(conn, user_id, city):
    if not check_user_existence(conn, user_id):
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, city) VALUES (%s, %s);", (user_id, city))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error registering user: {e}")
            return False
        finally:
            cursor.close()
    else:
        print(f"User with user_id {user_id} already exists.")
        return False



# Функция для обновления города пользователя в базе данных
def update_user_city(conn, user_id, city):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET city = %s WHERE user_id = %s;", (city, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating user city: {e}")
        return False
    finally:
        cursor.close()

    conn.close()
