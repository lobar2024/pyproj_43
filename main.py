class Database:
    def query(self, sql):
        print(f"  [DB] So'rov: {sql}")
        return f"Natija: {sql}"

class DatabaseProxy:
    """Kesh + kirish nazorati bilan Proxy."""
    def __init__(self, db, allowed_users):
        self._db      = db
        self._allowed = set(allowed_users)
        self._cache   = {}

    def query(self, sql, user="guest"):
        if user not in self._allowed:
            raise PermissionError(f"'{user}' ruxsati yo'q!")
        if sql in self._cache:
            print(f"  [Kesh] {sql}")
            return self._cache[sql]
        result = self._db.query(sql)
        self._cache[sql] = result
        return result

if __name__ == "__main__":
    db    = Database()
    proxy = DatabaseProxy(db, allowed_users=["admin","ali"])

    print(proxy.query("SELECT * FROM users", user="admin"))
    print(proxy.query("SELECT * FROM users", user="admin"))  # keshdan

    try:
        proxy.query("DROP TABLE users", user="guest")
    except PermissionError as e:
        print(f"  Xato: {e}")
