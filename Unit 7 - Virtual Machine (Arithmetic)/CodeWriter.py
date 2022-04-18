"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

NEXT_LINE = '\n'


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        self.out_file = output_stream
        self.file_name = ""
        self.counter_label = 1
        self.compare_op = {"eq": "EQ", "gt": "GT", "lt": "LT"}

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        self.file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        self.counter_label += 1
        # Your code goes here!
        if command == "shiftleft":
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M-1" + NEXT_LINE)
            self.out_file.write("M<<" + NEXT_LINE)
        elif command == "shiftright":
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M-1" + NEXT_LINE)
            self.out_file.write("M>>" + NEXT_LINE)
        elif command == "add":
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("A=A-1" + NEXT_LINE)
            self.out_file.write("A=A-1" + NEXT_LINE)
            self.out_file.write("D=M" + NEXT_LINE)
            self.out_file.write("A=A+1" + NEXT_LINE)
            self.out_file.write("D=D+M" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("M=M-1" + NEXT_LINE)
            self.out_file.write("M=M-1" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("M=D" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("M=M+1" + NEXT_LINE)

        elif command == "sub":
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("A=A-1" + NEXT_LINE)
            self.out_file.write("A=A-1" + NEXT_LINE)
            self.out_file.write("D=M" + NEXT_LINE)
            self.out_file.write("A=A+1" + NEXT_LINE)
            self.out_file.write("D=D-M" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("M=M-1" + NEXT_LINE)
            self.out_file.write("M=M-1" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("M=D" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("M=M+1" + NEXT_LINE)

        elif command == "neg":
            self.out_file.write("D=0" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M-1" + NEXT_LINE)
            self.out_file.write("M=D-M" + NEXT_LINE)
        elif command in self.compare_op:
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("M=M-1" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("D=M" + NEXT_LINE)
            self.out_file.write("@R13" + NEXT_LINE)
            self.out_file.write("M=D" + NEXT_LINE)
            self.out_file.write("@IFBNEG" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("D;JLT" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("M=M-1" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("D=M" + NEXT_LINE)
            self.out_file.write("@BpAn" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("D;JLT" + NEXT_LINE)
            self.out_file.write("@R13" + NEXT_LINE)
            self.out_file.write("D=D-M" + NEXT_LINE)
            self.out_file.write("@ST" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("0;JMP" + NEXT_LINE)
            self.out_file.write("(IFBNEG" + str(self.counter_label) + ")" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("M=M-1" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("D=M" + NEXT_LINE)
            self.out_file.write("@BnAp" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("D;JGT" + NEXT_LINE)
            self.out_file.write("@R13" + NEXT_LINE)
            self.out_file.write("D=D-M" + NEXT_LINE)
            self.out_file.write("A=D" + NEXT_LINE)
            self.out_file.write("@ST" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("0;JMP" + NEXT_LINE)

            self.out_file.write("(BpAn" + str(self.counter_label) + ")" + NEXT_LINE)
            self.out_file.write("D=-1" + NEXT_LINE)
            self.out_file.write("@ST" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("0;JMP" + NEXT_LINE)
            self.out_file.write("(BnAp" + str(self.counter_label) + ")" + NEXT_LINE)
            self.out_file.write("D=1" + NEXT_LINE)
            self.out_file.write("@ST" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("0;JMP" + NEXT_LINE)

            self.out_file.write("(ST" + str(self.counter_label) + ")" + NEXT_LINE)
            self.out_file.write("@TRUE" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("D;J" + self.compare_op[command] + NEXT_LINE)
            self.out_file.write("D=0" + NEXT_LINE)
            self.out_file.write("@SAF" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("0;JMP" + NEXT_LINE)
            self.out_file.write("(TRUE" + str(self.counter_label) + ")" + NEXT_LINE)
            self.out_file.write("D=-1" + NEXT_LINE)
            self.out_file.write("@SAF" + str(self.counter_label) + NEXT_LINE)
            self.out_file.write("0;JMP" + NEXT_LINE)
            self.out_file.write("(SAF" + str(self.counter_label) + ")" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("M=D" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("M=M+1" + NEXT_LINE)

            self.counter_label += 1
        elif command == "and":
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("AM=M-1" + NEXT_LINE)
            self.out_file.write("D=M" + NEXT_LINE)
            self.out_file.write("A=A-1" + NEXT_LINE)
            self.out_file.write("M=D&M" + NEXT_LINE)

        elif command == "or":
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("AM=M-1" + NEXT_LINE)
            self.out_file.write("D=M" + NEXT_LINE)
            self.out_file.write("A=A-1" + NEXT_LINE)
            self.out_file.write("M=D|M" + NEXT_LINE)

        elif command == "not":
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M-1" + NEXT_LINE)
            self.out_file.write("M=!M" + NEXT_LINE)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        d = ""
        write = ""
        # print(segment, " - ", index)
        if command == "C_PUSH":
            if segment == "temp":
                self.out_file.write("@R11" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
            elif segment == "pointer":
                self.out_file.write("@" + str(3 + index) + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
            elif segment == "constant":
                self.out_file.write("@" + str(index) + NEXT_LINE)
                self.out_file.write("D=A" + "\n")
            elif segment == "static":
                self.out_file.write("@" + self.file_name + "." + str(index) + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
            elif segment == "argument":
                self.out_file.write("@" + str(index) + NEXT_LINE)
                self.out_file.write("D=A" + NEXT_LINE)
                self.out_file.write("@ARG" + NEXT_LINE)
                self.out_file.write("A=M+D" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
            elif segment == "this":
                self.out_file.write("@" + str(index) + NEXT_LINE)
                self.out_file.write("D=A" + NEXT_LINE)
                self.out_file.write("@THIS" + NEXT_LINE)
                self.out_file.write("A=M+D" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
            elif segment == "that":
                self.out_file.write("@" + str(index) + NEXT_LINE)
                self.out_file.write("D=A" + NEXT_LINE)
                self.out_file.write("@THAT" + NEXT_LINE)
                self.out_file.write("A=M+D" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
            elif segment == "local":
                self.out_file.write("@" + str(index) + NEXT_LINE)
                self.out_file.write("D=A" + NEXT_LINE)
                self.out_file.write("@LCL" + NEXT_LINE)
                self.out_file.write("A=M+D" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("M=D" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("M=M+1" + NEXT_LINE)

        elif command == "C_POP":
            if segment == "static":
                self.out_file.write("@SP" + NEXT_LINE)
                self.out_file.write("M=M-1" + NEXT_LINE)
                self.out_file.write("A=M" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
                self.out_file.write("@" + self.file_name + "." + str(index) + NEXT_LINE)
                self.out_file.write("M=D" + NEXT_LINE)
                return
            if segment == "temp":
                self.out_file.write("@SP" + NEXT_LINE)
                self.out_file.write("AM=M-1" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
                self.out_file.write("@R11" + NEXT_LINE)
                self.out_file.write("M=D" + NEXT_LINE)
                return
            if segment == "pointer":
                self.out_file.write("@SP" + NEXT_LINE)
                self.out_file.write("AM=M-1" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
                self.out_file.write("@" + str(3 + index) + NEXT_LINE)
                self.out_file.write("M=D" + NEXT_LINE)
                return
            if segment == "that" or segment == "this":
                self.out_file.write("@" + str(index) + NEXT_LINE)
                self.out_file.write("D=A" + NEXT_LINE)
                self.out_file.write("@" + segment.upper() + NEXT_LINE)
                self.out_file.write("D=M+D" + NEXT_LINE)
                self.out_file.write("@R13" + NEXT_LINE)
                self.out_file.write("M=D" + NEXT_LINE)
                self.out_file.write("@SP" + NEXT_LINE)
                self.out_file.write("AM=M-1" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
                self.out_file.write("@R13" + NEXT_LINE)
                self.out_file.write("A=M" + NEXT_LINE)
                self.out_file.write("M=D" + NEXT_LINE)
                return
            self.out_file.write("@" + str(index) + NEXT_LINE)
            self.out_file.write("D=A" + NEXT_LINE)
            if segment == "local":
                d = "LCL"
            elif segment == "argument":
                d = "ARG"
            self.out_file.write("@" + d + NEXT_LINE)
            self.out_file.write("D=M+D" + NEXT_LINE)
            self.out_file.write("@R13" + NEXT_LINE)
            self.out_file.write("M=D" + NEXT_LINE)
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("AM=M-1" + NEXT_LINE)
            self.out_file.write("D=M" + NEXT_LINE)
            self.out_file.write("@R13" + NEXT_LINE)
            self.out_file.write("A=M" + NEXT_LINE)
            self.out_file.write("M=D" + NEXT_LINE)
            return

    def close(self) -> None:
        """Closes the output file."""
        # Your code goes here!
        self.out_file.close()
