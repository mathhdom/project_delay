-- Calculate the current accuracy by the planned end
    -- Real end and Baseline end - I already have it (detalhamento dos empreendimentos)
    -- feature will be the start date
-- Calculate the model accuracy by prediction and Real end
    -- feature will be the start date
WITH dates AS (
    
    SELECT 

        Empreendimento AS project,
        MIN(COALESCE(
            "Início - Efetiva",
            "Conclusão - Efetiva",
            "Início - Prevista",
            "Conclusão - Prevista"
        )) AS first_start_date

    FROM schedule

    GROUP BY Empreendimento
)

SELECT * FROM dates