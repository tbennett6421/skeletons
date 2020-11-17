pid=1355
end=$((SECONDS+60))
echo -e '%CPU \t %MEM'
while [ $SECONDS -lt $end ]; do
	ps -p $pid --no-headers -o %cpu,%mem | awk 'BEGIN {OFS="\t";}{print "$1,$2;"}'
	sleep 6;
done
