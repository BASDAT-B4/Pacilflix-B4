CREATE OR REPLACE FUNCTION check_username_exists()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM PENGGUNA WHERE username = NEW.username) THEN
        RAISE EXCEPTION 'Username % sudah terdaftar', NEW.username;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_username
BEFORE INSERT ON PENGGUNA
FOR EACH ROW
EXECUTE FUNCTION check_username_exists();

