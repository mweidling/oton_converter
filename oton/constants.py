from string import ascii_letters, digits

# All available processors.
# The list follows alphabetical order. 
# Source: https://ocr-d.de/en/workflows
OCRD_PROCESSORS = [
  'ocrd-anybaseocr-block-segmentation',
  'ocrd-anybaseocr-crop',
  'ocrd-anybaseocr-deskew',
  'ocrd-anybaseocr-dewarp',
  'ocrd-calamari-recognize',
  'ocrd-cis-align',
  'ocrd-cis-ocropy-binarize',
  'ocrd-cis-ocropy-clip',
  'ocrd-cis-ocropy-denoise',
  'ocrd-cis-ocropy-deskew',
  'ocrd-cis-ocropy-dewarp',
  'ocrd-cis-ocropy-resegment',
  'ocrd-cis-ocropy-segment',
  'ocrd-cis-postcorrect',
  'ocrd-cor-asv-ann-align',
  'ocrd-cor-asv-ann-evaluate',
  'ocrd-cor-asv-ann-process',
  'ocrd-detectron2-segment',
  'ocrd-dinglehopper',
  'ocrd-doxa-binarize',
  'ocrd-dummy',
  'ocrd-eynollah-segment',
  'ocrd-fileformat-transform',
  'ocrd-im6convert',
  'ocrd-olahd-client',
  'ocrd-olena-binarize',
  'ocrd-page-transform',
  'ocrd-page2tei',
  'ocrd-pagetopdf',
  'ocrd-pc-segmentation',
  'ocrd-preprocess-image',
  'ocrd-sbb-binarize',
  'ocrd-sbb-textline-detector',
  'ocrd-segment-evaluate',
  'ocrd-segment-extract-glyphs',
  'ocrd-segment-extract-lines',
  'ocrd-segment-extract-pages',
  'ocrd-segment-extract-regions',
  'ocrd-segment-extract-words',
  'ocrd-segment-from-coco',
  'ocrd-segment-from-masks',
  'ocrd-segment-project',
  'ocrd-segment-repair',
  'ocrd-segment-replace-original',
  'ocrd-segment-replace-page',
  'ocrd-skimage-binarize',
  'ocrd-skimage-normalize',
  'ocrd-skimage-denoise',
  'ocrd-skimage-denoise-raw',
  'ocrd-tesserocr-crop',
  'ocrd-tesserocr-deskew',
  'ocrd-tesserocr-fontshape',
  'ocrd-tesserocr-recognize',
  'ocrd-tesserocr-segment',
  'ocrd-tesserocr-segment-line',
  'ocrd-tesserocr-segment-region',
  'ocrd-tesserocr-segment-table',
  'ocrd-tesserocr-segment-word',
  'ocrd-typegroups-classifier'
]

# Valid characters to be used in the ocrd file
VALID_CHARS = f'-_.{ascii_letters}{digits}'

# SYMBOLS
BRACKETS = '{}'
BACKSLASH = '\\'
# Quotation Mark
QM = '"'
TAB = '\t'
LF = '\n'
SPACE = ' '

# NEXTFLOW RELATED
DSL2 = 'nextflow.enable.dsl = 2'
# input/output dirs
IN_DIR = 'input_dir'
OUT_DIR = 'output_dir'
# input/output dirs placeholders
IN_DIR_PH = f'${BRACKETS[0]}{IN_DIR}{BRACKETS[1]}'
OUT_DIR_PH = f'${BRACKETS[0]}{OUT_DIR}{BRACKETS[1]}'
