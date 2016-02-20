-- Function: fntr_op2can_comission()

-- DROP FUNCTION fntr_op2can_comission();

CREATE OR REPLACE FUNCTION fntr_op2can_comission()
  RETURNS trigger AS
$BODY$BEGIN
   NEW.Sum = NEW.Amount - ROUND(NEW.Amount * 0.0275, 2);
   NEW.bill_no = (REGEXP_REPLACE(COALESCE(NEW.description,'0'), '[^0-9]+', '', 'g'))::INTEGER;
   RETURN NEW;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION fntr_op2can_comission()
  OWNER TO arc_energo;
