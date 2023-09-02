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
