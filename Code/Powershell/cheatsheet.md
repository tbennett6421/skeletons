# Active Directory

## Users

### Locked out accounts
```ps
Search-ADAccount -LockedOut
```

### Getting everything for a user account
```ps1
Get-ADUser USER1 -Properties *
```

### Getting latest epoch time for user in forest
```ps
# LastLogon and BadPasswordTime are not replicated, collect this from all DCs and take the highest value

$sites = @("ATL","NYC")
$dcs = Get-ADDomainController -Filter * | where {$sites -contains $_.site}
$userObj = Get-ADuser USER1

$a = @()
$prop = "LastLogon"
ForEach ($dc in $dcs)
{
    $a += Get-ADuser $userObj -server $dc.hostname -Pr $prop | Select-Object $prop
}
$a = $a.$prop | Where {$_ -ne $null} | Sort-Object -Descending | Select-Object -Unique -First 1
$lastTS = [datetime]::FromFileTime($a)

$a = @()
$prop = "BadPasswordTime"
ForEach ($dc in $dcs)
{
    $a += Get-ADuser $userObj -server $dc.hostname -Pr $prop | Select-Object $prop
}
$a = $a.$prop | Where {$_ -ne $null} | Sort-Object -Descending | Select-Object -Unique -First 1
$BadTS = [datetime]::FromFileTime($a)

Write-Host "LastLogon : $lastTS"
Write-Host "BadPasswordTime : $BadTS"
```

## Groups

### Getting groups a user is in
```ps
Get-ADPrincipalGroupMembership -Identity USER1 | Select-Object name
```

### Getting filtered groups a user is in
```ps
Get-ADPrincipalGroupMembership -Identity USER1 |Select-Object name | findstr /i hadoop
```

### Getting users in a security group
```ps
Get-ADGroupMember "SG_Example" -Recursive | Select-Object SAMAccountName | Sort-Object SAMAccountName
```

## Domains

### Get sites in forest
```ps
Get-ADForest | select-object -ExpandProperty Sites
```

### Getting all domain controllers
```ps
$dcs = Get-ADDomainController -filter * | Select-Object name
```

### Getting subset of domain controllers
```ps
# Only search Atlanta and New-York City
$sites = @("ATL","NYC")
$dcs = Get-ADDomainController -Filter * | where {$sites -contains $_.site}

# Results that are not prod
$deny = @("PRD")
$dcs = Get-ADDomainController -Filter * | where {$_.site -ne $deny}
```

## Passwords

### Change password using Get-Credential
```ps
$old = Get-Credential
$new = Get-Credential
Set-ADAccountPassword -Identity USER1 -OldPassword $old.Password -NewPassword $new.Password
```

## Change password using CLI prompt
```
Set-ADAccountPassword -Identity USER1
```

## Pulling users with an email address
```ps
Get-ADUser -Filter {EmailAddress -like "*@example.com"} -Properties * | Select Name, SamAccountName, EmailAddress
```

# Updating Sysmon on remote hosts
```ps
foreach ($host in $hosts) {
    $remotehost = $host + '.' + $domain
    write-output "Doing $remotehost"
    $channel = New-PSSession $remotehost
    Copy-Item -ToSession $channel $sourceFile -Destination $remoteFile

    Invoke-Command -ComputerName $remotehost -ScriptBlock { C:\Windows\Sysmon64.exe -c $Using:remoteFile 2>&1 | %{ "$_" }}
    Invoke-Command -ComputerName $remotehost -ScriptBlock { net stop sysmon64 }
    Invoke-Command -ComputerName $remotehost -ScriptBlock { net start sysmon64 }
}
```
