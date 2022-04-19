"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """
    set_commands = {"add", "sub", "neg", "not", "or", "and", "eq", "gt", "lt", "shiftleft", "shiftright"}

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_file.read().splitlines()
        self.line = 0
        self.cur_command_type = ""
        self.cur_line = ""
        self.command_type_cur_line = ""
        self.space_index = -1
        self.data = input_file.read().splitlines()

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        if self.line >= len(self.data):
            return False
        return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        self.cur_line = self.data[self.line]
        self.line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        if "//" in self.cur_line:
            self.cur_line = self.cur_line[:self.cur_line.find("//")]
        if "return" in self.cur_line:
            return "C_RETURN"
        if self.cur_line in Parser.set_commands:
            return "C_ARITHMETIC"
        if ' ' not in self.cur_line:
            return "C_" + (self.cur_line.upper())
        self.space_index = self.cur_line.find(' ')

        if self.cur_line.find('-') != -1:
            return "C_IF"
        if self.space_index != -1:
            if self.cur_line[:self.space_index] in Parser.set_commands:
                return "C_ARITHMETIC"
            command_type = self.cur_line[:self.space_index]
        else:
            command_type = self.cur_line[:]
        return "C_" + command_type.upper()

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        if self.cur_command_type == "C_ARITHMETIC":
            if " " in self.cur_line:
                return self.cur_line[:self.cur_line.find(' ')]
            return self.cur_line
        i = self.space_index
        prev = i
        while i + 1 < len(self.cur_line) and self.cur_line[i + 1] != ' ':
            i += 1

        self.space_index = i + 1
        return self.cur_line[prev + 1:self.space_index]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        stringy = ""
        i = self.space_index
        if len(self.cur_line) <= i:
            return int()
        while i + 1 < len(self.cur_line) and self.cur_line[i + 1] != " ":
            stringy += self.cur_line[i + 1]
            i += 1

        return int(stringy)
