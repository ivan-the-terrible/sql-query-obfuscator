# sql-query-obfuscator

An automated tool to ingest your SQL QUERY (not the data) and obfuscate column names, table names, and other aspects of the query itself.

## Usage

Running the script requires parameters:

- Path of source SQL file
- Path for new obfuscated SQL file and/or including the file name.

If you do not include these when running the script, you will be prompted for them.

Once the script is done, it will output the obfuscated SQL file.

If you do not include an output path, the script will output the obfuscated file where the original file is with the name `"obfuscated-{sql_file_name}.sql"`. If you include a path with no file name for the new file, again the new file will be named `"obfuscated-{sql_file_name}.sql"` and deposited where you specified.
