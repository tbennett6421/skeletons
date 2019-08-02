declare -i i=0
while IFS="" read -r p || [ -n "$p" ]
do
    if [ "$i" -eq "20" ] ; then
        for job in `jobs -p`; do wait ${job}; done
        i=0
    else
        nikto -host $p -output $p.xml &
        ((i++))
    fi
done < webservers.lst
