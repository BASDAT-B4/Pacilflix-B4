class SubscriptionManager:
    def get_active_package():
        # username = request.user.username
        return f"""
        SELECT p.nama, p.harga, p.resolusi_layar, STRING_AGG(dp.dukungan_perangkat, ', ') AS dukungan_perangkat, t.start_date_time, t.end_date_time
        FROM pacilflix.PAKET AS p
        JOIN pacilflix.DUKUNGAN_PERANGKAT AS dp ON p.nama = dp.nama_paket
        JOIN pacilflix.TRANSACTION AS t ON p.nama = t.nama_paket
        WHERE t.username = 'christopher34' AND t.end_date_time >= CURRENT_TIMESTAMP
        GROUP BY p.nama, t.start_date_time, t.end_date_time
        ORDER BY t.start_date_time DESC
        LIMIT 1
        """
    
    def get_all_packages():
        return f"""
        SELECT p.nama, p.harga, p.resolusi_layar, STRING_AGG(dp.dukungan_perangkat, ', ') AS dukungan_perangkat
        FROM pacilflix.PAKET AS p
        JOIN pacilflix.DUKUNGAN_PERANGKAT AS dp ON p.nama = dp.nama_paket
        GROUP BY p.nama
        ORDER BY p.harga DESC;
        """

    def get_transaction_history():
        # username = request.user.username
        return f"""
        SELECT p.nama, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran, p.harga AS total_pembayaran
        FROM pacilflix.PAKET AS p
        JOIN pacilflix.TRANSACTION AS t ON p.nama = t.nama_paket
        WHERE t.username = 'christopher34'
        GROUP BY p.nama, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran
        ORDER BY t.start_date_time;
        """
    
    def purchase_package(nama_paket, metode_pembayaran):
        return f"""
        INSERT INTO pacilflix.TRANSACTION (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
        VALUES ('christopher34', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 month', '{nama_paket}', '{metode_pembayaran}', CURRENT_TIMESTAMP);
        """