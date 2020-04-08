import json
import os

# load json file
with open('vehicles.json') as f:
    data = json.load(f)

# reservation list
reservation_list = []

# clear screen


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def brands_menu():

    # get the unique brands
    brands = set()
    for item in data:
        brands.add(item['brand'])

    print()
    print()
    print("Marka seçenekleri")
    print()
    for i, brand in enumerate(sorted(brands)):
        print(f'{i+1} - {brand}')
    print("0 - <Ana Menu>")
    print()
    print()
    length = len(brands)

    def read_menu_choice():
        choice = input("Seçiminiz  ")
        try:
            choice = int(choice)
            if choice < 0:
                print("Lütfen geçerli bir seçenek giriniz")
                return read_menu_choice()
            elif choice > length:
                print("Lütfen geçerli bir seçenek giriniz")
                return read_menu_choice()
            return choice
        except ValueError:
            print("Lütfen seçeneğinizi rakam olarak giriniz")
            return read_menu_choice()

    option = read_menu_choice()
    if option == 0:
        main_menu()
    elif option <= length:
        models_menu(sorted(brands)[option-1])


def models_menu(brand):

    models = []
    for item in data:
        if item["brand"] == brand:
            models.append(item["type"])

    print()
    print()
    print("Model seçenekleri")
    print()
    for i, model in enumerate(models):
        print(f'{i+1} - {model}')
    print("0 - <Markalar Menusu>")
    print()
    print()
    length = len(models)

    def read_menu_choice():
        choice = input("Seçiminiz  ")
        try:
            choice = int(choice)
            if choice < 0:
                print("Lütfen geçerli bir seçenek giriniz")
                return read_menu_choice()
            elif choice > length:
                print("Lütfen geçerli bir seçenek giriniz")
                return read_menu_choice()
            return choice
        except ValueError:
            print("Lütfen seçeneğinizi rakam olarak giriniz")
            return read_menu_choice()

    option = read_menu_choice()
    if option == 0:
        brands_menu()
    elif option <= length:
        selected_model = models[option-1]

        def read_quantity():
            choice = input("Kaç günlüğüne reservasyon yapmak istiyorsunuz  ")
            try:
                choice = int(choice)
                if choice <= 0:
                    print("Lütfen geçerli bir seçenek giriniz")
                    return read_quantity()

                return choice
            except ValueError:
                print("Lütfen seçeneğinizi rakam olarak giriniz")
                return read_quantity()

        day_count = read_quantity()

        # vehicle inventory check
        if vehicle_inventory_check(brand, selected_model) == False:
            print("** Yeterli araç bulunamadı.")
            print("** Reservasyon yapılamıyor.")
            print("** Lütfen başka bir araç deneyiniz")
            print()
            print()
            main_menu()
            return

        # add new reservation item
        reservation = []
        reservation.append(brand)
        reservation.append(selected_model)
        reservation.append(day_count)

        # calculate pricing
        for item in data:
            if item["brand"] == brand:
                if item["type"] == selected_model:
                    reservation.append(day_count*int(item["daily_price"]))

        # save reservation
        reservation_list.append(reservation)
        print("Reservasyon bilgileriniz kaydedildi")
        print()
        print()
        main_menu()


def reservation_list_menu():

    print()
    print()
    print("Reservasyon Listesi")
    print()
    for reservation in reservation_list:
        print(
            f'{reservation[0]} - {reservation[1]} -> {reservation[2]}  günlüğüne. Toplam tutar: {reservation[3]}TL')
    print()
    print("0 - <Ana Menu>")
    print()
    print()

    def read_menu_choice():
        choice = input("Seçiminiz  ")
        try:
            choice = int(choice)
            if choice != 0:
                print("Lütfen geçerli bir seçenek giriniz")
                return read_menu_choice()

            return choice
        except ValueError:
            print("Lütfen seçeneğinizi rakam olarak giriniz")
            return read_menu_choice()

    option = read_menu_choice()
    if option == 0:
        main_menu()


def main_menu():

    print("**************************************************************************************")
    print("***                                                                                ***")
    print("***\t\t Araç Kiralama Servisine Hoşgeldiniz!                             ****")
    print("***                                                                                ***")
    print("**************************************************************************************")
    print()
    print()
    print("1 - Yeni Reservasyon")
    print("2 - Reservasyon Listesi")
    print("3 - Çıkış")
    print()
    print()

    def read_menu_choice():
        choice = input("Seçiminiz (1,2,veya 3) ")
        try:
            choice = int(choice)
            if choice < 1:
                print("Lütfen geçerli bir seçenek giriniz")
                return read_menu_choice()
            elif choice > 3:
                print("Lütfen geçerli bir seçenek giriniz")
                return read_menu_choice()
            return choice
        except ValueError:
            print("Lütfen seçeneğinizi rakam olarak giriniz")
            return read_menu_choice()

    option = read_menu_choice()
    if option == 1:
        brands_menu()
    elif option == 2:
        reservation_list_menu()
    elif option == 3:
        print("Çıkış işlemi yapılıyor....")
        exit()


def vehicle_inventory_check(brand, model):
    inventory_count = 0
    for item in data:
        if item["brand"] == brand:
            if item["type"] == model:
                inventory_count = item["amount"]

    # reserved quantity
    reserved_count = 1
    for item in reservation_list:
        if item[0] == brand:
            if item[1] == model:
                reserved_count += 1

    if inventory_count-reserved_count >= 0:
        return True
    else:
        return False


cls()
main_menu()
