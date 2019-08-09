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

# Interacting with containers
exec into container
```bash
docker exec -it $(docker container ls  | grep '<seach_term>' | awk '{print $1}') bash
```
exec into container on windows with Git Bash
```bash
winpty docker exec -it $(docker container ls  | grep '<seach_term>' | awk '{print $1}') bash
```

# Taking actions on containers
Stop ALL containers
```bash
docker stop $(docker ps -a -q)
```

Remove ALL containers
```bash
docker rm -f $(docker ps -a -q)
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

# Task Examples

Create new docker container, ie. ubuntu
```bash
docker pull ubuntu:latest
docker run -i -t ubuntu /bin/bash
```

Print all docker containers in a `tab`ulated table
```bash
sudo docker ps -a --format "table {{.ID}}: {{.Image}}: {{.Command}}: {{.Status}}: {{.Ports}}: {{.Names}} | \
awk -v OFS="\t" -v FS=":" '{$1=$1}1'
```

Clean up orphaned volumes
```bash
docker volume rm $(docker volume ls -qf dangling=true)
```

Clean up orphaned networks
```bash
docker network rm $(docker network ls -q)
```
