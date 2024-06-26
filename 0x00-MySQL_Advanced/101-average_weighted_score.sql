-- Creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for every student

DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE project_weight_sum INT;
    DECLARE score_project_weight FLOAT;
    DECLARE user_count INT;
    DECLARE loop_count INT;

    SELECT COUNT(*) INTO user_count
    FROM users;

    IF user_count > 1 THEN
        SET loop_count = user_count - (user_count - 1);
    ELSEIF user_count = 1 THEN
        SET loop_count = user_count;
    END IF; 
    
    WHILE loop_count <= user_count AND loop_count > 0 DO
        SELECT SUM(projects.weight * corrections.score)
        INTO score_project_weight
        FROM projects
        JOIN corrections
        ON corrections.user_id = loop_count AND projects.id = corrections.project_id;

        SELECT SUM(projects.weight)
        INTO project_weight_sum
        FROM corrections
        JOIN projects
        ON corrections.user_id = loop_count AND corrections.project_id = projects.id;
        
        UPDATE users
        SET average_score = (score_project_weight / project_weight_sum)
        WHERE id = loop_count;

        SET loop_count = (loop_count + 1);
    END WHILE;

END;
$$
