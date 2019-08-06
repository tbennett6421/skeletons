# Basics
The basic format of an awk command is:

```
awk '/search_pattern/ { action_to_take_on_matches; another_action; }' file_to_parse
```
or more succinctly
```
awk 'condition { action }' file_to_parse
```

----------------------------

### Print a file
```
awk '{print}' /etc/fstab
```

### Search in file (grep)
```
awk '/UUID/' /etc/fstab
```

### Search with regex
```
awk '/^UUID/' /etc/fstab
```

### AWK search and print column 1
```
awk '/^UUID/ {print $1;}' /etc/fstab
```

# Understanding Awk beyond basics
## References
We can reference every column (as delimited by whitespace) by variables associated with their column number. 
 * The first column can be referenced by $1 for instance.
 * The entire line can by referenced by $0.

## Internal Variables
Awk uses some internal variables to assign certain pieces of information as it processes a file.

**The internal variables that Awk uses are:**
| Variable | Purpose |
| -- | -- |
| FILENAME | References the current input file. |
| FNR | References the number of the current record relative to the current input file. For instance, if you have two input files, this would tell you the record number of each file instead of as a total. |
| FS | The current field separator used to denote each field in a record. By default, this is set to whitespace. |
| NF | The number of fields in the current record. |
| NR | The number of the current record. |
| OFS | The field separator for the outputted data. By default, this is set to whitespace. |
| ORS | The record separator for the outputted data. By default, this is a newline character. |
| RS | The record separator used to distinguish separate records in the input file. By default, this is a newline character. |


