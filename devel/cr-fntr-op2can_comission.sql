-- Function: fntr_op2can_comission()

-- DROP FUNCTION fntr_op2can_comission();

CREATE OR REPLACE FUNCTION fntr_op2can_comission()
  RETURNS trigger AS
$BODY$BEGIN
IF NEW.tag = 'Payment' AND NEW.status IN ('Completed', 'Проведен')
THEN
    NEW.Sum = NEW.Amount - ROUND(NEW.Amount * 0.0275, 2);
ELSE -- Refund or Voided
    NEW.Sum = NEW.Amount;
END IF;
   
BEGIN
    NEW.bill_no = (REGEXP_REPLACE(NEW.description, '[^0-9]+', '', 'g'))::INTEGER;
EXCEPTION WHEN OTHERS THEN
    NEW.bill_no = NULL;
END;

RETURN NEW;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION fntr_op2can_comission()
  OWNER TO arc_energo;
