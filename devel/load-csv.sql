\COPY operations2can(id, status, rrn, createdat, device_model, amount, tid, description, authcode, card) FROM 'payments.csv'  WITH(FORMAT CSV, DELIMITER ';', HEADER true );
