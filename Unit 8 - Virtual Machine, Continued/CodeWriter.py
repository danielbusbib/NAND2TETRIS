"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import typing

NEXT_LINE = '\n'


class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    FUNC_C = 0
    LABEL_C = 0

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        self.out_file = output_stream
        self.file_name = ""
        self.counter_label = CodeWriter.LABEL_C
        self.compare_op = {"eq": "EQ", "gt": "GT", "lt": "LT"}
        self.func_counter = CodeWriter.FUNC_C

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        self.file_name = filename

    def write_init(self):
        self.out_file.write("@256" + NEXT_LINE)
        self.out_file.write("D=A" + NEXT_LINE)
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)
        self.write_call("Sys.init", 0)
        return

    def write_label(self, label: str) -> None:
        self.out_file.write("(" + label + ")" + NEXT_LINE)

    def write_goto(self, label: str) -> None:
        self.out_file.write("@" + label + NEXT_LINE)
        self.out_file.write("0;JMP" + NEXT_LINE)

    def write_if(self, label: str) -> None:
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("M=M-1" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@" + label + NEXT_LINE)

        self.out_file.write("D;JNE" + NEXT_LINE)

    def __push_sp_call(self):
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("M=M+1" + NEXT_LINE)

    def write_call(self, function_name: str, num_args: int) -> None:
        self.func_counter += 1
        CodeWriter.FUNC_C += 1
        self.out_file.write("@RETURN" + str(self.func_counter) + NEXT_LINE)
        self.out_file.write("D=A" + NEXT_LINE)
        # self.out_file.write("@SP" + NEXT_LINE)
        # self.out_file.write("D=A-D" + NEXT_LINE)
        self.__push_sp_call()  # PUSH RETURN ADDRESS

        self.out_file.write("@LCL" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.__push_sp_call()  # PUSH LCL

        self.out_file.write("@ARG" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.__push_sp_call()  # PUSH ARG

        self.out_file.write("@THIS" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.__push_sp_call()  # PUSH THIS

        self.out_file.write("@THAT" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.__push_sp_call()  # PUSH THAT

        # ARG = SP - numArgs - 5
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@" + str((int(num_args) + 5)) + NEXT_LINE)
        self.out_file.write("D=D-A" + NEXT_LINE)
        self.out_file.write("@ARG" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)

        # LCL = SP
        self.out_file.write("@LCL" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)

        # GOTO F
        self.write_goto(function_name)
        # (return-address)
        self.write_label("RETURN" + str(self.func_counter))
        return

    def write_return(self) -> None:
        # FRAME=LCL
        self.out_file.write("@LCL" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@R13" + NEXT_LINE)  # FRAME
        self.out_file.write("M=D" + NEXT_LINE)
        # RET=*(FRAME-5)
        self.out_file.write("@5" + NEXT_LINE)
        self.out_file.write("D=A" + NEXT_LINE)
        self.out_file.write("@R13" + NEXT_LINE)
        self.out_file.write("D=M-D" + NEXT_LINE)
        self.out_file.write("A=D" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@R14" + NEXT_LINE)  # RET
        self.out_file.write("M=D" + NEXT_LINE)
        # *ARG=pop()
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("D=A" + NEXT_LINE)
        self.out_file.write("@ARG" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("D=A+D" + NEXT_LINE)
        self.out_file.write("@R15" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("M=M-1" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@R15" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)

        # @SP = ARG+1
        self.out_file.write("@ARG" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("M=D+1" + NEXT_LINE)

        # THAT =*(FRAME-1)
        self.out_file.write("@R13" + NEXT_LINE)
        self.out_file.write("M=M-1" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@THAT" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)

        # THIS =*(FRAME-2)
        self.out_file.write("@R13" + NEXT_LINE)
        self.out_file.write("M=M-1" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@THIS" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)

        # ARG =*(FRAME-3)
        self.out_file.write("@R13" + NEXT_LINE)
        self.out_file.write("M=M-1" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@ARG" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)

        # LCL =*(FRAME-4)
        self.out_file.write("@R13" + NEXT_LINE)
        self.out_file.write("M=M-1" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("D=M" + NEXT_LINE)
        self.out_file.write("@LCL" + NEXT_LINE)
        self.out_file.write("M=D" + NEXT_LINE)

        # goto RET
        self.out_file.write("@R14" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("0;JMP" + NEXT_LINE)
        return

    def push_function_arg(self, ) -> None:
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("A=M" + NEXT_LINE)
        self.out_file.write("M=0" + NEXT_LINE)
        self.out_file.write("@SP" + NEXT_LINE)
        self.out_file.write("M=M+1" + NEXT_LINE)

    def write_function(self, function_name: str, num_args: int) -> None:
        # self.write_label(function_name)
        self.out_file.write("(" + function_name + ")" + NEXT_LINE)

        for k in range(num_args):  # repeat k times: PUSH 0
            self.push_function_arg()

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        if command == "shiftleft":
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M-1" + NEXT_LINE)
            self.out_file.write("M=M<<" + NEXT_LINE)
        elif command == "shiftright":
            self.out_file.write("@SP" + NEXT_LINE)
            self.out_file.write("A=M-1" + NEXT_LINE)
            self.out_file.write("M=M>>" + NEXT_LINE)
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
            CodeWriter.LABEL_C += 1

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
                self.out_file.write("@" + str(index) + NEXT_LINE)
                self.out_file.write("D=A" + NEXT_LINE)
                self.out_file.write("@5" + NEXT_LINE)
                self.out_file.write("A=A+D" + NEXT_LINE)
                self.out_file.write("D=A" + NEXT_LINE)
                self.out_file.write("@R13" + NEXT_LINE)
                self.out_file.write("M=D" + NEXT_LINE)
                self.out_file.write("@SP" + NEXT_LINE)
                self.out_file.write("M=M-1" + NEXT_LINE)
                self.out_file.write("A=M" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
                self.out_file.write("M=0" + NEXT_LINE)
                self.out_file.write("@R13" + NEXT_LINE)
                self.out_file.write("A=M" + NEXT_LINE)
                self.out_file.write("M=D" + NEXT_LINE)
                self.out_file.write("@R13" + NEXT_LINE)
                self.out_file.write("M=0" + NEXT_LINE)

                return
            if segment == "pointer":
                self.out_file.write("@SP" + NEXT_LINE)
                self.out_file.write("AM=M-1" + NEXT_LINE)
                self.out_file.write("D=M" + NEXT_LINE)
                self.out_file.write("M=0" + NEXT_LINE)
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
