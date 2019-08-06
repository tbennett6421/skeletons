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

## Expanded Format
Awk is fairly complex in it's capabilities. Changing the internal variable would typically be done before any text processing against documents. Awk supports this by using a BEGIN condition to preprocess documents.

| Keyword | Purpose |
| -- | -- |
| BEGIN | condition that match before the document has been processed |
| END | condition that match after the document has been processed |

This can further generalize our pipeline as such
```
awk 'BEGIN { action; }
/search/ { action; }
END { action; }' input_file
```

Examples include parsing `/etc/passwd` and extracting the users
```
awk 'BEGIN { FS=":"; }
{ print $1; }' /etc/passwd
```

or printing a table header/footer
```
awk 'BEGIN { FS=":"; print "User\t\tUID\t\tGID\t\tHome\t\tShell\n--------------"; }
{print $1,"\t\t",$3,"\t\t",$4,"\t\t",$6,"\t\t",$7;}
END { print "---------\nFile Complete" }' /etc/passwd
```
