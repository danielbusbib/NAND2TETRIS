"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter

COMMANDS = {"C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL", "C_ARITHMETIC"}

counter_lst = [0, 0]
def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
        "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
    """
    # Your code goes here!
    # Note: you can get the input file's name using:
    # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    p = Parser(input_file)
    cd = CodeWriter(output_file)
    cd.set_file_name(os.path.basename(input_file.name)[:-3])
    cd.write_init()
    while p.has_more_commands():
        # output_file.write("//" + p.command_type() + "\n")
        # print(p.cur_line, "\n")
        p.advance()
        command = p.command_type()
        if p.cur_line:
            output_file.write('//' + p.cur_line + '\n')
        if command not in COMMANDS:
            continue
        p.cur_command_type = command
        if command == "C_RETURN":
            cd.write_return()
            continue
        arg1 = p.arg1()
        if command == "C_ARITHMETIC":
            cd.write_arithmetic(arg1)
            continue
        if command == "C_GOTO":
            cd.write_goto(arg1)
            continue
        if command == "C_LABEL":
            cd.write_label(arg1)
            continue
        if command == "C_IF":
            cd.write_if(arg1)
            continue
        arg2 = p.arg2()
        if command == "C_PUSH" or command == "C_POP":
            cd.write_push_pop(command, arg1, arg2)
            continue
        if command == "C_CALL":
            cd.write_call(arg1, arg2)
            continue
        if command == "C_FUNCTION":
            cd.write_function(arg1, arg2)
            continue
        output_file.write('\n')


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file)
