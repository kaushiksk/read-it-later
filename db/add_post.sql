DELIMITER //

CREATE PROCEDURE add_post
( 
    IN c_url varchar(512),
    IN c_title text,
    IN c_description longtext,
    IN c_thumb text 
)
BEGIN
    
    INSERT INTO post
    (
       url,
       title,
       description,
       thumb,
       counter
    ) 
    VALUES
    (
       c_url,
       c_title,
       c_description,
       c_thumb,
       0
    );
END//

DELIMITER ;
