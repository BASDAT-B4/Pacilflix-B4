
class AuthenticationManager:
    @staticmethod
    def check_username(username):
        return """
        SELECT * FROM pacilflix.PENGGUNA WHERE username = %s
        """

    @staticmethod
    def insert_user():
        return """
        INSERT INTO pacilflix.PENGGUNA (username, password, negara_asal) VALUES (%s, %s, %s)
        """
    
    @staticmethod
    def check_user():
        return """
        SELECT * FROM pacilflix.PENGGUNA WHERE username = %s AND password = %s
        """
