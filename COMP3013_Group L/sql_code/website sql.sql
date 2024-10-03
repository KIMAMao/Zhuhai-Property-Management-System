-- check username exist or not
SELECT u_id FROM users WHERE u_id = user_id;

-- check email exist or not
SELECT email FROM users WHERE u_id = user_id;

-- create users
INSERT INTO users VALUES (user_id, username, password, email);

-- delete users
DELETE FROM users WHERE u_id = user_id;

-- update users
UPDATE users 
SET u_id = user_id, name = username, password = password, email = email 
WHERE u_id = user_id;

-- create agents
INSERT INTO agents VALUES (user_id, username, password, email, phone, NOW(), NULL);

-- delete agents
DELETE FROM agents WHERE u_id = user_id;

-- update agents
UPDATE agents 
SET u_id = user_id, name = username, password = password, email = email, phone = phone, intro = intro
WHERE u_id = user_id;

-- create admin
INSERT INTO admins VALUES (user_id, username, password, email);

-- update admin
UPDATE admins 
SET u_id = user_id, name = username, password = password, email = email
WHERE u_id = user_id;

-- apply show in users' interface
(SELECT * FROM new_apply WHERE user_id = user_id) 
UNION 
(SELECT * FROM old_apply WHERE user_id = user_id);

-- fav show in users' interface
(SELECT * FROM new_fav WHERE u_id = user_id) 
UNION 
(SELECT * FROM old_fav WHERE u_id = user_id);

-- users show in agent's interface
SELECT * FROM users ORDER BY u_id;

-- charged houses show in agent's interface
(SELECT * FROM new_house WHERE agent_id = user_id) 
UNION 
(SELECT * FROM old_house WHERE agent_id = user_id);

-- related apply show in agent's interface
-- added new
(SELECT * FROM new_apply JOIN new_house ON (house_id = h_num AND sub_id = s_num) WHERE agent_id = user_id) 
UNION 
(SELECT * FROM old_apply JOIN old_house ON (house_id = h_num AND sub_id = s_num) WHERE agent_id = user_id);

-- agents show in admin's interface
SELECT * FROM agents ORDER BY u_id;

-- show admins interface
SELECT * FROM admins ORDER BY u_id;

-- users show in admin's interface
SELECT * FROM users ORDER BY u_id;

-- mvp show in admin's interface
SELECT * FROM mvp ORDER BY u_id;

-- delete fav
DELETE FROM (
    (SELECT * FROM new_fav WHERE u_id = user_id) 
    UNION 
    (SELECT * FROM old_fav WHERE u_id = user_id)
) WHERE sub_id = sub_id;

-- agent delete house
DELETE FROM (
    (SELECT * FROM new_house WHERE agent_id = user_id) 
    UNION 
    (SELECT * FROM old_house WHERE agent_id = user_id)
) WHERE h_num = house_id;

-- admin add mvp
INSERT INTO mvp VALUES (user_id, agent_id, NOW());

-- admin delete mvp
DELETE FROM mvp WHERE agent_id = agent_id;

-- add apply for new house
INSERT INTO new_apply VALUES (user_id, sub_id, house_id, msg);

-- check apply in new house
SELECT user_id, sub_id, house_id 
FROM new_apply 
WHERE user_id = user_id AND sub_id = sub_id AND house_id = house_id;

-- add apply for old house
INSERT INTO old_apply VALUES (user_id, sub_id, house_id, msg);

-- check apply in old house (one user cannot apply one house for multiple times)
SELECT user_id, sub_id, house_id 
FROM old_apply 
WHERE user_id = user_id AND sub_id = sub_id AND house_id = house_id;

-- add fav for new subdivision
INSERT INTO new_fav VALUES (sub_id, user_id);

-- check fav in new subdivision (one user cannot fav one house for multiple times)
SELECT * FROM new_fav WHERE sub_id = sub_id AND user_id = user_id;

-- add fav for old subdivision
INSERT INTO old_fav VALUES (sub_id, user_id);

-- check fav in old subdivision (one user cannot fav one house for multiple times)
SELECT * FROM old_fav WHERE sub_id = sub_id AND user_id = user_id;

-- show all new subdivision
SELECT * FROM new_subdivision ORDER BY price;

-- show one new subdivision
SELECT * FROM new_subdivision WHERE id = sub_id;

-- show all old subdivision
SELECT * FROM old_subdivision ORDER BY price;

-- show one old subdivision
SELECT * FROM old_subdivision WHERE id = sub_id;

-- show houses for a new subdivision
SELECT * FROM new_house JOIN new_subdivision ON (s_num = id) WHERE s_num = sub_id;

-- show houses for a old subdivision
SELECT * FROM old_house JOIN old_subdivision ON (s_num = id) WHERE s_num = sub_id;

-- show new houses info
SELECT * FROM new_house WHERE s_num = sub_id AND h_num = house_id;

-- show old houses info
SELECT * FROM old_house WHERE s_num = sub_id AND h_num = house_id;