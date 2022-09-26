import click

@click.group()
def cli():
    pass

@cli.command("convert", help="Convert a OCR-D workflow to a NextFlow workflow.")
@click.option('-I', '--input', help='PATH to a OCR-D workflow file in TXT format')
@click.option('-O', '--output', help='PATH to a NextFlow workflow file')
@click.option('-D', '--docker', help='Set if a Docker image is used for OCR-D workflow')
def convert(input, output, docker):
    print("Hello World!")
