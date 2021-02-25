(*
* Copyright 2021
* Christopher Lee
*)
(* Below is the declaration of the exception handler: Eval_error*)
exception Eval_error
(*Below is the custom variable type to be used to create a big stemp interpreter*)
type exp =
  | True
  | False
  | If of exp * exp * exp
  | Num of int
  | IsZero of exp
  | Plus of exp * exp
  | Mult of exp * exp
(* the function below is for printing out variables of type exp that has been created and is finished *)
let rec string_of_exp (e : exp) = match e with 
  | Num(e) -> string_of_int(e)
  | True -> "true"
  | False -> "false"
  | Plus(e1,e2) -> string_of_exp(e1) ^ " + " ^ string_of_exp(e2)
  | Mult(e1,e2) -> string_of_exp(e1) ^ " * " ^ string_of_exp(e2)
  | If(e1,e2,e3) -> "if " ^ string_of_exp(e1) ^  ", then " ^ string_of_exp(e2) ^ ", else " ^ string_of_exp(e3) 
  | IsZero(e) -> "(isZero " ^ string_of_exp(e) ^ ")"
(*
*  the function below is for evaluating complex expressions down to simple ones and is NOT finished
*  currently the largest issue remains within the exception handling in having the code continue to 
*  run after the exception is hit and any expression coming out of either Plus or Mult is triggering 
*  the exception handler making inputs such as for expressions such as the ones from 5 and 6 nothing
*  more than caught "errors" instead of false in the case of successful coding or even true from cases
*  of less than successful coding
*)
  let rec eval (e : exp) = match e with
  | Num(e) -> Num (e)
  | True -> True
  | False -> False
  | Plus(e1,e2) -> (
      match e1 with 
      | Num(e1) -> (
          match e2 with 
          | Num (e2)-> eval(Num(e1+e2))
          | _ -> raise (Eval_error) )
      | _ -> raise Eval_error )
  | Mult(e1,e2) -> (
      match e1 with 
      | Num(e1) -> (
          match e2 with 
          | Num (e2) -> eval(Num (e1*e2))
          | _ -> raise Eval_error )
      | _ -> raise Eval_error )
  | If(e1,e2,e3) -> if eval(e1) = True then eval(e2) else eval(e3) 
  | IsZero(e1) -> (
      match e1 with
      | Num e1 -> (
          match (e1 = 0) with
          | true -> True
          | false -> False )
      | _ -> raise Eval_error )


  let () = 
    (*Below are all the test prompts for the syntax portion and to my knowledge all work as intended*)
    print_endline( "**********Syntax Outputs*************");
    print_endline( "1) " ^ string_of_exp(Num(3)) ) ;
    print_endline( "2) " ^ string_of_exp(True) );
    print_endline( "3) " ^ string_of_exp(False) );
    print_endline( "4) " ^ string_of_exp(Plus( Num 3,Num 2)) );
    print_endline( "5) " ^ string_of_exp(Mult( Num 3,Num 2)) );
    print_endline( "6) " ^ string_of_exp( Plus( Num 3, Plus( Num 3,Mult(Num 2,Plus( Num 3, Num 2))))) );
    print_endline( "7) " ^ string_of_exp(If( True, Num 3, Num 5 )) );
    print_endline( "8) " ^ string_of_exp(If( False, Plus(Num 3,Num 2), Plus(Num 5,Num 1) )) );
    print_endline( "9) " ^ string_of_exp(If( Plus(False,True), Plus(Num 3,False), Mult(Num 3,Num 1) )) );
    print_endline( "10) " ^ string_of_exp(If( IsZero(Num 1), Plus(Num 3,Num 2), Plus(Num 5,Num 1) )) );
    print_endline( "11) " ^ string_of_exp(IsZero(Mult(Num 3, Num 5)) ));
    print_endline( "12) " ^ string_of_exp(IsZero(If( IsZero(Num 1), Plus(Num 3,Num 2), Plus(Num 5,Num 1 ) )) ));
    print_endline( "13) " ^ string_of_exp(Plus(Num 3, If( IsZero(Num 1 ), Plus(Num 3,Num 2 ), Plus(Num 5,Num 1) ))));
    print_endline( "14) " ^ string_of_exp(Plus(Num 3, Mult(If( IsZero(Num 1), Plus(Num 3,Num 2), Plus(Num 5,Num 1) ),IsZero(True)))));
    print_endline( "15) " ^ string_of_exp(If( If(True, True, False), Plus(Num 3,Num 2), Plus(Num 5,Num 1), Plus(Num 5,Num 1) )) );
    print_endline( "16) " ^ string_of_exp(If(True, 
      If( IsZero(Mult(Num 3, Num 5)),Plus(Num 3,Num 2) ,Plus(Num 5,Num 1)),
      If(True, Mult(Num 3,Num 2), Mult(Num 2,Plus( Num 3, Num 2))) )) );;

    (*
    * Below are all the test prompts for the big step portion and to my knowledge none work as intended
    * as at the beginning until i reread the assignment i thought eval was  (e : exp) -> string instead
    * of (e : exp) -> exp
    *)
    print_endline("\n\n *******************Big Step Outputs*******************");
    print_endline( "1) " ^ eval(True) );
    print_endline( "2) " ^ eval(False) );
    print_endline( "3) " ^ eval(Num 0) );
    print_endline( "4) " ^ eval(IsZero(Num 0)) );
    print_endline( "5) " ^ eval(IsZero(Plus(Num 1, Num 1))) );
    print_endline( "6) " ^ eval (IsZero (Plus (Plus (Num 2, Num (-1)), Num 1))) );
    print_endline( "7) " ^ eval (Plus (Plus (Num (-1), Num 1), Plus (Num (-1), Num 1))) );
    print_endline( "8) " ^ eval (Plus (Num (-1), Plus (Mult (Num 2, Num 2), Num 1))) );
    print_endline( "9) " ^ eval (Plus (Plus (Plus (Num 2, Num (-1)), Num 1), Num (-1))) );
    print_endline( "10) " ^ eval (Plus (IsZero (Plus (Num (-1), Num 1)), Num 1)) );
    print_endline( "11) " ^ eval (IsZero (If (IsZero (Num 0), True, Num 0))) );
    print_endline( "12) " ^ eval (IsZero (If ( IsZero (Mult (Num 5, Num 0)), If (False, Num 0, IsZero (Plus (Num (-1), Num 0))), Num 0 ))) );
    print_endline( "13) " ^ eval (If (IsZero (Plus (Num (-1), Num 1)), Num 2, True)) );
    print_endline( "14) " ^ eval (If ( If (IsZero (Mult (Plus (Num 1, Num (-1)), Num 1)), False, True) , Mult (Num 1, Num 2) , True )) );
    print_endline( "15) " ^ eval (If ( If (IsZero (Mult (Num 0, Num 0)), IsZero (Num 2), Num 0), Mult (Num 2, Mult (Num 1, Num 1)), Plus ( Plus ( Plus( Plus (If (IsZero (Num 0), Num 1, Num 0), Num (-1)), Num 1 ), Num (-1) ), Num 1 ) )) );
  print_endline( "16) " ^ eval(If( True, If (True, Mult (If (False, Num 0, Num 1), Num 1), Num 5), Plus (Mult (Num 4, Num 1), Num 1) )) );
  print_endline( "17) " ^ eval(If( IsZero (If (IsZero (Plus (Num (-1), Num 2)), Num 0, Num 1)) , If ( True, If (False, Mult (Num 0, Num 6), Plus (Num 0, Num 1)), Num 5 ), Num 5 )) );
  print_endline( "18) " ^ eval(If ( IsZero (Plus (Num (-1), Plus (Num 1, Plus (Num (-1), Num 1)))), IsZero True, Num 1 )) );
  print_endline( "19) " ^ eval(Plus ( Num 1, Plus( Num (-1), If ( IsZero (Plus (Num 1, If (True, Num 1, Num 2))) , Plus (Num 1, Num 2), Mult (Num 2, Num 2) ) ) )) );
  print_endline( "20) " ^ eval(Plus ( Num (-1), If( IsZero (Plus (Num 5, Num (-4))), Mult (Num 123, Plus (Num 5, Num (-4))), IsZero (Num 0) ) )) );