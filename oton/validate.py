import sys
from os.path import exists, isfile

from .constants import *


# Order:
# 1. Validate token syntax
# 2. Validate token order
# 3. Validate input/output order
def validate_ocrd_file(filepath, standalone=True):
    if not exists(filepath):
        print(f"OCR-D file {filepath} does not exist!")
        sys.exit(2)
    if not isfile(filepath):
        print(f"OCR-D file {filepath} is not a readable file!")
        sys.exit(2)

    print(f"Start validation of {filepath} ...")

    # Extract tokens from a file
    ocrd_lines = _ocrd_extract_tokens(filepath)

    # Validate token syntax 
    _ocrd_validate_token_syntax(ocrd_lines)

    # Validate inputs/outputs order
    _ocrd_validate_io_order(ocrd_lines)

    print(f"Validation of {filepath} has been successful; no errors detected.")

    if not standalone:
        return ocrd_lines

# Rules:
# 1. Each QM and BACKSLASH is a separate token
# 2. Each ocrd-process is a separate token
# 3. Each -I, -O, and -P is a separate token
def _ocrd_extract_tokens(filepath):
    ocrd_lines = []

    # Extract tokens from the ocrd_file
    # Unnecessary empty spaces/lines are discarded
    with open(filepath, mode='r') as ocrd_file:
        for line in ocrd_file:
            curr_line_tokens = []
            line = line.strip().split(SPACE)
            for token in line:
                if len(token) == 0: continue
                
                # Create separate tokens
                # for quotation marks
                if token.startswith(QM):
                    curr_line_tokens.append(QM)
                    curr_line_tokens.append(token[1:])
                elif token.endswith(QM):
                    curr_line_tokens.append(token[:-1])
                    curr_line_tokens.append(QM)
                else:
                    curr_line_tokens.append(token)

            if len(curr_line_tokens) > 0:
                ocrd_lines.append(curr_line_tokens)
        return ocrd_lines

  # Rules:
  # 1. The first line starts with 'ocrd process \'
  # 2. Each line starting from line 2 must have 
  # a single processor call, an input fule, 
  # and an output file. In other words,
  # a minimum amount of tokens.
  # 3. Each ocrd command starts 
  # with a quotation mark (QM)
  # 4. After a QM token on each line
  # a valid ocr-d process must follow
  # 5. After a '-I' token on each line
  # only one argument must follow
  # 6. After a '-O' token on each line
  # only one argument must follow
  # 7. After a '-P' token on each line
  # only two arguments must follow
  # 8. Only one '-I' and one '-O' token allowed on each line
  # 9. Multiple '-P' tokens are allowed on each line
  # 10. The order of '-I', '-O', and '-P' does not matter
  # Warning:
  # -P are not checked if they are supported 
  # or not by the specific OCR-D processors
  # 11. Each ocrd command ends
  # with a quotation mark (QM)
  # 12. Each line except the last one ends 
  # with a BACKSLASH (BACKSLASH).
  # The last line ends with a QM.
  # 13. Invalid chars inside tokens
  # invalidate the token
def _ocrd_validate_token_syntax(lines):
    # Validate the first line syntax (Rule 1)
    expected = ['ocrd', 'process', BACKSLASH]
    first_line = lines[0]
    if not first_line == expected:
      print("Syntax error!")
      print(f"Invalid line: {1}!")
      print(f"Expected: '{' '.join(expected)}', tokens: {len(expected)}")
      print(f"Got: '{' '.join(first_line)}', tokens: {len(first_line)}")
      print("Hint: Single spaces between the tokens are allowed.")
      sys.exit(2)

    # Validate lines starting from the second line 
    # (Rules 2-12)
    for line_index in range (1, len(lines)):
      # Validate the start of an OCR-D line/command
      # (Rule 3)
      if not lines[line_index][0] == QM:
        print("Syntax error!")
        print(f"Invalid line: {line_index+1}, wrong token at {1}")
        print(f"Token: {lines[line_index][0]}")
        print(f"Hint: Commands must start with a quotation mark ({QM}).")
        sys.exit(2)

      # Validate the minimum amount of tokens needed 
      # (Rule 2)
      # This check also prevents index out of 
      # range errors in the following Rule checks
      if len(lines[line_index]) < 8:
        # the last line has one less token than usual
        if line_index == len(lines)-1 and len(lines[-1]) >= 7:
          continue
        print("Syntax error!")
        print(f"Invalid line {line_index+1}, low amount of tokens!")
        print(f"Hint: Each line must start with a {QM} and end with a {BACKSLASH}.")
        print("Hint: Each line must have a processor call, an input file, and an output file.")
        sys.exit(2)
      
      # Validate the OCR-D processor call in the OCR-D command
      # (Rule 4)
      ocrd_processor = f"ocrd-{lines[line_index][1]}"
      if ocrd_processor not in OCRD_PROCESSORS:
        print("Syntax error!")
        print(f"Ivalid line: {line_index+1}, invalid token: {lines[line_index][1]}")
        print("Hint: ocrd-process is spelled incorrectly or does not exists.")
        sys.exit(2)

      # Validate the -I, -O, and -P 
      # (Rules 5-10)
      input_found = False  # track duplicate inputs
      output_found = False  # track duplicate outputs
      processed_tokens = [] # track already matched tokens
      for token_index in range(2, len(lines[line_index])):
        token = lines[line_index][token_index]
        if token == '-I':
          # Duplicate input token found
          if input_found:
            print("Syntax Error!")
            print(F"Invalid line: {line_index+1}, duplicate -I token at: {token_index}")
            print("Hint: Only a single input token is allowed!")
            sys.exit(2)
          input_found = True
          # Validate the -I token
          # Exactly one token comes after the -I
          # The token must not be a QM or a BACKSLASH
          token_next = lines[line_index][token_index+1]
          if token_next == QM or token_next == BACKSLASH or \
            token_next == '-O' or token_next == '-P':
            print("Syntax Error!")
            print(F"Invalid line: {line_index+1}, wrong or missing input token for: {token_index}")
            sys.exit(2)
          else:
            processed_tokens.append(token_next)
          # print(f"InputToken: {token}, {token_next}")

        elif token == '-O':
          # Duplicate output token found
          if output_found:
            print("Syntax Error!")
            print(F"Invalid line: {line_index+1}, duplicate -O token at: {token_index}")
            print("Hint: Only a single output token is allowed!")
            sys.exit(2)
          output_found = True
          # Validate the -O token
          # Exactly one token comes after the -O
          # The token must not be a '"' or '\'
          token_next = lines[line_index][token_index+1]
          if token_next == QM or token_next == BACKSLASH or \
            token_next == '-I' or token_next == '-P':
            print("Syntax Error!")
            print(F"Invalid line: {line_index+1}, wrong or missing output token for: {token_index}")
            sys.exit(2)
          else:
            processed_tokens.append(token_next)
          # print(f"OutputToken: {token}, {token_next}")

        elif token == '-P':
          # Validate the -P token
          # Exactly two tokens comes after the -P
          # The tokens must not be a '"' or '\'
          token_next1 = lines[line_index][token_index+1]
          if token_next1 == QM or token_next1 == BACKSLASH or \
            token_next1 == '-I' or token_next1 == '-O':
            print("Syntax Error!")
            print(F"Invalid line: {line_index+1}, wrong or missing parameter token at: {token_index+1}")
            sys.exit(2)
          else:
            processed_tokens.append(token_next1)

          token_next2 = lines[line_index][token_index+2]
          if token_next2 == QM or token_next2 == BACKSLASH or \
            token_next2 == '-I' or token_next2 == '-O':
            print("Syntax Error!")
            print(F"Invalid line: {line_index+1}, wrong or missing parameter token at: {token_index+2}")
            sys.exit(2)
          else:
            processed_tokens.append(token_next2)
          # print(f"ParameterToken: {token}, {token_next1}, {token_next2}")

        else:
          if token == QM or token == BACKSLASH:
            continue 
          if token in processed_tokens:
            continue
          else:
            print("Syntax Error!")
            print(f"Invalid line: {line_index+1}, wrong unknown token at: {token_index}")
            print(f"Token: {token}")
            print(f"Hint: Exactly one token must follow -I or -O.")
            print(f"Hint: Exactly two tokens must follow -P.")
            print("Tokens following -I, -O, and -P cannot be a quotation mark or a BACKSLASH.")
            sys.exit(2)

      # Validate the end of an OCR-D command (Rule 11)
      if not lines[line_index][-2] == QM:
        # the last line has no QM in position -2
        if line_index == len(lines)-1:
          continue
        print("Syntax error!")
        print(f"Invalid line: {line_index+1}")
        print("Hint: Commands must end with a single quotation mark.")
        print("Hint: No whitespaces before the quotation mark.")
        sys.exit(2)

      # Validate the end of a OCR-D line (Rule 12)
      if not lines[line_index][-1] == BACKSLASH:
        # the last line has no '\\' in position -1
        if line_index == len(lines)-1:
          print(f"Line_index: {line_index}")
          continue
        print("Syntax error!")
        print(f"Invalid line: {line_index+1}")
        print("Hint: Lines must end with a single \\.")
        sys.exit(2)

    # Validate token symbols (Rule 13)
    _ocrd_validate_token_symbols(lines)

  # Rules:
  # 1. A single char token must be either: QM or BACKSLASH
  # 2. A double char token must be either: -I, -O, or -P
  # 3. Other tokens must contain only VALID_CHARS
def _ocrd_validate_token_symbols(lines):
    # Check for invalid symbols/tokens
    for line_index in range (0, len(lines)):
      for token_index in range(0, len(lines[line_index])):
        token = lines[line_index][token_index]
        # Rule 1
        if len(token) == 1:
          if token == QM or token == BACKSLASH:
            continue
          else:
            print("Syntax error!")
            print(f"Invalid line {line_index+1}, invalid token: {token}")
            print("Hint: Remove invalid tokens.")
            sys.exit(2)
        # Rule 2
        elif len(token) == 2:
          if token[0] == '-':
            if token[1] == 'I' or \
            token[1] == 'O' or \
            token[1] == 'P':
              continue
            else:
              print("Syntax error!")
              print(f"Invalid line {line_index+1}, invalid token: {token}")
              print("Hint: Remove invalid tokens.")
              sys.exit(2)
          else:
            if token[0] not in VALID_CHARS or token[1] not in VALID_CHARS:
              print("Syntax error!")
              print(f"Invalid line {line_index+1}, invalid token: {token}")  
              print("Hint: Remove invalid tokens.")
              sys.exit(2)
        # Rule 3
        else:
          for char in token:
            if char not in VALID_CHARS:
              print("Syntax error!")
              print(f"Invalid line {line_index+1}, invalid token: {token}")  
              print("Hint: Remove invalid tokens.") 
              print(f"Hint: Tokens cannot contain character: {char}")
              sys.exit(2)

  # Rules
  # 1. The input parameter of the second line is the entry-point
  # 2. The input parameter of lines after the second line 
  # are the output parameters of the previous line 
def _ocrd_validate_io_order(lines):
    prev_output = None
    curr_input = None
    curr_output = None

    for line_index in range (1, len(lines)):
      curr_line = lines[line_index]
      curr_input = curr_line[curr_line.index('-I')+1]
      curr_output = curr_line[curr_line.index('-O')+1]

      if prev_output is not None:
        if prev_output != curr_input:
          print(f'Input/Output mismatch error!')
          print(f'{prev_output} on line {line_index} does not match with {curr_input} on line {line_index+1}')
          sys.exit(2)

      prev_output = curr_output
