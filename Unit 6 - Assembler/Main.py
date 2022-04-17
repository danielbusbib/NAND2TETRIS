"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code

SHIFT_COMP = ["D<<", "A<<", "M<<", "D>>", "A>>", "M>>"]


def check_num(sym):
    for s in sym:
        if s not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return False
    return True


def bin_num_16(j):
    a = ["0"] * 16
    n = 1
    for i in range(14, -1, -1):
        if j // (2 ** i) > 0:
            a[n] = "1"
            j = j - (2 ** i)
        n += 1
    return ''.join(a)


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # out = open(output_file, "w")

    # Your code goes here!
    #
    # You should use the two-pass implementation suggested in the book:
    #
    # *Initialization*
    # Initialize the symbol table with all the predefined symbols and their
    # pre-allocated RAM addresses, according to section 6.2.3 of the book.
    #
    s = SymbolTable()

    # *First Pass*
    # Go through the entire assembly program, line by line, and build the symbol
    # table without generating any code. As you march through the program lines,
    # keep a running number recording the ROM address into which the current
    # command will be eventually loaded.
    # This number starts at 0 and is incremented by 1 whenever a C-instruction
    # or an A-instruction is encountered, but does not change when a label
    # pseudo-command or a comment is encountered. Each time a pseudo-command
    # (Xxx) is encountered, add a new entry to the symbol table, associating
    # Xxx with the ROM address that will eventually store the next command in
    # the program.
    # This pass results in entering all the programs labels along with their
    # ROM addresses into the symbol table.
    # The programs variables are handled in the second pass.
    #
    p = Parser(input_file)
    i = 0
    while p.has_more_commands():
        p.advance()
        if p.command_type() == "NONE_COMMAND":
            continue

        if p.command_type() == "L_COMMAND":
            s.add_entry(p.symbol(), i)
            continue
        i += 1
    # *Second Pass*
    # Now go again through the entire program, and parse each line.
    # Each time a symbolic A-instruction is encountered, namely, @Xxx where Xxx
    # is a symbol and not a number, look up Xxx in the symbol table.
    # If the symbol is found in the table, replace it with its numeric meaning
    # and complete the commands translation.
    # If the symbol is not found in the table, then it must represent a new
    # variable. To handle it, add the pair (Xxx,n) to the symbol table, where n
    # is the next available RAM address, and complete the commands translation.
    # The allocated RAM addresses are consecutive numbers, starting at address
    # 16 (just after the addresses allocated to the predefined symbols).
    # After the command is translated, write the translation to the output file.
    p.reset()
    c = Code()
    j = 16

    while p.has_more_commands():
        p.advance()
        if p.command_type() == "A_COMMAND":
            sym = p.symbol()
            if sym in s.PRE_DEFINED_SYMBOLS:
                a_binary = bin_num_16(int(s.PRE_DEFINED_SYMBOLS[sym]))
                output_file.write(a_binary + "\n")
                continue
            if sym in s.symbols:
                a_binary = bin_num_16(int(s.symbols[sym]))
                output_file.write(a_binary + "\n")
                continue
            if not check_num(sym):
                s.add_entry(sym, j)
                a_binary = bin_num_16(j)
                j += 1
                output_file.write(a_binary + "\n")
                continue
            if check_num(sym):
                a_binary = bin_num_16(int(sym))
                output_file.write(a_binary + "\n")
            continue
        if p.command_type() == "L_COMMAND" or p.command_type() == "NONE_COMMAND":
            continue
        comp = c.comp(p.comp())
        dest = c.dest(p.dest())
        jump = c.jump(p.jump())
        if comp in SHIFT_COMP:
            output_file.write("101" + comp + dest + jump + '\n')
            continue
        output_file.write("111" + comp + dest + jump + '\n')
        # if not p.has_more_commands():
        #     out.write("111" + comp + dest + jump)
        # else:
        #     out.write("1" + comp + dest + jump + "\n")

    # out.close()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
