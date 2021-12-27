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
`zcat conn.*.gz | cut -f3- | egrep '^x.x.x.x.x' | cut -f3 | sort | uniq -c | sort -n`

## Given a bad src->dst ip, extract zeek conn data and print unqiue src_ports ascending
`zcat conn.*.gz | cut -f3- | egrep '^10.224.110.133' | grep 10.47.6.58 | cut -f2 | sort | uniq -c | sort -n`

## Given a bad src->dst ip, extract zeek conn data and print unqiue dst_ports ascending
`zcat conn.*.gz | cut -f3- | egrep '^10.224.110.133' | grep 10.47.6.58 | cut -f4 | sort | uniq -c | sort -n`

# dns.log

## Extract zeek conn data via 4 tuple (src, sport, dst, dport)
`zcat dns.*.gz | cut -f3-6`

## Extract zeek conn data via 4 tuple + protocol
`zcat dns.*.gz | cut -f3-7`

## Extract zeek conn data via 4 tuple + protocol + query data
`zcat dns.*.gz | cut -f3-7,10,14,16,22,25`

# files.log

## Extract src,dst,proto,hashs,mime
`zcat files.*.gz | cut -f3-6,8-10,15,20-22`

# http.log

## Extract zeek conn data via 4 tuple (src, sport, dst, dport)
`zcat http.*.gz | cut -f3-6,8-11,`

## Extract conn,verb,uri
`zcat http.*.gz | cut -f3-6,8,10`

## Extract conn,verb,uri,ua
`zcat http.*.gz | cut -f3-6,8,10,13`

## Extract conn,verb,uri,status
`zcat http.*.gz | cut -f3-6,8,10,17,18`

## Extract conn,verb,uri,all
`zcat http.*.gz | cut -f3-6,8,10,13-`

## Extract conn,verb,uri,all
`zcat http.*.gz | cut -f3-6,8,10,13-`

## Given a bad src ip, get all the http urls visit
`zcat http.*.gz | cut -f3- | egrep '^10.164.94.120' | cut -f1-4,6,8`

## sort the user-agent strings ascending
`zcat http.*.gz | cut -f13 | awk '{ print length, $0 }' | sort -n | uniq -c`

## sort the user-agent strings by uniq count, showing length
`zcat http.*.gz | cut -f13 | awk '{ print length, $0 }' | sort -n | uniq -c | sort -n`

## Top talkers via POST
`zcat http.*.gz | grep POST | cut -f3,10 | cut -f1 | sort | uniq -c | sort -n`

# mysql.log

# ntp.log

# smtp.log

# ssl.log

# kerberos.log

# x509.log

# References

|Item|Link|
|---|---|
|conn.log|https://docs.zeek.org/en/master/scripts/base/protocols/conn/main.zeek.html|
|dns.log|https://docs.zeek.org/en/master/scripts/base/protocols/dns/main.zeek.html|
|files.log|https://docs.zeek.org/en/master/scripts/base/frameworks/files/main.zeek.html|
|http.log|https://docs.zeek.org/en/master/scripts/base/protocols/http/main.zeek.html|
|mysql.log|https://docs.zeek.org/en/master/scripts/base/protocols/mysql/main.zeek.html|
|ntp.log|https://docs.zeek.org/en/master/scripts/base/protocols/ntp/main.zeek.html|
|smtp.log|https://docs.zeek.org/en/master/scripts/base/protocols/smtp/main.zeek.html|
|ssl.log|https://docs.zeek.org/en/master/scripts/base/protocols/ssl/main.zeek.html|
|kerberos.log|https://docs.zeek.org/en/master/scripts/base/protocols/krb/main.zeek.html|
|x509.log|https://docs.zeek.org/en/master/scripts/base/files/x509/main.zeek.html|
