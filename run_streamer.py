#!/usr/bin/env python

import jinja2
import subprocess
import tempfile


def main(args):
    path_to_streamer = './streamer'
    path_to_template = './template.inp'

    # Create a file to hold the input data
    # After it exits the file will be deleted immediately
    with tempfile.NamedTemporaryFile('w', delete=True) as input_fp:
        # Read the template file and create jinja2 template
        with open(path_to_template) as template_fp:
            template = jinja2.Template(template_fp.read())

        # Write the rendered template to the temporary input file
        input_fp.write(render_template(template))
        input_fp.flush()

        # Get filesystem path to temporary file
        path_to_input = input_fp.name

        # Call streamer with input file
        subprocess.check_call([path_to_streamer, path_to_input])


def render_template(template):
    """
    Render the template object with a bunch of defaults for testing
    :param template: jinja2 template file
    :return: string of rendered template
    """
    return template.render(output_filename='output_filename.out',
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


if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser()
    args = parser.parse_args()
    sys.exit(main(args))
