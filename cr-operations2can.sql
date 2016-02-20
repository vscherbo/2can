-- Table: operations2can

-- DROP TABLE operations2can;

CREATE TABLE operations2can
(
  id integer NOT NULL,
  tag character varying(7), -- Операция. В xml - это tag. Значения "Payment", "Refund" ...
  amount numeric(19,2), -- Сумма. Положительное десятичное число с фиксированной точкой, кол-во цифр после точки точно равно двум.
  createdat timestamp with time zone, -- Дата создания транзакции(UTC) в Процессинге
  rrn character varying, -- Номер операции в платежной системе
  cardtype character varying, -- Тип карты: Visa, MasterCard, Maestro, AmericanExpress
  tid character varying, -- Идентификатор терминала в банке
  mid character varying, -- Клише mPOS
  card character varying, -- Первые 6 и последние 4 цифры номера карты в формате ...
  description character varying, -- Описание, указанное при оплате
  authcode character varying,
  status character varying NOT NULL, -- Состояние платежа...
  device_id integer, -- Уникальный идентификатор устройства в Процессинге
  device_name character varying, -- Название устройства, указанное пользователем
  device_model character varying, -- Модель устройства
  payment integer, -- Идентификатор транзакции, для которой проводится отмена/возврат
  sum numeric(19,2), -- Сумма за вычетом комиссии
  bill_no integer,
  CONSTRAINT operations2can_pk PRIMARY KEY (id, status)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE operations2can
  OWNER TO arc_energo;
COMMENT ON TABLE operations2can
  IS 'Уведомления от 2can об опреациях';
COMMENT ON COLUMN operations2can.tag IS 'Операция. В xml - это tag. Значения "Payment", "Refund" ...';
COMMENT ON COLUMN operations2can.amount IS 'Сумма. Положительное десятичное число с фиксированной точкой, кол-во цифр после точки точно равно двум.';
COMMENT ON COLUMN operations2can.createdat IS 'Дата создания транзакции(UTC) в Процессинге';
COMMENT ON COLUMN operations2can.rrn IS 'Номер операции в платежной системе';
COMMENT ON COLUMN operations2can.cardtype IS 'Тип карты: Visa, MasterCard, Maestro, AmericanExpress';
COMMENT ON COLUMN operations2can.tid IS 'Идентификатор терминала в банке';
COMMENT ON COLUMN operations2can.mid IS 'Клише mPOS';
COMMENT ON COLUMN operations2can.card IS 'Первые 6 и последние 4 цифры номера карты в формате 
NNNNNN** **** **** NNNN';
COMMENT ON COLUMN operations2can.description IS 'Описание, указанное при оплате';
COMMENT ON COLUMN operations2can.status IS 'Состояние платежа
Completed - проведен
Voided - отменен';
COMMENT ON COLUMN operations2can.device_id IS 'Уникальный идентификатор устройства в Процессинге';
COMMENT ON COLUMN operations2can.device_name IS 'Название устройства, указанное пользователем';
COMMENT ON COLUMN operations2can.device_model IS 'Модель устройства';
COMMENT ON COLUMN operations2can.payment IS 'Идентификатор транзакции, для которой проводится отмена/возврат';
COMMENT ON COLUMN operations2can.sum IS 'Сумма за вычетом комиссии';


-- Trigger: tr_op2can_AI on operations2can

-- DROP TRIGGER "tr_op2can_AI" ON operations2can;

CREATE TRIGGER "tr_op2can_AI"
  AFTER INSERT
  ON operations2can
  FOR EACH ROW
  EXECUTE PROCEDURE fntr_op2can_inetamount();
COMMENT ON TRIGGER "tr_op2can_AI" ON operations2can IS 'Записывает sum в Счета.inetamount';

-- Trigger: tr_op2can_BIU on operations2can

-- DROP TRIGGER "tr_op2can_BIU" ON operations2can;

CREATE TRIGGER "tr_op2can_BIU"
  BEFORE INSERT OR UPDATE
  ON operations2can
  FOR EACH ROW
  EXECUTE PROCEDURE fntr_op2can_comission();

