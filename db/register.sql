DELIMITER //

CREATE PROCEDURE register
(
    IN c_first_name varchar(50), 
    IN c_last_name varchar(50), 
    IN c_username varchar(50), 
    IN c_password varchar(200), 
    IN c_email varchar(50), 
    IN c_roll_no char(50), 
    IN c_d_id varchar(10)
)
BEGIN
    IF ( SELECT EXISTS (SELECT 1 FROM users WHERE username = c_username) ) THEN

        select 'fail_username';

    ELSEIF ( SELECT EXISTS (SELECT 1 FROM users WHERE email = c_email) ) THEN

        select 'fail_email';

    ELSEIF ( SELECT EXISTS (SELECT 1 FROM users WHERE roll_no = c_roll_no) ) THEN

        select 'fail_roll_no';    

    ELSE
    INSERT INTO users
    (
        first_name,
        last_name, 
        username, 
        password, 
        email, 
        roll_no, 
        d_id
    ) 
    VALUES
    (
        c_first_name,
        c_last_name, 
        c_username, 
        c_password, 
        c_email, 
        c_roll_no, 
        c_d_id
    );
    select 'success';
    END IF;
END//

DELIMITER ;
