-- creates a stored procedure ComputeAverageWeightedScoreForUser that
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight) INTO total_weighted_score
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    SELECT SUM(projects.weight) INTO total_weight
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    UPDATE users
    SET average_score = total_weighted_score / total_weight
    WHERE id = user_id;
END //
DELIMITER ;
