"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer

NEXT_LINE = '\n'


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    # add global sets
    OPS = {'+', '-', '*', '/', '&', '<', '>', '|', '&', '=', "&lt;", "&gt;", "&amp;"}

    def __init__(self, input_stream: typing.TextIO,
                 output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        self.out_file = output_stream
        self.in_file = input_stream
        self.tokenizer = JackTokenizer(input_stream)
        self.cur_indent = ""

    def __add_indent(self):
        self.cur_indent += "    "

    def __rm_indent(self):
        self.cur_indent = self.cur_indent[:-4]

    def __write_line(self, token, val):
        self.out_file.write("<" + token + "> " + val + " </" + token + ">" + NEXT_LINE)

    def write_start_token(self, token_type):
        self.out_file.write("<" + token_type + ">" + NEXT_LINE)

    def write_end_token(self, token_type):
        self.out_file.write("</" + token_type + ">" + NEXT_LINE)

    def __advance_and_write(self):
        self.tokenizer.advance()
        # print(self.tokenizer.token_type().lower(), self.tokenizer.keyword())
        tok_type = self.tokenizer.token_type()
        if tok_type == "INT_CONST":
            tok_type = "integerConstant"
        elif tok_type == "STRING_CONST":
            self.__write_line("stringConstant", self.tokenizer.keyword()[1:-1])
            return
        elif tok_type == "SYMBOL":
            self.__write_line("symbol", self.tokenizer.symbol())
            return
        else:
            tok_type = tok_type.lower()
        self.__write_line(tok_type, self.tokenizer.keyword())

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.write_start_token("class")
        self.__advance_and_write()  # class
        self.__advance_and_write()  # class name
        self.__advance_and_write()  # {
        # maybe change to WHILE !
        c = self.tokenizer.peek()
        print(self.tokenizer.tokens_from_line)
        print(c)
        while c in {"static", "field"}:
            self.compile_class_var_dec()
            c = self.tokenizer.peek()
        while c in {"constructor", "function", "method"}:
            self.compile_subroutine()
            c = self.tokenizer.peek()
        self.__advance_and_write()  # }
        self.write_end_token("class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.write_start_token("classVarDec")
        self.__advance_and_write()  # static/field
        self.__advance_and_write()  # type
        self.__advance_and_write()  # varName
        while self.tokenizer.peek() == ",":
            self.__advance_and_write()  # ,
            self.__advance_and_write()  # varName
        self.__advance_and_write()  # ;
        self.write_end_token("classVarDec")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        # Your code goes here!
        self.write_start_token("subroutineDec")
        self.__advance_and_write()  # constructor/function/method
        self.__advance_and_write()  # void/type*
        self.__advance_and_write()  # subRoutineName
        self.__advance_and_write()  # (
        self.compile_parameter_list()  # parameter list
        self.__advance_and_write()  # )
        # start:
        self.write_start_token("subroutineBody")
        self.__advance_and_write()  # {
        while self.tokenizer.peek() == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.__advance_and_write()  # }
        self.write_end_token("subroutineBody")
        self.write_end_token("subroutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.write_start_token("parameterList")
        next_tok = self.tokenizer.peek()
        if next_tok == ")":
            self.write_end_token("parameterList")
            return
        self.__advance_and_write()  # param type
        self.__advance_and_write()  # name

        while self.tokenizer.peek() == ',':
            self.__advance_and_write()  # ,
            self.__advance_and_write()  # param type
            self.__advance_and_write()  # name
        self.write_end_token("parameterList")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        self.write_start_token("varDec")
        self.__advance_and_write()  # var
        self.__advance_and_write()  # type
        self.__advance_and_write()  # varName
        while self.tokenizer.peek() == ",":
            self.__advance_and_write()  # ,
            self.__advance_and_write()  # varName
        self.__advance_and_write()  # ;
        self.write_end_token("varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        self.write_start_token("statements")
        print(self.tokenizer.tokens_from_line)
        print(self.tokenizer.c_token)
        p = self.tokenizer.peek()
        print(p)
        while p in {"let", "if", "while", "do", "return"}:
            if p == "let":
                self.compile_let()
            elif p == "if":
                self.compile_if()
            elif p == "while":
                self.compile_while()
            elif p == "do":
                self.compile_do()
            elif p == "return":
                self.compile_return()
            p = self.tokenizer.peek()
        self.write_end_token("statements")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.write_start_token("doStatement")
        self.__advance_and_write()  # do
        self.__advance_and_write()  #
        if self.tokenizer.peek() == ".":
            self.__advance_and_write()  # .
            self.__advance_and_write()  # subr name
        self.__advance_and_write()  # (
        self.compile_expression_list()
        self.__advance_and_write()  # )
        self.__advance_and_write()  # ;
        self.write_end_token("doStatement")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.write_start_token("letStatement")
        self.__advance_and_write()  # let
        self.__advance_and_write()  # varName
        p = self.tokenizer.peek()
        if p == "[":
            self.__advance_and_write()  # [
            self.compile_expression()  # expression
            self.__advance_and_write()  # ]
        self.__advance_and_write()  # =
        self.compile_expression()  # expression
        self.__advance_and_write()  # ;
        self.write_end_token("letStatement")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.write_start_token("whileStatement")
        self.__advance_and_write()  # while
        self.__advance_and_write()  # (
        self.compile_expression()
        self.__advance_and_write()  # )
        self.__advance_and_write()  # {
        self.compile_statements()
        self.__advance_and_write()  # }
        self.write_end_token("whileStatement")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.write_start_token("returnStatement")
        self.__advance_and_write()  # return
        if self.tokenizer.peek() != ";":
            self.compile_expression()
        self.__advance_and_write()  # ;
        self.write_end_token("returnStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.write_start_token("ifStatement")
        self.__advance_and_write()  # if
        self.__advance_and_write()  # (
        self.compile_expression()
        self.__advance_and_write()  # )
        self.__advance_and_write()  # {
        self.compile_statements()
        self.__advance_and_write()  # }

        if self.tokenizer.peek() == "else":
            self.__advance_and_write()  # else
            self.__advance_and_write()  # {
            self.compile_statements()
            self.__advance_and_write()  # }
        self.write_end_token("ifStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.write_start_token("expression")
        # complete
        self.compile_term()
        while self.tokenizer.peek() in CompilationEngine.OPS:
            self.__advance_and_write()
            self.compile_term()

        self.write_end_token("expression")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        self.write_start_token("term")
        if self.tokenizer.peek_token_type(self.tokenizer.peek()) in {"INT_CONST", "STRING_CONST", "KEYWORD"}:
            self.__advance_and_write()
            self.write_end_token("term")
            return
        # complete
        tok = self.tokenizer.peek()
        print('tok:', tok)
        toke_type = self.tokenizer.peek_token_type(tok)
        if toke_type == "IDENTIFIER":
            self.__advance_and_write()
            if self.tokenizer.peek() == "[":
                self.__advance_and_write()  # [
                self.compile_expression()  # expression
                self.__advance_and_write()  # ]

            if self.tokenizer.peek() == ".":
                self.__advance_and_write()  # .
                self.__advance_and_write()  # name
                self.__advance_and_write()  # (
                self.compile_expression_list()
                self.__advance_and_write()  # )

            if self.tokenizer.peek() == "(":
                self.__advance_and_write()  # (
                self.compile_expression_list()
                self.__advance_and_write()  # )

        elif self.tokenizer.peek() == "(":
            self.__advance_and_write()  # (
            self.compile_expression()
            self.__advance_and_write()  # )

        elif self.tokenizer.peek() in {'-', '~', '^', "#"}:
            self.__advance_and_write()
            self.compile_term()

        self.write_end_token("term")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.write_start_token("expressionList")
        # complete
        if self.tokenizer.peek() == ")":
            self.write_end_token("expressionList")
            return
        self.compile_expression()

        while self.tokenizer.peek() == ',':
            self.__advance_and_write()  # ,
            self.compile_expression()
        self.write_end_token("expressionList")
