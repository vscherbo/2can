
DROP TRIGGER "tr_op2can_AIU" ON operations2can;

CREATE TRIGGER "tr_op2can_AIU"
  AFTER INSERT OR UPDATE
  ON operations2can FOR EACH ROW
  EXECUTE PROCEDURE fntr_op2can_inetamount();
