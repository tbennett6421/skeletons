from datetime import datetime

csv = 'importantlist.csv'
email = 'demo@example.com'
username = email.split('@')[0]
local_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
utc_ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

reason = "You can't tell me what to do"

payload = (
    'exec_mode=oneshot&output_mode=json&search='
    '| inputlookup {csv}'
    '| append ['
        '| makeresults '
        '| eval username="{uid}" '
        '| eval email="{email}" '
        '| eval local_ts="{local_ts}" '
        '| eval utc_ts="{utc_ts}" '
        '| eval reason="{reason}" '
    ']'
    '| fields - _time | dedup akaname, username '
    '| outputlookup {csv}'
).format(
    csv=csv, username = username, email = email,
    local_ts=local_ts, utc_ts = utc_ts, reason = reason
)
