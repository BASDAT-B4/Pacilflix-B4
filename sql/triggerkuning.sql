
CREATE OR REPLACE FUNCTION restrict_hapus_unduhan () RETURNS TRIGGER AS $$
BEGIN
    IF OLD.timestamp BETWEEN (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta') - INTERVAL '24 hours' AND
                               CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta' THEN
        RAISE EXCEPTION 'Tayangan minimal harus berada di daftar unduhan selama 1 hari agar bisa dihapus.';
    ELSE
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_hapus_unduhan BEFORE DELETE ON pacilflix.TAYANGAN_TERUNDUH FOR EACH ROW
EXECUTE FUNCTION restrict_hapus_unduhan ();