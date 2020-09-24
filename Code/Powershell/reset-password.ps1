$ID = (Read-Host -Prompt "Provide SAMAcountName: ") 
$CurPassword = (Read-Host -Prompt "Provide Current Password" -AsSecureString)
$NewPassword = (Read-Host -Prompt "Provide New Password" -AsSecureString)
Set-ADAccountPassword -Identity $ID -OldPassword $CurPassword -NewPassword $NewPassword
