# data constraints

-- new house price cannot be 0
ALTER TABLE new_house
ADD CONSTRAINT new_house_price_domain
CHECK (price <> "0元" AND price <> "0");


-- new house area cannot be 0
ALTER TABLE new_house
ADD CONSTRAINT new_house_area_domain
CHECK (area <> "0㎡" AND area <> "0");


-- new house room_num cannot be 0
ALTER TABLE new_house
ADD CONSTRAINT new_house_room_num_domain
CHECK (room_num <> "0室0厅0卫" AND room_num <> "0");


--old house price cannot be 0
ALTER TABLE old_house
ADD CONSTRAINT old_house_price_domain
CHECK (price <> "0元" AND price <> "0");


-- old house area cannot be 0
ALTER TABLE old_house
ADD CONSTRAINT old_house_area_domain
CHECK (area <> "0㎡" AND area <> "0");


-- old house room_num cannot be 0
ALTER TABLE old_house
ADD CONSTRAINT old_house_room_num_domain
CHECK (room_num <> "0室0厅0卫" AND room_num <> "0");


-- new subdivision price cannot be 0
ALTER TABLE new_subdivision
ADD CONSTRAINT new_subdivision_price_domain
CHECK (price <> "0元" AND price <> "0");


-- old subdivision price cannot be 0
ALTER TABLE old_subdivision
ADD CONSTRAINT old_subdivision_price_domain
CHECK (price <> "0元" AND price <> "0");


-- trigger and constraints

-- delete or update one house from old_house then old_apply change
ALTER TABLE old_apply
ADD CONSTRAINT old_house_apply
FOREIGN KEY (house_id, sub_id) REFERENCES old_house(h_num, s_num)
	ON DELETE CASCADE
	ON UPDATE CASCADE;


-- delete or update one house from new_house then new_apply change
ALTER TABLE new_apply
ADD CONSTRAINT new_house_apply
FOREIGN KEY (house_id, sub_id) REFERENCES new_house(h_num, s_num)
	ON DELETE CASCADE
	ON UPDATE CASCADE;


-- delete one agent then mvp, new_house and old_house change as agent_id changed
DELIMITER |
CREATE TRIGGER delete_agent
BEFORE DELETE ON agents 
FOR EACH ROW
BEGIN
	IF old.u_id IN (
		SELECT DISTINCT agent_id FROM old_house
		UNION
		SELECT DISTINCT agent_id FROM new_house
	) THEN 
		UPDATE new_house 
      	SET agent_id = (SELECT u_id FROM agents ORDER BY rand() LIMIT 1)
      	WHERE new_house.agent_id = old.u_id;
      
    	UPDATE old_house 
      	SET agent_id = (SELECT u_id FROM agents ORDER BY rand() LIMIT 1)
      	WHERE old_house.agent_id = old.u_id;
        
        DELETE FROM mvp WHERE agent_id = old.u_id;
	END IF;
END;|
DELIMITER ;


-- update one agent then new_house and old_house change as agent_id changed
DELIMITER |
CREATE TRIGGER update_agent
BEFORE UPDATE ON agents 
FOR EACH ROW
BEGIN
	IF old.u_id IN (
		SELECT DISTINCT agent_id FROM old_house
		UNION
		SELECT DISTINCT agent_id FROM new_house
	) THEN 
		UPDATE new_house 
      	SET agent_id = new.u_id
      	WHERE new_house.agent_id = old.u_id;
      
    	UPDATE old_house 
      	SET agent_id = new.u_id
      	WHERE old_house.agent_id = old.u_id;

    	UPDATE mvp 
      	SET agent_id = new.u_id
      	WHERE mvp.agent_id = old.u_id;
	END IF;
END;|
DELIMITER ;


-- delete one user then new_fav, old_fav, new_apply, and old_apply change as u_id changed
DELIMITER |
CREATE TRIGGER delete_user
BEFORE DELETE ON users
FOR EACH ROW
BEGIN
	DELETE FROM new_fav WHERE new_fav.u_id = old.u_id;
    DELETE FROM old_fav WHERE old_fav.u_id = old.u_id;
    DELETE FROM new_apply WHERE new_apply.user_id = old.u_id;
    DELETE FROM old_apply WHERE old_apply.user_id = old.u_id;
END;|
DELIMITER ;


-- update one user then new_fav, old_fav, new_apply, and old_apply change as u_id changed
DELIMITER |
CREATE TRIGGER update_user
BEFORE update ON users
FOR EACH ROW
BEGIN
	UPDATE new_fav 
	SET u_id = new.u_id
    WHERE new_fav.u_id = old.u_id;
   
    UPDATE old_fav 
    SET u_id = new.u_id
    WHERE old_fav.u_id = old.u_id;
   
    UPDATE new_apply 
    SET user_id = new.u_id
    WHERE new_apply.user_id = old.u_id;
   
    UPDATE old_apply 
    SET user_id = new.u_id
    WHERE old_apply.user_id = old.u_id;
END;|
DELIMITER ;