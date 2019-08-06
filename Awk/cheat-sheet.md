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


