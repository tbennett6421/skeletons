## Dump Java procs
pgrep -f java > pids.txt

## Dump all java procs environment
while IFS="" read -r p || [ -n "$p" ]
do
  cat /proc/$p/environ | tr '\0' '\n' | tee $p.env
done < pids.txt
