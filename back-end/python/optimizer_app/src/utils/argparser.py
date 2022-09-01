import argparse

def get_parser():
    parser = argparse.ArgumentParser(description = 'Um programa de exemplo.')

    parser.add_argument('--frase', action = 'store', dest = 'frase',
                           default = 'Hello, world!', required = False,
                           help = 'A frase que deseja imprimir n vezes.')