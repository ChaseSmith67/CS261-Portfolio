# Name: Chase Smith
# OSU Email: smitcha6@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap
# Due Date: 12//02/2022
# Description: Implementation of a HashMap using open addressing with
#              quadratic probing to handle collisions

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        table, the existing value will be replaced with the new one. Uses open addressing
        with quadratic probing to handle collisions.
        """

        # Calculate load factor and resize if >= 0.5
        load_factor = self.table_load()
        if load_factor >= 0.5:
            self.resize_table(self._capacity * 2)

        # Assign variables for readability
        array, length = self._buckets, self._capacity

        # Create new HashEntry with supplied key/value
        kv_pair = HashEntry(key, value)

        # Use hash function to determine appropriate index
        hash = self._hash_function(key)
        i = hash % length
        j = 0
        index = (i + (j ** 2)) % length

        matching_key = self.contains_key(key)

        while array[index] is not None:
            # Replace matching key, if one exists
            if matching_key:
                if array[index].key == key:
                    if array[index].is_tombstone:
                        self._size += 1
                    array[index] = kv_pair
                    return
            # Replace tombstone, if one is encountered
            if array[index].is_tombstone:
                array[index] = kv_pair
                return

            # Increment and calculate next index
            j += 1
            index = (i + (j ** 2)) % length

        # Insert new HashEntry at empty index and update size
        array[index] = kv_pair
        self._size += 1

    def table_load(self) -> float:
        """
        Calculates and returns the load factor for the Hashmap.
        """

        load_factor = self._size / self._capacity

        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the HashMap.
        """

        count = 0

        # TODO: Incorporate iter() function, when built
        for x in range(self._capacity):
            if not self._buckets[x]:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the size of the table to the given new_capacity. If the value specified is
        not a prime number, the table will be resized to the next prime number. All existing
        entries in the HashMap will be rehashed and added to the new table.
        """

        # Validate specified capacity
        if new_capacity < 1 or new_capacity < self._size:
            return

        # Ensure new capacity is a prime number, update if not
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        function = self._hash_function

        new_map = HashMap(new_capacity, function)

        # TODO: Incorporate iter() function, when built
        for x in range(self._capacity):
            old_hash_entry = self._buckets[x]
            if old_hash_entry and not old_hash_entry.is_tombstone:
                key = old_hash_entry.key
                value = old_hash_entry.value
                new_map.put(key, value)

        # Set data members all to new hashmap
        self._buckets = new_map._buckets
        self._size = new_map._size
        self._capacity = new_map._capacity

    def get(self, key: str) -> object:
        """
        Searches the HashMap for the given key. If found, returns that key's
        matching value. If not found, returns None.
        """

        val = None

        array, length = self._buckets, self._capacity

        # Use hash function to determine appropriate index
        hash = self._hash_function(key)
        i = hash % length
        j = 0
        index = (i + (j ** 2)) % length

        while array[index] is not None:
            if array[index].key == key and not array[index].is_tombstone:
                val = array[index].value
                return val

            # Increment and calculate next index
            j += 1
            index = (i + (j ** 2)) % length

        # Key not found in table
        return val

    def contains_key(self, key: str) -> bool:
        """
        Searches the HashMap for the given key. Returns True if
        the key is found. False, if not.
        """

        if self._size == 0:
            return False

        array, length = self._buckets, self._capacity

        # Use hash function to determine appropriate index
        hash = self._hash_function(key)
        i = hash % length
        j = 0
        index = (i + (j ** 2)) % length

        while array[index] is not None:
            # Key found and is not tombstone
            if array[index].key == key and not array[index].is_tombstone:
                return True

            # Increment and calculate next index
            j += 1
            index = (i + (j ** 2)) % length

        # Key not found in table
        return False

    def remove(self, key: str) -> None:
        """
        Searches the table for the given key and removes that HashEntry from
        the table, leaving a tombstone in its place. If the key is not found
        in the table, nothing happens.
        """

        # Table is empty
        if self._size == 0:
            return

        array, length = self._buckets, self._capacity

        # Use hash function to determine appropriate index
        hash = self._hash_function(key)
        i = hash % length
        j = 0
        index = (i + (j ** 2)) % length

        while array[index] is not None:
            # Key found and is not tombstone
            if array[index].key == key and not array[index].is_tombstone:
                array[index].is_tombstone = True
                self._size -= 1
                return

            # Increment and calculate next index
            j += 1
            index = (i + (j ** 2)) % length

        # Key not found in table
        return

    def clear(self) -> None:
        """
        Removes all entries from the HashMap, but does not change capacity.
        """

        for x in range(self._capacity):
            self._buckets[x] = None

        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray consisting of tuples of all the key/value pairs contained
        in the HashMap. If the HashMap is empty, will return an empty DynamicArray.
        """

        kv_array = DynamicArray()

        # Table is empty
        if self._size == 0:
            return kv_array

        array, length = self._buckets, self._capacity

        for x in range(length):
            if not array[x] or array[x].is_tombstone:
                continue
            key, value = array[x].key, array[x].value
            kv_pair = key, value
            kv_array.append(kv_pair)

        return kv_array

    def __iter__(self):
        """
        Initializes an iterator to traverse through the HashMap.
        """

        # Used to move through the HashMap's entries.
        self._index = 0

        val = self._buckets[self._index]
        # Skip over None and tombstone values
        while not val or val.is_tombstone:
            self._index += 1
            val = self._buckets[self._index]

        return self

    def __next__(self):
        """
        Returns next value in the HashMap and advances the iterator. Skips over
        None values and tombstones.
        """

        try:
            val = self._buckets[self._index]
            # Skip over None and tombstone values
            while not val or val.is_tombstone:
                self._index += 1
                val = self._buckets[self._index]

        except DynamicArrayException:
            raise StopIteration

        self._index += 1

        return val

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(13, hash_function_1)
    # for i in range(25):
    #     m.put('str' + str(i), i * 100)
    #     print(m)
        # if i % 25 == 24:
        #     print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(1500):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

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

    print("\nCustom - empty_buckets example 3")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(1000, 1501):
        print(i)
        if i == 1317:
            print("wtf?")
        m.put('key' + str(i), i * 100)
        if i % 1 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())
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
    #     if m.table_load() > 0.5:
    #         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
    #               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")
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
    # m = HashMap(11, hash_function_1)
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
    # #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())
    #
    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
    #
    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
