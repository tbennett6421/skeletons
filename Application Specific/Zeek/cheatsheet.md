# conn.log

## Extract zeek conn data via 4 tuple (src, sport, dst, dport)
`zcat conn.*.gz | cut -f3-6`

## Extract zeek conn data via 4 tuple + protocol
`zcat conn.*.gz | cut -f3-7`

## Extract zeek conn data via 4 tuple + protocol + duration
`zcat conn.*.gz | cut -f3-7,9`

## Extract zeek conn data via 4 tuple + protocol + conn_state
`zcat conn.*.gz | cut -f3-7,12`

## Given GNU cut doesn't allow arbitary ordering of columns, we can use awk to print out how we wish
`zcat conn.*.gz | awk '{ print $7,$3,$5,$4,$6}'`

## top talkers ascending
`zcat conn.*.gz | cut -f3 | sort | uniq -c | sort -n`

## top destinations ascending
`zcat conn.*.gz | cut -f5 | sort | uniq -c | sort -n`

## Given a bad src ip, extract zeek conn data and print unqiue destinations ascending
`zcat conn.log.gz | cut -f3- | egrep '^x.x.x.x.x' | cut -f3 | sort | uniq -c | sort -n`

## Given a bad src->dst ip, extract zeek conn data and print unqiue src_ports ascending
`zcat conn.log.gz | cut -f3- | egrep '^10.224.110.133' | grep 10.47.6.58 | cut -f2 | sort | uniq -c | sort -n`

## Given a bad src->dst ip, extract zeek conn data and print unqiue dst_ports ascending
`zcat conn.log.gz | cut -f3- | egrep '^10.224.110.133' | grep 10.47.6.58 | cut -f4 | sort | uniq -c | sort -n`

# dns.log

# files.log

# http.log

# mysql.log

# ntp.log

# smtp.log

# ssl.log

# kerberos.log

# x509.log
