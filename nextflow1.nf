nextflow.enable.dsl = 2

params.workspace_path = "$projectDir/ocrd-workspace/"
params.mets_path = "$projectDir/ocrd-workspace/mets.xml"
params.venv_path = "\$HOME/venv37-ocrd/bin/activate"

process ocrd_cis_ocropy_binarize {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    source "${params.venv_path}"
    ocrd-cis-ocropy-binarize -I ${input_dir} -O ${output_dir}
    deactivate
    """
}

process ocrd_anybaseocr_crop {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    source "${params.venv_path}"
    ocrd-anybaseocr-crop -I ${input_dir} -O ${output_dir}
    deactivate
    """
}

process ocrd_skimage_binarize {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    source "${params.venv_path}"
    ocrd-skimage-binarize -I ${input_dir} -O ${output_dir} -P method li
    deactivate
    """
}

process ocrd_skimage_denoise {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    source "${params.venv_path}"
    ocrd-skimage-denoise -I ${input_dir} -O ${output_dir} -P level-of-operation page
    deactivate
    """
}

process ocrd_tesserocr_deskew {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    source "${params.venv_path}"
    ocrd-tesserocr-deskew -I ${input_dir} -O ${output_dir} -P operation_level page
    deactivate
    """
}

process ocrd_cis_ocropy_segment {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    source "${params.venv_path}"
    ocrd-cis-ocropy-segment -I ${input_dir} -O ${output_dir} -P level-of-operation page
    deactivate
    """
}

process ocrd_cis_ocropy_dewarp {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    source "${params.venv_path}"
    ocrd-cis-ocropy-dewarp -I ${input_dir} -O ${output_dir}
    deactivate
    """
}

process ocrd_calamari_recognize {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    source "${params.venv_path}"
    ocrd-calamari-recognize -I ${input_dir} -O ${output_dir} -P checkpoint_dir qurator-gt4histocr-1.0
    deactivate
    """
}

workflow {
  main:
    ocrd_cis_ocropy_binarize(params.mets_path, "OCR-D-IMG", "OCR-D-BIN")
    ocrd_anybaseocr_crop(ocrd_cis_ocropy_binarize.out, "OCR-D-BIN", "OCR-D-CROP")
    ocrd_skimage_binarize(ocrd_anybaseocr_crop.out, "OCR-D-CROP", "OCR-D-BIN2")
    ocrd_skimage_denoise(ocrd_skimage_binarize.out, "OCR-D-BIN2", "OCR-D-BIN-DENOISE")
    ocrd_tesserocr_deskew(ocrd_skimage_denoise.out, "OCR-D-BIN-DENOISE", "OCR-D-BIN-DENOISE-DESKEW")
    ocrd_cis_ocropy_segment(ocrd_tesserocr_deskew.out, "OCR-D-BIN-DENOISE-DESKEW", "OCR-D-SEG")
    ocrd_cis_ocropy_dewarp(ocrd_cis_ocropy_segment.out, "OCR-D-SEG", "OCR-D-SEG-LINE-RESEG-DEWARP")
    ocrd_calamari_recognize(ocrd_cis_ocropy_dewarp.out, "OCR-D-SEG-LINE-RESEG-DEWARP", "OCR-D-OCR")
}


