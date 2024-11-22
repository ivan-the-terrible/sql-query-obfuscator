import logging
import os
import sys
from pathlib import Path
from typing import Tuple


def parse_input() -> Tuple[str, str]:
    """
    Parses the command line arguments or prompts the user for input.

    When the script is called, the arguments of the SQL file to be obfuscated and an output file name are expected. If the arguments are not provided, the user will be prompted for them.

    Returns:
      sql_input: SQL file to be obfuscated
      output_path: Obfuscated SQL file with its path
    """
    if len(sys.argv) < 3:
        sql_input = input("Enter the SQL file to be obfuscated: ")
        output_path = input("Enter the output file name: ")
    else:
        sql_input = sys.argv[1]
        output_path = sys.argv[2]

    return sql_input, output_path


def check_input(sql_input, output_path) -> Tuple[str, str]:
    """
    Checks if the input SQL file exists and the output file is not empty.

    Args:
      sql_input: SQL file to be obfuscated
      output_path: Obfuscated SQL file with its path

    Returns:
      sql_file: SQL file to be obfuscated
      output_path: Obfuscated SQL file with its path
    """
    current_directory = os.getcwd()

    if not os.path.isfile(sql_input):
        logging.error(f"{sql_input} is not a file.")
        sys.exit(1)

    if os.path.isdir(output_path):
        sql_file_name = Path(sql_input).stem
        output_path = os.path.join(output_path, f"obfuscated-{sql_file_name}.sql")
    else:
        if os.path.exists(output_path) or os.path.exists(
            os.path.join(current_directory, output_path)
        ):
            logging.error(f"{output_path} already exists.")
            sys.exit(1)

    return os.path.abspath(sql_input), os.path.abspath(output_path)


def obfuscate_sql_query(sql_file) -> str:
    """
    Obfuscates the SQL query.

    Args:
      sql_file: SQL file to be obfuscated
    """
    with open(sql_file, "r") as file:
        sql_query = file.read()

    return sql_query


def write_result(obfuscated_sql, output_path):
    """
    Writes the obfuscated SQL query to a file.

    Args:
      obfuscated_sql: Obfuscated SQL query
      output_path: Obfuscated SQL file with its path
    """
    with open(output_path, "w") as file:
        file.write(obfuscated_sql)


def main():
    sql_input, output_path = parse_input()
    sql_file, output_path = check_input(sql_input, output_path)

    obfuscated_sql = obfuscate_sql_query(sql_file)

    write_result(obfuscated_sql, output_path)


if __name__ == "__main__":
    main()
