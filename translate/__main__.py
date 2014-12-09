# -*- coding: utf-8 -*-
"""
Copyright: Sang Han 2014

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os

from sys import exit
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from functools import partial

from .__version__ import __version__, __build__
from .translator import translator
from .coroutines import chunk, spool, source, set_task
from .languages import print_table, translation_table

__all__ = []

class TermWidthHelpFormatter(RawDescriptionHelpFormatter):

    def __init__(self,  *args, **kwargs):
        term = os.get_terminal_size()
        width = term.columns
        super(TermWidthHelpFormatter, self).__init__(
            width=width, max_help_position=35, *args, **kwargs
        )

def command_line():

    description = 'A simple translation command line utility'
    version     = ' '.join([__version__, __build__])
    table       = sorted(translation_table('en').keys())

    codes = ArgumentParser(add_help=False)
    codes.add_argument(
        '-l', '--list',
        nargs='?',
        default=False,
        const='en',
        metavar='code',
        dest='code',
        help=' '.join(
            [
                'Enumerate the name of country and language code pair.',
                'Optionally specify output language',
            ])
        )

    # Preparse Language Code Flag
    language,_ = codes.parse_known_args()
    if language.code:
        print_table(language.code)
        exit(0)

    # Main Parser
    parser = ArgumentParser(
        parents=[codes],
        prog='translate',
        description=description,
        formatter_class=TermWidthHelpFormatter,
    )
    parser.add_argument(
        '--translit',
        action='store_true',
        help='Print out the transliteration of the text',
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version="%s v%s" % ('translate', version)
    )
    parser.add_argument(
        'source',
        nargs='?',
        default=None,
        choices=[None]+table,
        help='Source language code',
        metavar='source',
    )
    parser.add_argument(
        'dest',
        type=str,
        choices=table,
        help='Destination language code',
        metavar='target',
    )

    return parser.parse_args()


def main():
    '''
    Main Entry point for translator and argument parser
    '''
    args = command_line()

    translate = partial(translator, version=' '.join([__version__, __build__]))

    source(spool(chunk(set_task(translate, args.source, args.dest))))

    return

if __name__ == '__main__':
    exit(main())
