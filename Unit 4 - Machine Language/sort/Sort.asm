// This file is part of nand2tetris, as taught in The Hebrew University,
// and was written by Aviv Yaish, and is published under the Creative 
// Common Attribution-NonCommercial-ShareAlike 3.0 Unported License 
// https://creativecommons.org/licenses/by-nc-sa/3.0/

// An implementation of a sorting algorithm. 
// An array is given in R14 and R15, where R14 contains the start address of the 
// array, and R15 contains the length of the array. 
// You are not allowed to change R14, R15.
// The program should sort the array in-place and in descending order - 
// the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that 
// R14 + R15 <= 16383. 
// No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is 
// at most C*O(N^2), like bubble-sort. 

// Put your code here.

	@i
	M=0
	@j
	M=0
(LOOP)
	@i
	D=M
	@R15
	D=M-D
	@END
	D;JLE
	@i
	D=M
	@R14
	A=M+D #A[i]
	D=A
	@ad1
	M=D
	A=D
	D=M
	@val1
	M=D
(INLOOP)
	@j
	M=M+1
	D=M
	//CHECK J
	@R15
	D=M-D
	@NEXTJ
	D;JLE

	@j
	D=M
	@R14
	A=M+D #A[J]
	D=A
	@ad2
	M=D
	A=D
	D=M
	@val2
	M=D
	D=M
	@val1
	D=M-D
	@SWAP
	D;JLT
	@INLOOP
	0;JMP

(SWAP)
	@val2
	D=M
	@ad1
	A=M
	M=D
	@val1
	D=M
	@ad2
	A=M
	M=D

	@val2
	D=M
	@val1
	M=D
	@INLOOP
	0;JMP
(NEXTJ)
	@i
	M=M+1
	D=M
	@j
	M=D
	@LOOP
	0;JMP

(END)
	@END
	0;JMP

