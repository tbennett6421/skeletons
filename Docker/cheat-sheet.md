# Installing Docker
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable "
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli docker-compose containerd.io -y
```
Running a Docker compose yaml file
```
docker-compose up
```

# Display Containers

List all containers
```
docker ps -a
```

List all container IDs
```
docker ps -a -q
```

List containers without truncating output
```
docker ps --no-trunc
```

List containers filtering by exit signal (137=SIGKILL)
```bash
docker ps -a --filter 'exited=0'    # Exited with SUCCESS
docker ps -a --filter 'exited=137'  # Exited via SIGKILL
```

List containers by networking ports
```
docker ps --filter publish=80

docker ps --filter expose=8000-8080/tcp
```

# Pretty Print Containers

*see the section on format variables*

Output a colon delimited table with headers for use in `cut`/`awk`
```bash
sudo docker ps -a --format "table {{.var1}}: {{.var2}}
```

Output a colon delimited table without headers for use in `cut`/`awk`
```bash
sudo docker ps -a --format "{{.var1}}: {{.var2}}
```

# References

## Formatting output
Values for use with `--format`

| Var | Description |
| -- | -- |
| .ID | Container ID |
| .Image | Image ID |
| .Command | Quoted command |
| .CreatedAt | Time when the container was created. |
| .RunningFor | Elapsed time since the container was started. |
| .Ports | Exposed ports. |
| .Status | Container status. |
| .Size | Container disk size. |
| .Names | Container names. |
| .Labels | All labels assigned to the container. |
| .Label | Value of a specific label for this container. For example '{{.Label "com.docker.swarm.cpu"}}' |
| .Mounts | Names of the volumes mounted in this container. |
| .Networks | Names of the networks attached to this container. |




