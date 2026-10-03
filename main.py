from datetime import datetime


class Product:
    next_id = 1

    def __init__(self, name, price, quantity):
        if not name.strip():
            raise ValueError("Тауар атауы бос болмауы керек!")
        if price < 0:
            raise ValueError("Баға теріс мән болмауы керек!")
        if quantity < 0:
            raise ValueError("Тауар саны теріс мән болмауы керек!")

        self.id = Product.next_id
        Product.next_id += 1

        self.name = name
        self.__price = price
        self.__quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Баға теріс мән болмауы керек!")
        self.__price = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Тауар саны теріс мән болмауы керек!")
        self.__quantity = value

    def total_cost(self):
        return self.price * self.quantity

    def sell(self, amount):
        if amount <= 0:
            raise ValueError("Сатылатын тауар саны 0-ден үлкен болуы керек!")
        if amount > self.quantity:
            raise ValueError("Қоймада тауар саны жеткіліксіз!")
        self.quantity -= amount

    def info(self):
        return (
            f"ID: {self.id} | Тауар атауы: {self.name} | "
            f"Тауар бағасы: {self.price:.2f} ₸ | Тауар саны: {self.quantity} | "
            f"Жалпы: {self.total_cost():.2f} ₸"
        )


class FoodProduct(Product):
    def __init__(self, name, price, quantity, expiration_date):
        super().__init__(name, price, quantity)
        try:
            self.expiration_date = datetime.strptime(
                expiration_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            raise ValueError(
                "Жарамдылық мерзімі YYYY-MM-DD форматында болуы керек!"
            )

    def info(self):
        return (
            super().info()
            + " | Санаты: Азық-түлік"
            + f" | Жарамдылық мерзімі: {self.expiration_date}"
        )


class ElectronicsProduct(Product):
    def __init__(self, name, price, quantity, warranty):
        super().__init__(name, price, quantity)
        if warranty < 0:
            raise ValueError("Кепілдік мерзімі теріс болмайды!")
        self.warranty = warranty

    def info(self):
        return (
            super().info()
            + " | Санаты: Электроника"
            + f" | Кепілдік: {self.warranty} ай"
        )


class ClothingProduct(Product):
    def __init__(self, name, price, quantity, size):
        super().__init__(name, price, quantity)
        if not size.strip():
            raise ValueError("Киім өлшемі бос болмауы керек!")
        self.size = size.upper()

    def info(self):
        return (
            super().info()
            + " | Санаты: Киім"
            + f" | Өлшемі: {self.size}"
        )


class Store:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        print("✅ Тауар сәтті қосылды!")

    def show_products(self):
        if not self.products:
            print("Қоймада тауар жоқ.")
            return

        print("\n========== ТАУАРЛАР ==========")
        for product in self.products:
            print(product.info())

    def find_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def search(self, keyword):
        return [
            product for product in self.products
            if keyword.lower() in product.name.lower()
        ]

    def delete_product(self, product_id):
        product = self.find_by_id(product_id)
        if product is None:
            print("❌ Мұндай ID нөмірі бар тауар табылмады.")
            return

        self.products.remove(product)
        print("✅ Тауар сәтті өшірілді!")

    def update_product(self, product_id, new_price, new_quantity):
        product = self.find_by_id(product_id)
        if product is None:
            print("❌ Мұндай ID нөмірі бар тауар табылмады.")
            return

        product.price = new_price
        product.quantity = new_quantity
        print("✅ Тауар мәліметтері сәтті өзгертілді!")

    def sell_product(self, product_id, amount):
        product = self.find_by_id(product_id)
        if product is None:
            print("❌ Мұндай ID нөмірі бар тауар табылмады.")
            return

        product.sell(amount)
        print(f"✅ {product.name} тауарының {amount} данасы сатылды!")

    def statistics(self):
        if not self.products:
            print("Қоймада тауар жоқ.")
            return

        total_products = len(self.products)
        total_quantity = sum(p.quantity for p in self.products)
        total_price = sum(p.total_cost() for p in self.products)
        most_expensive = max(self.products, key=lambda p: p.price)

        print("\n========== СТАТИСТИКА ==========")
        print(f"Тауар атауларының саны: {total_products}")
        print(f"Қоймадағы жалпы тауар саны: {total_quantity}")
        print(f"Қоймадағы тауарлардың жалпы құны: {total_price:.2f} ₸")
        print(
            f"Ең қымбат тауар: {most_expensive.name} "
            f"({most_expensive.price:.2f} ₸)"
        )


def main():
    store = Store()

    while True:
        try:
            print("\n========== ТАУАР БАСҚАРУ ЖҮЙЕСІ ==========")
            print("1 - Жаңа тауар қосу")
            print("2 - Барлық тауарларды көру")
            print("3 - Тауарды іздеу")
            print("4 - Тауар мәліметтерін өзгерту")
            print("5 - Тауарды өшіру")
            print("6 - Тауарды сату")
            print("7 - Статистиканы көру")
            print("0 - Бағдарламадан шығу")

            choice = input("\nТаңдауыңыз: ")

            if choice == "1":
                print("\nТауар санатын таңдаңыз:")
                print("1 - Азық-түлік")
                print("2 - Электроника")
                print("3 - Киім")

                product_type = input("Таңдауыңыз: ")
                name = input("Тауар атауы: ")
                price = float(input("Тауар бағасы: "))
                quantity = int(input("Тауар саны: "))

                if product_type == "1":
                    expiration = input(
                        "Жарамдылық мерзімі (YYYY-MM-DD): "
                    )
                    store.add_product(
                        FoodProduct(name, price, quantity, expiration)
                    )

                elif product_type == "2":
                    warranty = int(input("Кепілдік мерзімі (ай): "))
                    store.add_product(
                        ElectronicsProduct(name, price, quantity, warranty)
                    )

                elif product_type == "3":
                    size = input("Өлшемі (S/M/L/XL): ")
                    store.add_product(
                        ClothingProduct(name, price, quantity, size)
                    )

                else:
                    print("❌ Тауар түрі дұрыс таңдалмады.")

            elif choice == "2":
                store.show_products()

            elif choice == "3":
                keyword = input("Іздеу үшін атауды енгізіңіз: ")
                results = store.search(keyword)

                if not results:
                    print("❌ Тауар табылмады.")
                else:
                    print("\n--- ІЗДЕУ НӘТИЖЕЛЕРІ ---")
                    for product in results:
                        print(product.info())

            elif choice == "4":
                product_id = int(input("Өзгертілетін тауардың ID нөмірі: "))
                new_price = float(input("Жаңа бағасы: "))
                new_quantity = int(input("Жаңа саны: "))
                store.update_product(
                    product_id, new_price, new_quantity
                )

            elif choice == "5":
                product_id = int(input("Өшірілетін тауардың ID нөмірі: "))
                store.delete_product(product_id)

            elif choice == "6":
                product_id = int(input("Сатылатын тауардың ID нөмірі: "))
                amount = int(input("Сатылатын тауар саны: "))
                store.sell_product(product_id, amount)

            elif choice == "7":
                store.statistics()

            elif choice == "0":
                print("\nБағдарлама жұмысы аяқталды.")
                break

            else:
                print("❌ Мұндай мәзір таңдауы жоқ!")

        except ValueError as error:
            print("❌ Қате:", error)

        except KeyboardInterrupt:
            print("\nБағдарлама пайдаланушы тарапынан тоқтатылды.")
            break

        except EOFError:
            print("\nДерек енгізу аяқталды.")
            break


if __name__ == "__main__":
    main()
