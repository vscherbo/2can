-- Trigger: tr_op2can_BIU on operations2can

-- DROP TRIGGER "tr_op2can_BIU" ON operations2can;

CREATE TRIGGER "tr_op2can_BIU"
  BEFORE INSERT OR UPDATE
  ON operations2can
  FOR EACH ROW
  EXECUTE PROCEDURE fntr_op2can_comission();
