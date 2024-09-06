WITH project_by_module AS (

    SELECT 
        Empreendimento AS project,
        "Módulo" AS module,
        "Situação" AS project_status,
        "Conclusão" AS real_project_end

    FROM detail_work

)

SELECT * FROM project_by_module