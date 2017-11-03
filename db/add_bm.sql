DELIMITER //

CREATE PROCEDURE add_bookmark
( 
    IN c_username varchar(50), 
    IN c_p_id bigint(20) unsigned,
    IN c_category varchar(50)
)
BEGIN
    
    INSERT INTO bookmark
    (
        read_status,
        time_added, 
        username, 
        p_id,
        category
    ) 
    VALUES
    (
       	b'0',
        NOW(), 
        c_username, 
        c_p_id,
        c_category
    );
    
    UPDATE post SET counter=counter+1 WHERE p_id=c_p_id;
END//

DELIMITER ;
