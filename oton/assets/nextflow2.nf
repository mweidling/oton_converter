nextflow.enable.dsl = 2

params.workspace_path = "$projectDir/ocrd-workspace/"
params.mets_path = "$projectDir/ocrd-workspace/mets.xml"

process ocrd_cis_ocropy_binarize_0 {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    ocrd-cis-ocropy-binarize -I ${input_dir} -O ${output_dir}
    """
}

process ocrd_anybaseocr_crop_1 {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    ocrd-anybaseocr-crop -I ${input_dir} -O ${output_dir}
    """
}

process ocrd_skimage_denoise_2 {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    ocrd-skimage-denoise -I ${input_dir} -O ${output_dir} -p '{"level-of-operation": "page"}'
    """
}

process ocrd_tesserocr_deskew_3 {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    ocrd-tesserocr-deskew -I ${input_dir} -O ${output_dir} -p '{"operation_level": "page"}'
    """
}

process ocrd_tesserocr_segment_4 {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    ocrd-tesserocr-segment -I ${input_dir} -O ${output_dir} -p '{"shrink_polygons": "true"}'
    """
}

process ocrd_cis_ocropy_dewarp_5 {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    ocrd-cis-ocropy-dewarp -I ${input_dir} -O ${output_dir}
    """
}

process ocrd_tesserocr_recognize_6 {
  maxForks 1

  input:
    path mets_file
    val input_dir
    val output_dir

  output:
    path mets_file

  script:
    """
    ocrd-tesserocr-recognize -I ${input_dir} -O ${output_dir} -p '{"textequiv_level": "glyph", "overwrite_segments": "true", "model": "GT4HistOCR_50000000.997_191951"}'
    """
}

workflow {
  main:
    ocrd_cis_ocropy_binarize_0(params.mets_path, "OCR-D-IMG", "OCR-D-BIN")
    ocrd_anybaseocr_crop_1(ocrd_cis_ocropy_binarize_0.out, "OCR-D-BIN", "OCR-D-CROP")
    ocrd_skimage_denoise_2(ocrd_anybaseocr_crop_1.out, "OCR-D-CROP", "OCR-D-BIN-DENOISE")
    ocrd_tesserocr_deskew_3(ocrd_skimage_denoise_2.out, "OCR-D-BIN-DENOISE", "OCR-D-BIN-DENOISE-DESKEW")
    ocrd_tesserocr_segment_4(ocrd_tesserocr_deskew_3.out, "OCR-D-BIN-DENOISE-DESKEW", "OCR-D-SEG")
    ocrd_cis_ocropy_dewarp_5(ocrd_tesserocr_segment_4.out, "OCR-D-SEG", "OCR-D-SEG-DEWARP")
    ocrd_tesserocr_recognize_6(ocrd_cis_ocropy_dewarp_5.out, "OCR-D-SEG-DEWARP", "OCR-D-OCR")
}


