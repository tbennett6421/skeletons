# Organizing host and group variables

Although you can store variables in the main inventory file, storing separate host and group variables files may help you track your variable values more easily.

Host and group variables can be stored in individual files relative to the inventory file (not directory, it is always the file).

These variable files are in YAML format. Valid file extensions include ‘.yml’, ‘.yaml’, ‘.json’, or no file extension. See YAML Syntax if you are new to YAML.

Let’s say, for example, that you keep your inventory file at `/etc/ansible/hosts`. You have a host named ‘foosball’ that’s a member of two groups: ‘raleigh’ and ‘webservers’. That host will use variables in YAML files at the following locations:
```
/etc/ansible/group_vars/raleigh
/etc/ansible/group_vars/webservers
/etc/ansible/host_vars/foosball
```
For instance, suppose you have hosts grouped by datacenter, and each datacenter uses some different servers. The data in the groupfile ‘/etc/ansible/group_vars/raleigh’ for the ‘raleigh’ group might look like:

```
---
ntp_server: acme.example.org
database_server: storage.example.org
```

It is okay if these files do not exist, as this is an optional feature.

As an advanced use case, you can create directories named after your groups or hosts, and Ansible will read all the files in these directories in lexicographical order. An example with the ‘raleigh’ group:

```
/etc/ansible/group_vars/raleigh/db_settings
/etc/ansible/group_vars/raleigh/cluster_settings
```

All hosts that are in the ‘raleigh’ group will have the variables defined in these files available to them. This can be very useful to keep your variables organized when a single file starts to be too big, or when you want to use Ansible Vault on a part of a group’s variables.
