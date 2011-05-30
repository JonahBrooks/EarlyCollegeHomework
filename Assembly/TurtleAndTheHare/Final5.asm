TITLE MASM FinalProblem5					(Final5.asm)
;---------------------------------------------------------------------------;
; Name: Jonah Brooks						Class: CS271 Fall 2010			;
; Date: 12-03-2010							Problem: Final, problem 5		;
;																			;
;	Description:															;
;		Simulates tortoise and the hare in a console window					;
;	EAX: loopDelay				DI: turtlePos		SI: harePos				;
;	EDX: OFFSET track			CL:	winStatus		CH: loopCount (time)	;
;---------------------------------------------------------------------------;
INCLUDE Irvine32.inc

.data
	track BYTE 70 DUP (" "), "|", 0
	ouchMsg		 BYTE "OUCH!!!", 0	
	turtleWinMsg BYTE "TORTOISE WINS!!! YAY!!!", 0Ah, 0Dh, 0
	hareWinMsg   BYTE "Hare wins. Yuch.", 0Ah, 0Dh, 0
	tieMsg		 BYTE "It's a tie.", 0Ah, 0Dh, 0
	timeMsg		 BYTE "TIME ELAPSED = ", 0
	secMsg		 BYTE " seconds", 0Ah, 0Dh, 0
	startMsg	 BYTE "ON YOUR MARK, GET SET ", 0Ah, 0Dh,
					  "BANG !!!! ", 0Ah, 0Dh,
					  "AND THEY'RE OFF !!!!", 0Ah, 0Dh, 0
.code
main PROC
	call ClrScr
	call Randomize
	MOV EDX, OFFSET startMsg
	call WriteString
	MOV EDX, OFFSET track
	MOV EAX, 1000		; loopDelay
	MOV EDI, 0			; Starting turtlePos
	MOV ESI, 0			; Starting harePos
	MOV CL, 0			; Initialize winStatus to 0
	MOV CH, 0			; Time = 0 seconds

 gameLoop:
	call MoveTurtle		; move the turtle and update string, DI = turtlePos
	call MoveHare		; move hare and update string, SI = harePos

	call WriteString	; Display the track to the screen
	CMP DI, SI			; compare turtlePos to harePos
	JNE dontShowOuch
		call PrintOuch	; Overwrite the track with the word "OUCH!!!"
    dontShowOuch:
	call Crlf

	call Delay		; Wait one second
	INC CH			; Add one second to loopCount, to keep track of total time ellapsed
				;Check CL for win condition
				; 0: no win yet,		1: Turtle,		2: Hare,		3: Tie
	CMP CL, 0			
		JE gameLoop		; run this loop again if no one has won yet
	
	call DisplayWinMsg
	call WaitMsg
	exit
main ENDP

;---------------------------------------------------------------------------;
;	MoveTurtle:																;
;			Calculates a random number between 1-10 to determine how the	;
;		turtle should move. Updates the string to erase the old turtle and	;
;		draw the new turtle, also updates DI with the new position			;
;	Receives:	DI = Turtle's current position								;
;	Returns:	DI = Turtle's new position									;
;				CL = winStatus (0: no win, 1: turtle wins, 3: tie with hare);
;---------------------------------------------------------------------------;
MoveTurtle PROC USES EAX EDX
	CMP DI, SI
	JE dontKillTheHare			; If the hare didn't just move into it...
		MOV track[DI], " "		; ...clear the turtle's current position
	dontKillTheHare:

		; ----- Update Position With Random Rolls ------
	MOV EAX, 10
	call RandomRange
	INC EAX		; Range from 1 to 10 inclusive
	
	CMP EAX, 5
	JG notFastPlod
  fastPlod: 
		ADD DI, 3		; fastPlod, move forward 3
	    JMP doneMovingTurtle
  notFastPlod:
	CMP EAX, 7
	JG slowPlod
  slip:
		SUB DI, 6	; slip, move backward 6
		JMP doneMovingTurtle
  slowPlod:
		ADD DI, 1		; slowPlod, move forward 1

  doneMovingTurtle:

		; ----- Validate Position -----
	CMP DI, 0
	JNL onTrack1
		MOV DI, 0		; Don't slip past the starting line
    onTrack1:
	
	CMP DI, 69
	JL onTrack2
		MOV DI, 69		; Stop at the finish line
		INC CL			; Add one to CL, to indicate that the turtle passed the finish line
	onTrack2:
		
		; ---- Update Position in registers and string ----
	MOV track[DI], "T"		; Fill in the turtle's new position
	ret
MoveTurtle ENDP

;---------------------------------------------------------------------------;
;	MoveHare:																;
;			Calculates a random number between 1-10 to determine how the	;
;		hare should move. Updates the string to erase the old hare and		;
;		draw the new hare, also updates SI with the new position			;
;	Receives:	SI = Turtle's current position								;
;	Returns:	SI = Turtle's new position									;
;				CL = winStatus (0: no win, 2: hare wins, 3: tie with turtle);
;---------------------------------------------------------------------------;
MoveHare PROC USES EAX EDX
	CMP DI, SI
	JE dontKillTheTurtle			; If the turtle didn't just move into it...
		MOV track[SI], " "			; ...clear the hare's current position
	dontKillTheTurtle:		

		; ----- Update Position With Random Rolls ------
	MOV EAX, 10
	call RandomRange
	INC EAX		; Range from 1 to 10 inclusive
	
	CMP EAX, 2
	JG notSleep
  zzz: 
	    JMP doneMovingHare	; sleep, don't move the hare
  notSleep:
	CMP EAX, 4
	JG notBigHop
  bigHop:
		ADD SI, 9			; bigHop, jump forward 9
		JMP doneMovingHare
  notBigHop:
	CMP EAX, 5
	JG notBigSlip
  bigSlip:
		SUB SI, 12			; bigSlip, move back 12
		JMP doneMovingHare
  notBigSlip:
	CMP EAX, 8
	JG smallSlip
  smallHop:
		ADD SI, 1			; smallHop, move forward 1
		JMP doneMovingHare
  smallSlip:
		SUB SI, 2			; smallSlip, move backward 2

  doneMovingHare:

		; ----- Validate Position -----
	CMP SI, 0
	JNL onTrack1
		MOV SI, 0		; Don't slip past the starting line
    onTrack1:
	
	CMP SI, 69
	JL onTrack2
		MOV SI, 69		; Stop at the finish line
		ADD CL, 2		; Add two to CL, to indicate that the hare passed the finish line
	onTrack2:
		
		; ---- Update Position in registers and string ----
	MOV track[SI], "H"
	ret
MoveHare ENDP

;---------------------------------------------------------------------------;
;	PrintOuch:																;
;			Prints the word "OUCH!!!" over the track, starting at the		;
;		position of the turtle, which is held in DI							;
;	Receives:	DI = Turtle's current position								;
;	Returns:	Nothing, it just prints to the screen						;
;---------------------------------------------------------------------------;
PrintOuch PROC USES EAX ECX EDX
	MOV EDX, OFFSET ouchMsg
	MOV AL, 0Dh			; Print a carriage return to write over the track...
	call WriteChar		; ... to keep the "Finish Line" character at the end
	MOV AL, " "	
	MOVSX ECX, DI
	JECXZ postIndentation
 lIndentToTurtle:
	  call WriteChar		; Print spaces starting at index 0 and going to turtlePos
	LOOP lIndentToTurtle
 postIndentation:
	call WriteString		; Display "OUCH!!!" at that position
	ret
PrintOuch ENDP

;---------------------------------------------------------------------------;
;	DisplayWinMsg:															;
;			Recieves the winStatus variable in register CL, and prints the	;
;		corresponding win message and the total time elapsed during the race;
;	Receives:	CL = {1: turtle wins, 2: hare wins, 3: race was a tie}		;								;
;	Returns:	Nothing, it only displays output to the screen				;
;---------------------------------------------------------------------------;
DisplayWinMsg PROC USES EDX EAX
	CMP CL, 2			; The "middle" win condition
	JE hareWins			; If CL equals 2, the hare won
	JL turtleWins
	JG tie
	
	hareWins:
		MOV EDX, OFFSET HareWinMsg
		JMP resultsAreIn
	turtleWins:
		MOV EDX, OFFSET TurtleWinMsg
		JMP resultsAreIn
	tie:
		MOV EDX, OFFSET TieMsg

	resultsAreIn:
		call WriteString	; Print the fanfare for the winning animal 
	MOV EDX, OFFSET timeMsg
	call WriteString
	MOVSX EAX, CH			; Move the loopCount into EAX to print
	call WriteDec			; Print that number to the screen
	MOV EDX, OFFSET secMsg			
	call WriteString		; And print the " seconds" to end it
	ret
DisplayWinMsg ENDP

END main