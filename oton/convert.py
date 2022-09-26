import tomli
from .constants import *
from .validate import validate_ocrd_file


class Converter:
  def __init__(self):
    # Convention:
    # ocrd_lines holds the number of lines
    # of the input ocrd file
    # for each line an inner list is created
    # to hold separate tokens of that line
    self.ocrd_lines = []
    # Convention:
    # nf_lines holds the number of lines
    # of the output Nextflow file
    # for each line an inner list is created
    # to hold separate tokens of that line
    self.nf_lines = []

  def _print_ocrd_tokens(self):
    print(f"INFO: lines in the ocrd file: {len(self.ocrd_lines)}")
    print(f"INFO: TOKENS ON LINES")
    for i in range (0, len(self.ocrd_lines)):
      print(f"ocrd_lines[{i}]: {self.ocrd_lines[i]}")
    print(f"INFO: TOKENS ON LINES END")


  def _print_nextflow_tokens(self):
    print(f"INFO: lines in the nextflow file: {len(self.nf_lines)}")
    print(f"INFO: TOKENS ON LINES")
    for i in range (0, len(self.nf_lines)):
      print(f"nf_lines[{i}]: {self.nf_lines[i]}")
    print(f"INFO: TOKENS ON LINES END")

  def _extract_nf_process_name(self, ocrd_processor):
    return f"{ocrd_processor.replace('-','_')}"

  def _extract_ocrd_commands(self, ocrd_lines):
    ocrd_commands = []
    for line_index in range(1, len(ocrd_lines)):
      first_QM_index = 0
      last_QM_index = 0

      for token_index in range(1, len(ocrd_lines[line_index])):
        curr_token = ocrd_lines[line_index][token_index]
        if curr_token == QM:
          last_QM_index = token_index
          break

      line = ocrd_lines[line_index]
      # Append ocrd- as a prefix
      line[first_QM_index+1] = f'ocrd-{line[first_QM_index+1]}'
      # Extract the ocr-d command without quotation marks
      sub_line = line[first_QM_index+1:last_QM_index]
      ocrd_commands.append(sub_line)

    return ocrd_commands

  # Rules:  
  # 1. Create the default beginning of a Nextflow script
  # 2. For each ord command (on each line) a separate 
  # Nextflow process is created
  # 3. Create the main workflow
  def convert_OtoN(self, input_path, output_path):
    ocrd_lines = validate_ocrd_file(input_path, standalone=False)

    # Nextflow script lines
    self.nf_lines = []

    # Rule 1
    self.nf_lines.append(DSL2)
    self.nf_lines.append('')

    with open('config.toml', mode='rb') as fp:
        config = tomli.load(fp)
        venv_path = config['venv_path']
        params_venv = f'params.venv = {QM}{venv_path}{QM}'
        workspace_path = config['workspace_path']
        params_workspace = f'params.workspace = {QM}{workspace_path}{QM}'
        mets_path = config['mets_path']
        params_mets = f'params.mets = {QM}{mets_path}{QM}'

    self.nf_lines.append(params_venv)
    self.nf_lines.append(params_workspace)
    self.nf_lines.append(params_mets)
    self.nf_lines.append('')

    # Create the nextflow processes
    # Rule 2
    ocrd_commands = self._extract_ocrd_commands(ocrd_lines)

    # Nextflow processes list
    nf_processes = []
    for oc in ocrd_commands:
      nf_process_name = self._extract_nf_process_name(oc[0])
      
      # Find the input/output parameters of the ocrd command
      in_index = oc.index('-I')+1
      out_index = oc.index('-O')+1
      oc_in = f'{QM}{oc[in_index]}{QM}'
      oc_out = f'{QM}{oc[out_index]}{QM}'

      # Replace the input/output parameters with their placeholders
      oc[in_index] = IN_DIR_PH
      oc[out_index] = OUT_DIR_PH
      # The bash string of the ocrd command
      oc_bash_str = ' '.join(oc)

      # Start building the current NF process
      self.nf_lines.append(f"process {nf_process_name} {BRACKETS[0]}")
      self.nf_lines.append(f"{TAB}maxForks 1")
      self.nf_lines.append('')
      self.nf_lines.append(f'{TAB}input:')
      self.nf_lines.append(f'{TAB}{TAB}path mets_file')
      self.nf_lines.append(f'{TAB}{TAB}val {IN_DIR}')
      self.nf_lines.append(f'{TAB}{TAB}val {OUT_DIR}')
      self.nf_lines.append('')
      self.nf_lines.append(f'{TAB}output:')
      self.nf_lines.append(f'{TAB}{TAB}val {OUT_DIR}')
      self.nf_lines.append('')
      self.nf_lines.append(f'{TAB}script:')
      self.nf_lines.append(f'{TAB}"""')
      self.nf_lines.append(f'{TAB}source "${BRACKETS[0]}params.venv{BRACKETS[1]}"')
      self.nf_lines.append(f'{TAB}{oc_bash_str}')
      self.nf_lines.append(f'{TAB}deactivate')
      self.nf_lines.append(f'{TAB}"""')
      self.nf_lines.append(BRACKETS[1])
      self.nf_lines.append('')
      # This list is used inside the workflow section in Rule 3
      nf_processes.append([nf_process_name, oc_in, oc_out])

    # Create the main workflow
    # Rule 3
    self.nf_lines.append(f'workflow {BRACKETS[0]}')
    self.nf_lines.append(f'{TAB}main:')
    previous_nfp = None
    for nfp in nf_processes:
      if previous_nfp == None:
        self.nf_lines.append(f'{TAB}{TAB}{nfp[0]}(params.mets, {nfp[1]}, {nfp[2]})')
      else:
        self.nf_lines.append(f'{TAB}{TAB}{nfp[0]}(params.mets, {previous_nfp}.out, {nfp[2]})')
      previous_nfp = nfp[0]
    self.nf_lines.append(f'{BRACKETS[1]}')

    # self._print_nextflow_tokens()
    # Write Nextflow line tokens to an output file
    with open(output_path, mode='w') as nextflow_file:
      for token_line in self.nf_lines:
        nextflow_file.write(f'{token_line}\n')
