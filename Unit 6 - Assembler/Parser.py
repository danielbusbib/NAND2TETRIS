"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads and assembly language
    command, parses it, and provides convenient access to the commands
    components (fields and symbols). In addition, removes all white space and
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_file.read().splitlines()
        self.line = 0
        self.cur_line = ""

        self.data = input_file.read().splitlines()
    def reset(self):
        self.line = 0
        self.cur_line = ""
    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        if self.line == len(self.data):
            return False
        return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        # if not self.has_more_commands():
        #     return
        self.cur_line = self.data[self.line]
        self.line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        temp = ""
        for s in self.cur_line:
            if s == ' ':
                continue
            if s == "/":
                break
            temp += s

        if not temp:
            return "NONE_COMMAND"
        self.cur_line = temp
        self.type = "C"
        if temp[0] == "@":
            self.type = "A"
            return "A_COMMAND"
        if temp[0] == "(":
            self.type = "L"
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or
            "L_COMMAND".
        """
        # Your code goes here!
        if self.type == "A":
            return self.cur_line[1:]

        return self.cur_line[1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if "=" not in self.cur_line:
            return "null"
        if self.cur_line[2] == "=":
            return self.cur_line[0:2]
        return self.cur_line[0]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if "=" in self.cur_line:
            if self.cur_line[2] == "=":
                return self.cur_line[3:]
            return self.cur_line[2:]
        return self.cur_line[0]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if ";" not in self.cur_line:
            return "null"
        return self.cur_line[2:]
