
# Troubleshooting

## Show details of the running logstash instance
```sh
curl -s -XGET 'localhost:9600?pretty' | jq
```

## Watch the log entries
```sh
export LOG_DIR='/var/log/logstash'
tail -f "$LOG_DIR/logstash-plain.log"
```

# Performance Monitoring

## Track Events in/out of Logstash
```sh
watch -d -n1 "\
curl -s -XGET 'localhost:9600/_node/stats/events?pretty' | \
jq \
"
```

## Track JVM performance, (Proc | Mem | GC)
```sh
watch -d -n1 "\
curl -s -XGET 'localhost:9600/_node/stats/?pretty' | \
jq '{jvm,process,os}' \
"
```

## Track persisted queues
```sh
watch -d -n1 "\
curl -s -XGET 'localhost:9600/_node/stats/?pretty' | \
jq .pipelines[].queue \
"
```

## Track plugins inside all pipeline relating to grok
```sh
watch -d -n1 "\
curl -s -XGET 'localhost:9600/_node/stats/pipelines/?pretty' | \
jq .pipelines[].plugins[] | \
jq '.[]|select(.name==\"grok\")' \
"
```

## Track plugins inside a pipeline (apm) relating to stream
```sh
watch -d -n1 "\
curl -s -XGET 'localhost:9600/_node/stats/pipelines/apm/?pretty' | \
jq .pipelines[].plugins[] | \
jq '.[]|select(.name==\"stream\")' \
"
```
