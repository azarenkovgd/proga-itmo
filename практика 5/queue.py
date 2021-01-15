class Node:
    def __init__(self, data, next_node=None):
        self.contained_object = data
        self.next = next_node

    def get_contained_object(self):
        return self.contained_object


class MyQueue:
    def __init__(self, head=None):
        self.head = head

    def add(self, obj):
        new_node = Node(obj)
        new_node.next = self.head
        self.head = new_node

    def remove(self, data):
        current_node = self.head
        prev_node = None

        while current_node is not None:
            if current_node.contained_object == data:
                if prev_node is not None:
                    prev_node.next = current_node.next
                else:
                    self.head = current_node.next
                return

            else:
                prev_node = current_node
                current_node = current_node.next

        return

    def __str__(self):
        if self.head is None:
            return "Очередь пуста"

        result = []
        current = self.head

        while True:
            obj_str = str(current.get_contained_object())
            result.append(obj_str)

            if current.next is None:
                break

            current = current.next

        result_str = ', '.join(result)
        return result_str

    def clear(self):
        self.head = None

    def to_list(self):
        result = []

        if self.head is None:
            return result

        current = self.head

        while True:
            obj = current.get_contained_object()
            result.append(obj)

            if current.next is None:
                break

            current = current.next

        return result


class Country:
    def __init__(self, name, capital, population):
        self.name = name
        self.capital = capital
        self.population = population

    def __str__(self):
        description = f'(Страна: {self.name}, Столица: {self.capital}, Население: {self.population})'
        return description


def main():
    nums_queue = MyQueue()

    nums_queue.add(1)
    nums_queue.add(3)
    nums_queue.add(2)
    nums_queue.add(10000)

    print("Числа:")
    print(nums_queue)

    russia = Country("Россия", "Москва", 150000000)
    usa = Country("США", "Вашингтон", 300000000)

    countries = MyQueue()
    countries.add(russia)
    countries.add(usa)

    print("Страны:")
    print(countries)


if __name__ == "__main__":
    main()
