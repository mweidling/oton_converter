import click
from .convert import Converter
from .validate import validate_ocrd_file

@click.group()
def cli():
    pass

@cli.command("convert", help="Convert a OCR-D workflow to a NextFlow workflow.")
@click.option('-I', '--input', help='PATH to a OCR-D workflow file in TXT format')
@click.option('-O', '--output', help='PATH to a NextFlow workflow file')
@click.option('-D', '--docker', help='Set if a Docker image is used for OCR-D workflow')
def convert(input, output, docker):
    converter = Converter()
    print(f"OtoN> In: {input}")
    print(f"OtoN> Out: {output}")
    converter.convert_OtoN(input, output)

@cli.command("validate", help="Validate OCR-D workflow file")
@click.option('-I', '--input', help='PATH to a OCR-D workflow file in TXT format')
def validate(input):
    validate_ocrd_file(input)
