------------ FUNCTION --------------
CREATE OR REPLACE FUNCTION purchase_package_procedure() RETURNS TRIGGER AS $$
DECLARE
    is_exist BOOLEAN;
    is_today BOOLEAN;
BEGIN
    -- Check if there is an active package
    SELECT EXISTS (
        SELECT 1 FROM pacilflix.TRANSACTION
        WHERE username = NEW.username
          AND end_date_time >= CURRENT_TIMESTAMP
    ) INTO is_exist;

    -- Check if there is an active package time is today
    SELECT EXISTS (
        SELECT 1 FROM pacilflix.TRANSACTION
        WHERE username = NEW.username
          AND DATE(start_date_time) = CURRENT_DATE
          AND end_date_time >= CURRENT_TIMESTAMP
    ) INTO is_today;

    -- If there is no active package, return NEW
    IF NOT is_exist THEN
        RETURN NEW;
    
    -- If there's an active package but not for today, update the existing transaction
    ELSIF is_exist AND NOT is_today THEN
        UPDATE pacilflix.TRANSACTION
        SET nama_paket = NEW.nama_paket,
            start_date_time = NEW.start_date_time,
            end_date_time = NEW.end_date_time,
            metode_pembayaran = NEW.metode_pembayaran,
            timestamp_pembayaran = CURRENT_TIMESTAMP
        WHERE username = NEW.username
            AND start_date_time = (
                SELECT start_date_time FROM pacilflix.TRANSACTION
                WHERE username = NEW.username
                    AND end_date_time >= CURRENT_TIMESTAMP
                ORDER BY start_date_time DESC
                LIMIT 1
            );
        RETURN NULL;

    -- If there's an active package for today, update the end date and payment details
    ELSE
        UPDATE pacilflix.TRANSACTION
        SET nama_paket = NEW.nama_paket,
            end_date_time = NEW.end_date_time,
            metode_pembayaran = NEW.metode_pembayaran,
            timestamp_pembayaran = CURRENT_TIMESTAMP
        WHERE username = NEW.username
            AND DATE(start_date_time) = CURRENT_DATE;
        RETURN NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;

------------ TRIGGER --------------
CREATE TRIGGER trigger_purchase_package_procedure
BEFORE INSERT ON pacilflix.TRANSACTION
FOR EACH ROW
EXECUTE FUNCTION purchase_package_procedure();