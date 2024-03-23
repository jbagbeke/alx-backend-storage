-- Creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student

DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE project_weight_sum INT;
    DECLARE score_project_weight FLOAT;

    SELECT SUM(projects.weight * corrections.score)
    INTO score_project_weight
    FROM projects
    JOIN corrections
    ON corrections.user_id = user_id AND projects.id = corrections.project_id;

    SELECT SUM(projects.weight)
    INTO project_weight_sum
    FROM corrections
    JOIN projects
    ON corrections.user_id = user_id AND corrections.project_id = projects.id;

    UPDATE users
    SET average_score = (score_project_weight / project_weight_sum)
    WHERE id = user_id;
END;
$$
