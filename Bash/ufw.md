# Install UFW

Notice that UFW is typically installed by default in Ubuntu. But if anything, you can install it yourself. To install UFW, run the following command.

```
sudo apt-get install ufw
```

# Adding Allow rules
In general, you can allow any port you need by using the following format:

`sudo ufw allow <port>/<optional: protocol>`

For example, adding a web server rule
```
sudo ufw allow 80/tcp
```

# Adding Deny rules

If you need to deny access to a certain port, use this:

`sudo ufw deny <port>/<optional: protocol>`

For example, let's deny access to our default MySQL port.

```
sudo ufw deny 3306
```

UFW also supports a simplified syntax for the most common service ports.

```
root@127:~$ sudo ufw deny mysql
Rule updated
Rule updated (v6)
```
# Allow access from a trusted IP address

Typically, you would need to allow access only to publicly open ports such as port 80. Access to all other ports need to be restricted or limited.

You can whitelist specific IP addresses to be able to access certain services

```
sudo ufw allow from 10.69.13.22 to any port 22
```

Let's also allow access to the MySQL port.
```
sudo ufw allow from 10.69.13.22 to any port 3306
```

# Check UFW status

Take a look at all of your rules.
```
sudo ufw status
```

Use the "verbose" parameter to see a more detailed status report.

```
sudo ufw status verbose
```

Use the "numbered" parameter to see a rules by their number

```
sudo ufw status numbered
```

# Enable UFW
To start/enable your UFW firewall, use the following command:
```
sudo ufw enable
```

# Disable/reload/restart UFW

To disable (stop) UFW, run this command.
```
sudo ufw disable
```

If you need to reload UFW (reload rules), run the following.
```
sudo ufw reload
```

In order to restart UFW, you will need to disable it first, and then enable it again.
```
sudo ufw disable
sudo ufw enable
```

# Removing rules

You can remove rules by their port

```
sudo ufw delete allow 80/tcp
```

by their application
```
sudo ufw delete allow mysql
```

or by their number
```
sudo ufw delete 13
```

# Back to default settings

If you need to go back to default settings, simply type in the following command. This will revert any of your changes.

```
sudo ufw reset
```
