New-NetFirewallRule -DisplayName "Enable WinRM" -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow
New-NetFirewallRule -DisplayName "Enable WinRM(S)" -Direction Inbound -Protocol TCP -LocalPort 5986 -Action Allow
Install-WindowsFeature -Name AS-NET-Framework
