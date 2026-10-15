# Estats d'una posició de la taula (hash tancat). NO canvieu aquests valors.
LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:
   
    def __init__(self, cap=13):
        self._table = [[None, None, LLIURE] for _ in range(cap)]
        self._n = 0  # nombre de claus desades

    def _hash_function(self, key):
        return key % len(self._table)  # h(x) = x % m

    def put(self, key: int, value: int) -> None:
        first_deleted_slot = None

        for i in range(0, len(self._table)):
            j = self._hash_function(key + i)
            state = self._table[j][2]

            if state == OCUPAT and self._table[j][0] == key:
                self._table[j][1] = value
                return

            if state == ESBORRAT and first_deleted_slot is None:
                first_deleted_slot = j

            if state == LLIURE:
                target = (
                    first_deleted_slot if first_deleted_slot is not None else j
                )
                self._table[target] = [key, value, OCUPAT]
                self._n += 1

                if self._n > len(self._table) // 2:
                    self._resize(2 * len(self._table) - 1)
                return

        if first_deleted_slot is not None:
            self._table[first_deleted_slot] = [key, value, OCUPAT]
            self._n += 1
            if self._n > len(self._table) // 2:
                self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        for i in range(0, len(self._table)):
            j = self._hash_function(key + i)
            if self._table[j][0] == key and self._table[j][2] == OCUPAT:
                return self._table[j][1]
            elif self._table[j][2] == LLIURE:
                return -1
        return -1

    def remove(self, key: int) -> None:
        for i in range(0, len(self._table)):
            j = self._hash_function(key + i)
            if self._table[j][0] == key:
                self._table[j] = [None, None, ESBORRAT]
                self._n -= 1
                return

    def __len__(self):
        return self._n

    def _resize(self, c):
        old = self._table
        self._table = [[None, None, LLIURE] for _ in range(c)]
        self._n = 0
        for taula in old:
            if taula[2] == OCUPAT:
                self.put(taula[0], taula[1])