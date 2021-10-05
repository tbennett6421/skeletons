# Active Directory

## Locked out accounts
```ps
Search-ADAccount -LockedOut
```

## Getting groups a user is in
```ps
Get-ADPrincipalGroupMembership -Identity USER1 | Select-Object name
```

## Getting filtered groups a user is in
```ps
Get-ADPrincipalGroupMembership -Identity USER1 |Select-Object name | findstr /i hadoop
```

## Getting users in a security group
```ps
Get-ADGroupMember "SG_Example" -Recursive | Select-Object SAMAccountName | Sort-Object SAMAccountName
```

## Pulling users with an email address
```ps
Get-ADUser -Filter {EmailAddress -like "*@example.com"} -Properties * | Select Name, SamAccountName, EmailAddress
```

## Change password using Get-Credential
```ps
$old = Get-Credential
$new = Get-Credential
Set-ADAccountPassword -Identity USER1 -OldPassword $old.Password -NewPassword $new.Password
```

## Change password using CLI prompt
```
Set-ADAccountPassword -Identity USER1
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
