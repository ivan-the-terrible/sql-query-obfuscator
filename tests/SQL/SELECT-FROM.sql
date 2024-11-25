SELECT * FROM test.important_table;

SELECT p.special_column FROM test.important_table p;

SELECT special_column FROM important_table;

SELECT special_column AS alias_column FROM test.important_table it
JOIN test.important_table2 it2 ON it.id = it2.id
WHERE it.id = 1;