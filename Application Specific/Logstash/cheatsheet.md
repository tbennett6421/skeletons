
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
jq "
```

## Track JVM performance, (Proc | Mem | GC)
```sh
watch -d -n1 "\
curl -s -XGET 'localhost:9600/_node/stats/jvm?pretty' | \
jq "

