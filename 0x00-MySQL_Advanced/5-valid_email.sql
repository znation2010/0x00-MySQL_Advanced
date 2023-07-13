-- Creates a trigger that resets the attribute valid_email
DELIMITER //
CREATE TRIGGER reset_valid_email_trigger BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END //
DELIMITER ;
