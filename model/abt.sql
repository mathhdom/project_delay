WITH detail_project AS ( -- 2521
    SELECT * FROM detail_project_fs
),

detail_work AS ( -- 2330 projects
    SELECT * FROM detail_work_fs
),

projects AS ( -- 2494 projects
    SELECT * FROM projects_fs
),

abt AS (
    SELECT 
        t1.project,
        t1.module,
        t1.project_status,
        t1.real_project_end,        
        
        t2.project_type,
        t2.agent,
        t2.baseline_end_date,
        t2.real_end_date,
        
        t3.baseline_date_legal_act,
        t3.legal_act,
        t3.legal_deadline,
        t3.modules_number,
        CASE WHEN t3.km IS NULL THEN 0.0 ELSE t3.km END AS km,
        CASE WHEN t3.active_power IS NULL THEN 0.0 ELSE t3.active_power END AS active_power,
        CASE WHEN t3.pos_reactive_power IS NULL THEN 0.0 ELSE t3.pos_reactive_power END AS pos_reactive_power,
        CASE WHEN t3.neg_reactive_power IS NULL THEN 0.0 ELSE t3.neg_reactive_power END AS neg_reactive_power,
        JULIANDAY(t2.real_end_date) - JULIANDAY(t3.baseline_date_legal_act) AS real_duration,
        CASE WHEN t2.real_end_date > t2.baseline_end_date THEN 1 ELSE 0 END AS deadline

    FROM detail_work AS t1

    INNER JOIN detail_project AS t2
    ON t1.project = t2.project

    INNER JOIN projects AS t3
    ON t1.project = t3.project

)

SELECT * FROM abt

