// This file is part of the materials accompanying the book
// "The Elements of Computing Systems" by Nisan and Schocken, 
// MIT Press 2004. Book site: http://www.idc.ac.il/tecs
// File name: projects/05/CPU.tst.   Version: beta 1.4.

load CPU.hdl,
output-file CPU2.out,
compare-to CPU2.cmp,
output-list time%S0.4.0 inM%D0.6.0 instruction%B0.16.0 reset%B2.1.2 newOutM%D1.6.0 writeM%B3.1.3 addressM%D0.5.0 pc%D0.5.0 DRegister[]%D1.6.1;


set instruction %B0000000000001010,//@10
tick, output, tock, output;
set instruction %B1010110000010000, //D=shift left A
tick, output, tock, output;
set instruction %B0000000000011101, // @29
tick, output, tock, output;
set instruction %B1110110000010000, // D=A
tick, output, tock, output;
set instruction %B1010000000110000, //AD=shift left A
tick, output, tock, output;
set instruction %B1110110111010000, // D=A+1
tick, output, tock, output;
set instruction %B0000001111101000, // @1000
tick, output, tock, output;
set instruction %B1100110000010000, // D=A;
tick, output, tock, output;
set instruction %B1010011111011000, //MD=shift left D+1
tick, output, tock, output;
set instruction %B1011001100010000, //D=shift left D
tick, output, tock, output;
set instruction %B0000000000000001, //@1
tick, output, tock, output;
set instruction %B1110110000010000, //D=A
tick, output, tock, output;
set instruction %B1011001100010001, //D = shiftLeft D;jgt
tick, output, tock, output;


