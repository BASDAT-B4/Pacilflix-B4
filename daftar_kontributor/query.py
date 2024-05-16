class ContributorManager:
    def filter_by_sutradara():
        return """
        SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan, 'Sutradara' AS tipe
        FROM pacilflix.CONTRIBUTORS AS c
        JOIN pacilflix.SUTRADARA AS s ON c.id = s.id
        """

    def filter_by_pemain():
        return """
        SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan, 'Pemain' AS tipe
        FROM pacilflix.CONTRIBUTORS AS c
        JOIN pacilflix.PEMAIN AS p ON c.id = p.id
        """

    def filter_by_penulis_skenario():
        return """
        SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan, 'Penulis Skenario' AS tipe
        FROM pacilflix.CONTRIBUTORS AS c
        JOIN pacilflix.PENULIS_SKENARIO AS ps ON c.id = ps.id
        """

    def get_all_contributors():
        return f"""
        SELECT res.id, res.nama, res.jenis_kelamin, res.kewarganegaraan, STRING_AGG(tipe, ', ') AS tipe
        FROM (
            ({ContributorManager.filter_by_penulis_skenario()})
            UNION ALL
            ({ContributorManager.filter_by_pemain()})
            UNION ALL
            ({ContributorManager.filter_by_sutradara()})
        ) AS res
        GROUP BY res.id, res.nama, res.jenis_kelamin, res.kewarganegaraan
        """