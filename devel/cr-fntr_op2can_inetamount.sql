-- Function: fntr_op2can_inetamount()

-- DROP FUNCTION fntr_op2can_inetamount();

CREATE OR REPLACE FUNCTION fntr_op2can_inetamount()
  RETURNS trigger AS
$BODY$BEGIN
   UPDATE Счета 
      SET inetamount = NEW.sum
      , inetdt = NEW.createdat::timestamp without time zone + EXTRACT(timezone FROM NEW.createdat)*(interval '1 second')
      , Сообщение = 't'
      , ps_id = 2
       -- ps_id = (SELECT id FROM payment_system WHERE ps_name = '2can')
      WHERE "№ счета" = NEW.bill_no;
   RETURN NEW;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION fntr_op2can_inetamount()
  OWNER TO arc_energo;
