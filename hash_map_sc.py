# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds the given key/value pair to the HashMap. If the key already exists in the
        table, the existing value will be replaced with the new one.
        """

        load_factor = self.table_load()

        if load_factor >= 1.0:
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)
        index = hash % self._capacity

        bucket = self._buckets[index]
        matching_key = bucket.contains(key)

        if matching_key:
            matching_key.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the HashMap
        """

        empty_buckets = 0

        for x in range(self._capacity):
            if self._buckets[x].length() == 0:
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        """
        Calculates and returns the load factor for the Hashmap.
        """

        load_factor = self._size / self._capacity

        return load_factor

    def clear(self) -> None:
        """
        Removes all contents of the HashMap and resets the size variable to 0.
        """

        for x in range(self._capacity):
            self._buckets[x] = LinkedList()

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the size of the table to the given new_capacity. If the value specified is
        not a prime number, the table will be resized to the next prime number.
        """

        if new_capacity < 1:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        function = self._hash_function

        new_map = HashMap(new_capacity, function)

        for x in range(self._capacity):
            # if self._buckets[x].length() > 0:
            #     iterator = self._buckets[x].__iter__()
            #     for y in range(self._buckets[x].length()):
            #         node = iterator.__next__()
            #         new_map.put(node.key, node.value)
            bucket = self._buckets[x]
            for node in bucket:
                new_map.put(node.key, node.value)

        self._buckets = new_map._buckets
        self._size = new_map._size
        self._capacity = new_map._capacity

    def get(self, key: str):
        """
        Searches the map for the given key and returns the corresponding value.
        If the key is not in the table, returns None.
        """

        val = None

        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]

        # if bucket.length() > 0:
        #     iterator = bucket.__iter__()
        #     while iterator is not None:
        #         node = iterator.__next__()
        #         if node.key == key:
        #             val = node.value
        #             return val

        for node in bucket:
            if node.key == key:
                val = node.value
                return val

        return val

    def contains_key(self, key: str) -> bool:
        """
        Searches the HashMap for the given key. If the key is found, returns
        True. If not, returns False.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]

        if self._capacity == 0 or self._size == 0:
            return False

        # if bucket.length == 0:
        #     return False
        # elif bucket.length() > 0:
        #     iterator = bucket.__iter__()
        #     node = iterator.__next__()
        #     while node:
        #         if node.key == key:
        #             return True
        #         try:
        #             node = iterator.__next__()
        #         except StopIteration:
        #             return False

        for node in bucket:
            if node.key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the HashMap. Has no effect
        if the key is not found.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]

        if self._capacity == 0 or self._size == 0:
            return

        if bucket.length == 0:
            return
        elif bucket.length() > 0:
            iterator = bucket.__iter__()
            node = iterator.__next__()
            while node:
                if node.key == key:
                    bucket.remove(key)
                    self._size -= 1
                    return
                try:
                    node = iterator.__next__()
                except StopIteration:
                    return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Creates and returns a DynamicArray consisting of tuples of each key/value
        pair. If the HashMap is empty, an empty DynamicArray will be returned.
        """

        kv_array = DynamicArray()

        for x in range(self._capacity):
            if self._buckets[x].length() > 0:
                iterator = self._buckets[x].__iter__()
                for y in range(self._buckets[x].length()):
                    node = iterator.__next__()
                    kv_pair = node.key, node.value
                    kv_array.append(kv_pair)

        return kv_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes a DynamicArray and returns a tuple consisting of the mode of the given
    DynamicArray (as a new DynamicArray) and the frequency of the mode.
    """

    length = da.length()

    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    for x in range(length):
        if not map.contains_key(da[x]):
            map.put(da[x], 1)
        else:
            current_count = map.get(da[x])
            map.put(da[x], current_count + 1)

    map_da = map.get_keys_and_values()
    result_da = DynamicArray()
    highest = 0

    for y in range(map_da.length()):
        if map_da[y][1] > highest:
            highest = map_da[y][1]

    for z in range(map_da.length()):
        if map_da[z][1] == highest:
            result_da.append(map_da[z][0])

    result = (result_da, highest)

    return result

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    pass
    #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # cases = [("apple", "red"), ("banana", "yellow"), ("orange", "orange"), ("blueberry", "blue"),
    #          ("raspberry", "red"), ("grape", "purple")]

    # cases = [[i for i in range(1, 101)], [x for x in range(5, 306, 5)]]
    #
    # print("\nCustom example 1")
    # print("-------------------")
    # m = HashMap(5, hash_function_1)
    # for case in cases:
    #     m.put(case[0], case[1])
    #     print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print(m)

    # print("\nCustom - put example 2")
    # print("-------------------")
    # m = HashMap(3, hash_function_1)
    # words = ['wer', 'sdfeww', 'ghtee', 'wwefwg', 'awefdgh', 'erteb', 'qpqpwkr', 'wef', 'ngfbvds', 'ergerg']
    # for i in range(15):
    #     for word in words:
    #         m.put(word + str(i), i * 13)
    #         # if i % 25 == 24:
    #         #     print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #         if i % 5 == 0:
    #             print(m)
    # m = HashMap(53, hash_function_1)
    # m.put("apple", "red")
    # m.put("banana", "yellow")
    # print(m.empty_buckets())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    # for i in range(50):
    #     m.put('str' + str(i // 5), i * 200)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
