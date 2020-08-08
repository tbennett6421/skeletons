# Getting Info

List ZFS filesystems
```bash
sudo zfs list
```

List pools
```bash
sudo zpool list
```

Get the status of a pool
```bash
sudo zpool status POOL
```

# Creating Pools

Create a striped pool (RAID 0)
```bash
sudo zpool create -f -m /zfs/mount/point POOL sdb sdc sdd
```

Create a vdev mirror (RAID 1)
```bash
sudo zpool create -f -m /zfs/mount/point POOL mirror sda sdb
```
Create a raidz pool (RAID 5)
```bash
sudo zpool create -f -m /zfs/mount/point POOL raidz sdb sdc sdd
```

Create a striped mirror (RAID 10)
```bash
sudo zpool create -f -m /zfs/mount/point POOL mirror sda sdb mirror sdc sdd
```

# Modifying ZFS pools

change zfs mountpoint
```bash
# do not use trailing slashes otherwise mount will fail
sudo zfs get mountpoint fserver
sudo zfs unmount fserver
sudo zfs set mountpoint=/new/mount/point fserver
sudo zfs unmount fserver
```

### mount all filesystems
zfs mount -a

### destroy a pool
sudo zpool destroy POOL

### turn on auto expand ###
sudo zpool set autoexpand=on POOL

