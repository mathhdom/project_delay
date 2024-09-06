SELECT 

    Empreendimento AS project,
    Tipo AS project_type,
    Transmissora AS agent,
    "Data Ato Legal" AS baseline_date_legal_act,
    "Ato Legal" AS legal_act,
    "Situação Cronograma" AS schedule_status,
    "Conclusão Previsão Efetiva" AS real_prediction_date,
    "Prazo Legal dias" AS legal_deadline,
    "Atraso Previsto dias" AS expected_delay,
    "N° Obras" AS modules_number,
    "Acréscimo KM" AS km,
    "Acréscimo Pot Ativa" AS active_power,
    "Acréscimo Pot Reat Positiva" AS pos_reactive_power,
    "Acréscimo Pot Reat Negativa" AS neg_reactive_power

FROM projects;