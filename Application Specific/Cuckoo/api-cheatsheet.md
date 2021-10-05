## Getting started

Quote all strings, to avoid issues with spaces or ampersands

Set remote host before running
```bash
host="cuckoo.mal"
port="8080"
proto="http"
export rhost="$proto://$host:$port"
```

## Viewing Tasks
```bash
# view all submitted tasks (from the beginning of time)
curl -vvv -XGET "$rhost/tasks/list"

# View last 5 submitted tasks
curl -vvv -XGET "$rhost/tasks/list?offset=-1&limit=5"
```

## Making submissions
```bash
# Submit a file to cuckoo for processing
curl -vvv -XPOST -F file=@"/root/evil.zip" "$rhost/tasks/create/file"

# Submit an url to cuckoo for processing
curl -vvv -XPOST -F url="https://google.com/" "$rhost/tasks/create/url"
```

# Geting data
```bash
# Get metadata from hash, if it exists
md5_hash="75bc7a4f547f6e0b54af3ee2461c8b86"
sha1_hash="f0fbaefb4643adf706cbc166ca960aee10d7f824"
sha256_hash= "1e02fb70b4870eda25d46e6f9d4f52b702d4aed0d98d670e2063dc521a17dd0b"
sha512_hash= "b95682c6534fb13490ec8972c7885d12c59ebb1ae9925969422d672c4c9a50153028de8f279a7f9c5285a8f78d3de6e21b126d40213bbc59ee6bec51c0b82aab"
curl -vvv -XGET "$rhost/files/view/md5/$md5_hash"
curl -vvv -XGET "$rhost/files/view/sha1/$sha1_hash"
curl -vvv -XGET "$rhost/files/view/sha256/$sha256_hash"
curl -vvv -XGET "$rhost/files/view/sha512/$sha512_hash"
 
# Get a file contents by SHA256 (ENSURE you write to a file as curl writes to STDOUT on connection)

curl -vvv -XGET "$rhost/files/get/$sha256_hash" -o "file.bad"
```


