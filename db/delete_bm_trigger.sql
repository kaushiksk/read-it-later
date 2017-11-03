DELIMITER //

CREATE TRIGGER delete_bm_trigger
AFTER DELETE ON bookmark
FOR EACH ROW

BEGIN    
    UPDATE post SET post.counter=post.counter-1 WHERE post.p_id=OLD.p_id;
    
    DELETE FROM post where post.counter=0 and post.p_id=OLD.p_id;  	

    	
END//

DELIMITER ;
