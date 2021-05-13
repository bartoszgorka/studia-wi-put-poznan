; Architektura Systemów Komputerowych
; Laboratorium nr 
; Temat: Obsługa wyświetlacza LCD
; Autor: Bartosz Górka [INF127228] - 14.05.2017r.

; Dyrektywa "pracy"
$MOD842

; Przypisania etykiet dla wygodniejszej pracy z urządzeniem - sposób połączenia LCD z układem sterowania (mikrokontrolerem)
; Dane
	LCD_D4  EQU P2.1
	LCD_D5  EQU P2.0
	LCD_D6  EQU P2.3
	LCD_D7  EQU P2.2

; Sterowanie
	LCD_E   EQU P2.5
	LCD_RW  EQU P2.4
	LCD_RS  EQU P2.7

; Cały port by było łatwiej edytować
	LCD_PORT EQU P2

; Początek danych w pamięci
	LCD_DATA EQU 30h


ORG 000h
JMP MAIN_CODE

; Inicjalizacja pamięci układu
INIT_SYSTEM:
	; Załadowanie do pamięci układu liter
	; Linia pierwsza
		MOV 030H, #'B'
		MOV 031H, #'A'
		MOV 032H, #'R'
		MOV 033H, #'T'
		MOV 034H, #'O'
		MOV 035H, #'S'
		MOV 036H, #'Z'
		MOV 037H, #0 ; Znacznik końca danych

	; Linia druga
		MOV 040H, #'G'
		MOV 041H, #'O'
		MOV 042H, #'R'
		MOV 043H, #'K'
		MOV 044H, #'A'
		MOV 045H, #0 ; Koniec danych

	RET

; Transfer danych z pamięci do wyświetlacza
SEND_TO_LCD:
	MOV R0, LCD_DATA
	SETB LED_RS
	CLR LED_RW

	PIERWSZA_LINIA:
		MOV A, @R0
		JZ DRUGA_LINIA ; Jeżeli mamy 0 czyli koniec ciągu znaków to skaczemy do drugiej linii danych
		
		CALL SEND_DATA
		INC R0
	JMP PIERWSZA_LINIA

	DRUGA_LINIA:
	MOV R0, #040H

	DRUGA_LINIA_ZAPIS:
		MOV A, @R0
		JZ KONIEC_ZAPISU

		CALL SEND_DATA
		INT R0
	JMP DRUGA_LINIA_ZAPIS

	FINISH:
		RET

; Funkcja zapisu danych z pamięci do LCD
SEND_DATA:
	MOV C, ACC.7
	MOV LED_D7, C
	MOV C, ACC.6
	MOV LED_D6, C
	MOV C, ACC.5
	MOV LED_D5, C
	MOV C, ACC.4
	MOV LED_D4, C

	SETB LED_E
	CLR LED_E

	MOV C, ACC.3
	MOV LED_D7, C
	MOV C, ACC.2
	MOV LED_D6, C
	MOV C, ACC.1
	MOV LED_D5, C
	MOV C, ACC.0
	MOV LED_D4, C

	SETB LED_E
	CLR LED_E

	CALL DELAY

	RET

; Mode - tryb pracy na przesuwanie kursora w lewo po zapisie
LCD_MODE_SETUP:
	CLR LED_RS
	CLR LED_RW

	CLR LED_D7
	CLR LED_D6
	CLR LED_D5
	CLR LED_D4

	SETB LED_E
	CLR LED_E

	CLR LED_D7
	SETB LED_D6
	SETB LED_D5
	CLR LED_D4

	SETB LED_E
	CLR LED_E

	RET

; Włączenie wyświetlacza, włączenie kursora, włączenie migania
LCD_SET_ON:
	CLR LCD_RS
	CLR LCD_RW

	; 1 CZĘŚĆ DANYCH
		CLR LCD_D7
		CLR LCD_D6
		CLR LCD_D5
		CLR LCD_D4

	; ZATWIERDZENIE DANYCH
		SETB LCD_E
		CLR LCD_E

	; 2 CZĘŚĆ DANYCH
		SETB LCD_D7
		SETB LCD_D6
		SETB LCD_D5
		SETB LCD_D4

	; ZATWIEDZENIE DANYCH
		SETB LCD_E
		CLR LCD_E
	RET	

; Wyłączenie wyświetlacza
LCD_SET_OFF:
	; 1 CZĘŚĆ DANYCH + RS NA 0, RW NA 0
		CLR LCD_PORT

	; ZATWIERDZENIE DANYCH
		SETB LCD_E
		CLR LCD_E

	; 2 CZĘŚĆ DANYCH
		CLR LCD_PORT

	; ZATWIEDZENIE DANYCH
		SETB LCD_E
		CLR LCD_E
	RET

; Zmiana trybu pracy na 4-bitowy
LCD_FOUR_BITS:
	; TRYB
		CLR LED_RS
		CLR LED_RW

	; 1 CZĘŚĆ DANYCH
		CLR LED_D7
		CLR LED_D6
		SETB LED_D5
		CLR LED_D4

	; POTWIERDZENIE WPISU
		SETB LED_E
		CLR LED_E

	; 2 CZĘŚĆ DANYCH
		SETB LED_D7 ; N = 1 -> 2 LINIE
		SETB LED_D6 ; F = 1 -> 5 x 10 FORMAT ZNAKÓW

	; POTWIERDZENIE
		SETB LED_E
		CLR LED_E
	RET

DELAY:
	MOV R7, #0FFH
	DEL2:	
	MOV R6, #0FFH
	DJNZ R6, $
	DJNZ R7, DEL2
	RET

LCD_CLEAR_DATA:
	CLR LED_PORT

	SETB LED_E
	CLR LED_E

	CLR LED_PORT
	SETB LED_D4

	SETB LED_E
	CLR LED_E

	RET

MAIN_CODE:
	CALL INIT_SYSTEM
	CALL LCD_FOUR_BITS
	CALL LCD_SET_ON
	CALL LCD_MODE_SETUP
	CALL LCD_CLEAR_DATA
	CALL SEND_TO_LCD

PETLA
	SJMP $

END