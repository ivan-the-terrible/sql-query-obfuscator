import logging
import os
import sys
from pathlib import Path
from typing import Tuple

from sqlglot import exp, parse_one

COLUMN_COUNTER = 0
TABLE_COUNTER = 0


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


def transformer(node):
    if isinstance(node, exp.Column):
        global COLUMN_COUNTER
        COLUMN_COUNTER += 1
        return "column_" + str(COLUMN_COUNTER)
    elif isinstance(node, exp.Table):
        global TABLE_COUNTER
        TABLE_COUNTER += 1
        return "table_" + str(TABLE_COUNTER)
    return node


def obfuscate_sql_query(sql_file) -> str:
    """
    Obfuscates the SQL query.

    Args:
      sql_file: SQL file to be obfuscated
    """
    with open(sql_file, "r") as file:
        sql_query = file.read()

    if sql_query.count(";") > 1:
        sql_queries = sql_query.split(";")
    else:
        sql_queries = [sql_query]

    obfuscated_sql_queries = ""
    for sql_query in sql_queries:
        if sql_query.strip():
            expression_tree = parse_one(sql_query)

            transformed_tree = expression_tree.transform(transformer)
            obfuscated_sql = transformed_tree.sql()
            obfuscated_sql_queries += obfuscated_sql + ";\n"

    return obfuscated_sql_queries


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
