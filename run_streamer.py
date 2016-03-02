#!/usr/bin/env python

import jinja2
import subprocess
import tempfile
import re

DEFAULT_SETTINGS = dict(output_filename='output_filename.out',
                        replace_statements=[{'bend': 129, 'bstart': 106}],
                        std_prof=1,
                        rectitle='Test everything out',
                        year=2015,
                        month=2,
                        day=20,
                        hour=5.5,
                        zen=10,
                        icthk=3,
                        nclouds=0,
                        ntype=1,
                        cldfrac=1.0,
                        cldtemp=-999,
                        cldtop=4.0,
                        cldthick=0.5,
                        cldtau=1.0,
                        nphases=1,
                        cldphase1=0,
                        cldrel=10,
                        cldwcl=0.1,
                        frwv=1.0,
                        fro3=1.0,
                        frrhhz=1.0,
                        frco2=1.0,
                        fro2=1.0,
                        frwv2=1.0
                        )

TROPICAL = DEFAULT_SETTINGS.copy()
TROPICAL.update(
    dict(std_prof=1, nclouds=0, zen=71)
)

ARCTIC = DEFAULT_SETTINGS.copy()
ARCTIC.update(
    dict(std_prof=7, nclouds=0, zen=84)
)

SW = dict(replace_statements=[{'bstart': 106, 'bend': 129}])
LW = dict(replace_statements=[{'bstart': 1, 'bend': 105}])
COMBINED = dict(replace_statements=[{'bstart': 1, 'bend': 129}])

SPECTRAL = dict(replace_statements=[{'bstart': x, 'bend': x} for x in range(1, 130)])

SW_WL_RANGE = [4.0, .28]
LW_WL_RANGE = [500.0, 4.03]
COMBINED_WL_RANGE = [500.0, 0.28]


def main(args):
    path_to_streamer = './streamer'
    path_to_template = './template.inp'

    run_and_parse(path_to_streamer, path_to_template)


def run_and_parse(path_to_streamer, path_to_template, **settings):
    # Create a file to hold the input data
    # After it exits the file will be deleted immediately
    with tempfile.NamedTemporaryFile('w+', delete=True) as input_fp:
        # Read the template file and create jinja2 template
        with open(path_to_template) as template_fp:
            template = jinja2.Template(template_fp.read())

        # Write the rendered template to the temporary input file
        input_fp.write(render_template(template, **settings))
        input_fp.flush()

        # Get filesystem path to temporary file
        path_to_input = input_fp.name

        # Call streamer with input file
        try:
            subprocess.check_call([path_to_streamer, path_to_input])
        except subprocess.CalledProcessError as e:
            print str(e)
            input_fp.seek(0)
            print input_fp.read()

        tables = parse_output(settings['output_filename'])

    return tables


def render_template(template, **kwargs):
    """
    Render the template object with a bunch of defaults for testing
    :param template: jinja2 template file
    :return: string of rendered template
    """
    return template.render(**kwargs)


def parse_output(output_file):
    import pandas as pd
    from StringIO import StringIO

    tables = []
    with open(output_file) as output_fp:
        contents = output_fp.read()

    for block in re.split('[+][+]+', contents):
        match = re.search('.*?--+$(.*?)$^$.*?(--+$.*?)?--+$(.*?)$^$', block, re.DOTALL | re.MULTILINE)
        if match:
            profile = pd.read_table(StringIO(match.group(1)),
                                    sep='\s+',
                                    header=None,
                                    names=['ind',
                                           'height',
                                           'pressure',
                                           'temperature',
                                           'h2o',
                                           'rh',
                                           'o3',
                                           'aer'
                                           ])
            radiance = pd.read_table(StringIO(match.group(3)),
                                     sep='\s+',
                                     header=None,
                                     names=['ind',
                                            'dirsw_down',
                                            'diffsw_down',
                                            'SWdown',
                                            'LWdown',
                                            'SWup',
                                            'LWup',
                                            'net',
                                            'heating_rate'])
            tables.append(profile.set_index('ind').join(radiance.set_index('ind')).set_index('height'))

    return tables


BANDS = [
    (20, 40),
    (40, 60),
    (60, 80),
    (80, 100),
    (100, 120),
    (120, 140),
    (140, 160),
    (160, 180),
    (180, 200),
    (200, 220),
    (220, 240),
    (240, 260),
    (260, 280),
    (280, 300),
    (300, 320),
    (320, 340),
    (340, 360),
    (360, 380),
    (380, 400),
    (400, 420),
    (420, 440),
    (440, 460),
    (460, 480),
    (480, 500),
    (500, 520),
    (520, 540),
    (540, 560),
    (560, 580),
    (580, 600),
    (600, 620),
    (620, 640),
    (640, 660),
    (660, 680),
    (680, 700),
    (700, 720),
    (720, 740),
    (740, 760),
    (760, 780),
    (780, 800),
    (800, 820),
    (820, 840),
    (840, 860),
    (860, 880),
    (880, 900),
    (900, 920),
    (920, 940),
    (940, 960),
    (960, 980),
    (980, 1000),
    (1000, 1020),
    (1020, 1040),
    (1040, 1060),
    (1060, 1080),
    (1080, 1100),
    (1100, 1120),
    (1120, 1140),
    (1140, 1160),
    (1160, 1180),
    (1180, 1200),
    (1200, 1220),
    (1220, 1240),
    (1240, 1260),
    (1260, 1280),
    (1280, 1300),
    (1300, 1320),
    (1320, 1340),
    (1340, 1360),
    (1360, 1380),
    (1380, 1400),
    (1400, 1420),
    (1420, 1440),
    (1440, 1460),
    (1460, 1480),
    (1480, 1500),
    (1500, 1520),
    (1520, 1540),
    (1540, 1560),
    (1560, 1580),
    (1580, 1600),
    (1600, 1620),
    (1620, 1640),
    (1640, 1660),
    (1660, 1680),
    (1680, 1700),
    (1700, 1720),
    (1720, 1740),
    (1740, 1760),
    (1760, 1780),
    (1780, 1800),
    (1800, 1820),
    (1820, 1840),
    (1840, 1860),
    (1860, 1880),
    (1880, 1900),
    (1900, 1920),
    (1920, 1940),
    (1940, 1960),
    (1960, 1980),
    (1980, 2000),
    (2000, 2080),
    (2080, 2160),
    (2160, 2240),
    (2240, 2320),
    (2320, 2400),
    (2400, 2480),
    (2500, 2920),
    (2920, 3440),
    (3440, 4200),
    (4200, 4700),
    (4700, 6080),
    (6080, 6520),
    (6520, 7840),
    (7840, 8400),
    (8400, 9120),
    (9120, 10000),
    (10000, 11540),
    (11540, 12820),
    (12820, 13300),
    (13300, 14500),
    (14500, 15620),
    (15620, 17540),
    (17540, 19240),
    (19240, 20840),
    (20840, 22720),
    (22720, 25000),
    (25000, 27780),
    (27780, 30300),
    (30300, 33340),
    (33340, 35710)
]

if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser()
    args = parser.parse_args()
    sys.exit(main(args))
