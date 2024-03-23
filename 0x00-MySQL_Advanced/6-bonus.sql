-- Creates a stored procedure AddBonus that adds a new
-- correction for a student.

DELIMITER $$

DROP PROCEDURE IF EXISTS AddBonus;

CREATE PROCEDURE AddBonus (IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project_id INT;

    IF EXISTS (SELECT * FROM projects WHERE name = project_name) THEN
        SELECT id INTO project_id FROM projects WHERE name = project_name; 

        INSERT INTO corrections
        VALUES(user_id, project_id, score);
    ELSE
        INSERT INTO projects (name)
        VALUES(project_name);
    
        SET project_id = LAST_INSERT_ID();
        
        INSERT INTO corrections
        VALUES(user_id, project_id, score);
    END IF;
END;
$$
