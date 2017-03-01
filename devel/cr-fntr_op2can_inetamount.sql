-- Function: fntr_op2can_inetamount()

-- DROP FUNCTION fntr_op2can_inetamount();

CREATE OR REPLACE FUNCTION fntr_op2can_inetamount()
  RETURNS trigger AS
$BODY$
DECLARE
    loc_sum NUMERIC;
    loc_dt timestamp without time ZONE;
    loc_msg BOOLEAN;
    loc_ps_id INTEGER;
BEGIN
IF new.status IN ('Voided'::CHARACTER VARYING, 'Отменен'::CHARACTER varying) THEN
    loc_sum := NULL;
    loc_dt := NULL;
    loc_msg := 'f';
    loc_ps_id := NULL;
ELSIF new.status IN ('Completed'::CHARACTER VARYING, 'Проведен'::CHARACTER varying) THEN
    loc_sum := NEW.sum;
    loc_dt := NEW.createdat::timestamp without time zone + EXTRACT(timezone FROM NEW.createdat)*(interval '1 second');
    loc_msg := 't';
    loc_ps_id := 2; -- ps_id = (SELECT id FROM payment_system WHERE ps_name = '2can')
ELSE

END IF;

UPDATE Счета 
  SET inetamount = loc_sum 
  , inetdt = loc_dt
  , Сообщение = loc_msg
  , ps_id = loc_ps_id
WHERE "№ счета" = NEW.bill_no;
    
RETURN NEW;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION fntr_op2can_inetamount()
  OWNER TO arc_energo;
