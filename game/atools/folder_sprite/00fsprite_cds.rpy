# MIT License

# Copyright (c) 2023 Melo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

python early:

    # Função que faz o processamento do CDS 'fsprite'
    def execute_fsprite(parsed_object):
        who, group, value = parsed_object
        if hasattr(fsc(who), group):
            setattr(fsc(who), group, value)
        else:
            raise Exception("Group "+group+" does not exists!")

    # Função de análise para o CDS 'fsprite'
    def parse_fsprite(lexer):
        who = lexer.image_name_component()

        group = lexer.simple_expression()

        if not group:
            raise Exception("Expected group")

        value = lexer.simple_expression()

        if not value:
            raise Exception("Expected value")
        
        rest = lexer.rest()

        if rest:
            raise Exception("Too many arguments")

        return (who, group, value)

    # Registrando o CDS 'fsprite'
    renpy.register_statement(
        name="fschange",
        parse=parse_fsprite,
        execute=execute_fsprite,
    )
