from colorama import init, Back, Style    # colors
init()


def get_repeat_product():
    rep = input(f'\ndeseja repetir? (sim/não): ').strip().lower()
    while rep not in ('sim' , 'não'):
        rep = input(f'{Back.YELLOW}por favor, insira uma opção valida (sim/não): {Style.RESET_ALL}').strip().lower()
    return rep