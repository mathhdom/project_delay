SELECT 

    "Status do empreendimento" AS status_project,
    "Status do cronograma" AS status_schedule,
    "Tipo do empreend." AS project_type,
    "Transmissora" AS agent,
    SUBSTR("Empreendimento", 1, INSTR("Empreendimento", ' - ') - 1) AS project,
    "Ato legal" AS baseline_end_date,
    "Conclusão informada" AS real_end_date

FROM detail_project