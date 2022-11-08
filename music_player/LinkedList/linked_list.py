class LinkedListItem:
    """Узел связного списка"""

    def __init__(self, data=None):
        self.__next_item = self.__previous_item = None
        self.data = data

    @property
    def next_item(self):
        """Следующий элемент"""
        return self.__next_item

    @next_item.setter
    def next_item(self, value):
        self.__next_item = value
        value.__previous_item = self

    @property
    def previous_item(self):
        """Предыдущий элемент"""
        return self.__previous_item

    @previous_item.setter
    def previous_item(self, value):
        self.__previous_item = value
        value.__next_item = self

    def __repr__(self):
        return f"data: {self.data}"


class LinkedList:
    """Связный список"""

    def __init__(self, first_item=None):
        self.__head = self.__tail = first_item

        if self.__tail:
            self.length = 1
            while self.__tail.next_item != self.__head and self.__tail.next_item:
                self.__tail = self.__tail.next_item
                self.length += 1

            self.__tail.next_item = self.__head
            self.__head.previous_item = self.__tail
        else:
            self.length = 0

    @property
    def last(self):
        """Последний элемент"""
        return self.__tail

    @property
    def first_item(self):
        """Первый элемент"""
        return self.__head

    def append_for_empty(self, item):
        new_item = LinkedListItem(item)
        self.__head = self.__tail = new_item
        self.__head.next_item = self.__tail.next_item = self.__head
        self.length = 1

    def append_left(self, item):
        """Добавление слева"""
        if self.__head is None:
            self.append_for_empty(item)
            return

        item = LinkedListItem(item)
        self.__head.previous_item = item
        self.__head = self.__head.previous_item
        self.__head.previous_item = self.__tail

        self.length += 1

    def append_right(self, item):
        """Добавление справа"""
        if self.__head is None:
            self.append_for_empty(item)
            return

        item = LinkedListItem(item)
        self.__tail.next_item = item
        self.__tail = self.__tail.next_item
        self.__tail.next_item = self.__head

        self.length += 1

    def append(self, item):
        """Добавление справа"""
        self.append_right(item)

    def remove(self, item):
        """Удаление"""
        cursor = self.__head
        for _ in range(self.length):
            if cursor.data == item:
                cursor.previous_item.next_item = cursor.next_item
                cursor.next_item.previous_item = cursor.previous_item
                self.length -= 1
                return
            cursor = cursor.next_item

        raise ValueError("no such elements in list")

    def insert(self, previous, item):
        """Вставка справа"""
        for node in self:
            if previous in (node, node.data):
                if node == self.__tail:
                    self.append(item)
                    return

                item = LinkedListItem(item)
                node.next_item.previous_item = item
                node.next_item = item
                self.length += 1
                return

    def swap(self, first_index, second_index):
        first_item = self[first_index]
        second_item = self[second_index]

        if first_item == self.__head:
            self.__head = second_item
        elif second_item == self.__head:
            self.__head = first_item
        if first_item == self.__tail:
            self.__tail = second_item
        elif second_item == self.__tail:
            self.__tail = first_item

        temp = first_item.next_item
        first_item.next_item = second_item.next_item
        second_item.next_item = temp

        if first_item.next_item is not None:
            first_item.next_item.previous_item = first_item
        if second_item.next_item is not None:
            second_item.next_item.previous_item = second_item

        temp = first_item.previous_item
        first_item.previous_item = second_item.previous_item
        second_item.previous_item = temp

        if first_item.previous_item is not None:
            first_item.previous_item.next_item = first_item
        if second_item.previous_item is not None:
            second_item.previous_item.next_item = second_item

    def pop(self, index):
        cursor = self.first_item
        for _ in range(index):
            cursor = cursor.next_item

        cursor.next_item.previous_item = cursor.previous_item
        cursor.previous_item.next_item = cursor.next_item

        if cursor == self.first_item:
            self.__head = cursor.next_item

        self.length -= 1

    def __len__(self):
        return self.length

    def __iter__(self):
        cursor = self.first_item
        for _ in range(self.length):
            yield cursor
            cursor = cursor.next_item

    def __getitem__(self, index):
        if index >= self.length:
            raise IndexError("index bound of range")

        if index < 0:
            index = self.length - abs(index)
            if index < 0:
                raise IndexError("index bound of range")

        cursor = self.first_item
        for _ in range(index):
            cursor = cursor.next_item

        return cursor

    def __contains__(self, item):
        if not self.__head:
            return False
        for node in self:
            if item in (node, node.data):
                return True

        return False

    def __reversed__(self):
        cursor = self.__tail
        for _ in range(self.length):
            yield cursor
            cursor = cursor.previous_item

    def __repr__(self):
        return ', '.join([i.data.artist for i in self])
