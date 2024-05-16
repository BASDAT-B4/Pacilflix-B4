class ContributorManager:
    def filter_by_sutradara():
        return """
        SELECT μ.id, μ.nama, μ.jenis_kelamin, μ.kewarganegaraan, 'Sutradara' AS tipe
        FROM pacilflix.CONTRIBUTORS AS μ
        JOIN pacilflix.SUTRADARA AS ψ ON μ.id = ψ.id
        """

    def filter_by_pemain():
        return """
        SELECT μ.id, μ.nama, μ.jenis_kelamin, μ.kewarganegaraan, 'Pemain' AS tipe
        FROM pacilflix.CONTRIBUTORS AS μ
        JOIN pacilflix.PEMAIN AS π ON μ.id = π.id
        """

    def filter_by_penulis_skenario():
        return """
        SELECT μ.id, μ.nama, μ.jenis_kelamin, μ.kewarganegaraan, 'Penulis Skenario' AS tipe
        FROM pacilflix.CONTRIBUTORS AS μ
        JOIN pacilflix.PENULIS_SKENARIO AS φ ON  μ.id = φ.id
        """

    def retrieve_all_contributors():
        return f"""
        SELECT δ.id, δ.nama, δ.jenis_kelamin, δ.kewarganegaraan, STRING_AGG(tipe, ', ') AS tipe
        FROM (
            ({ContributorManager.filter_by_penulis_skenario()})
            UNION ALL
            ({ContributorManager.filter_by_pemain()})
            UNION ALL
            ({ContributorManager.filter_by_sutradara()})
        ) AS δ
        GROUP BY δ.id, δ.nama, δ.jenis_kelamin, δ.kewarganegaraan
        """