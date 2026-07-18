CREATE VIEW candidate_status AS
SELECT
    c.candidate_id,
    c.name,
    p.position_name,
    a.recruitment_year,
    s.stage_name AS current_stage,
    CASE
        WHEN a.current_stage_id BETWEEN 0 AND 2 THEN ns.stage_name
        ELSE NULL
    END AS next_stage,
    a.next_interview_date
FROM applications a
JOIN candidates c
    ON a.candidate_id = c.candidate_id
JOIN positions p
    ON a.position_id = p.position_id
JOIN selection_stages s
    ON a.current_stage_id = s.stage_id
LEFT JOIN selection_stages ns
    ON ns.stage_id = a.current_stage_id + 1;
