# bridge.py
from user_login import login_user, register_user
from user_info import add_user_food, check_user_food_status, add_to_favorites, list_favorites

def user_session(user_id):
    while True:
        print("\n--- User Food Menu ---")
        print("1. Add Food")
        print("2. Check Food Status")
        print("3. Add to Favorites")
        print("4. List Favorites")
        print("5. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            food_name = input("Food name: ").strip()
            nutrition = input("Nutrition info (optional): ").strip()
            add_user_food(user_id, food_name, nutrition=nutrition)
        elif choice == "2":
            foods = check_user_food_status(user_id)
            print("\n--- User Food Status ---")
            for name, status, nutrition in foods:
                print(f"{name}: {status}, nutrition: {nutrition}")
        elif choice == "3":
            item_name = input("Item to add to favorites: ").strip()
            add_to_favorites(user_id, item_name)
        elif choice == "4":
            list_favorites(user_id)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option.")

# login
def main():
    """
    register/login/ menu
    """
    while True:
        print("\n--- Main Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            register_user(username, email, password)

        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user_id = login_user(username, password)  
            if user_id:
                # successfully logged in
                user_session(user_id)
            else:
                print("Login failed. Try again.")

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
