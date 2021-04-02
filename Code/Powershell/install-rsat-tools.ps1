# RSAT Install Error 0x800f0954 in Windows 10

# If you have Internet access on Windows 10 desktops, but when installing RSAT via Add-WindowsCapability or 
# DISM (DISM.exe /Online /add-capability /CapabilityName:Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0 .1.0), 
# you encounter the error 0x800f0954, most likely your computer is configured to update from the local WSUS 
# update server using Group Policy settings.

# To correctly install RSAT components in Windows 10 1809+, you can temporarily disable updating from the WSUS 
# server through the registry (open the registry key HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU 
# and change the UseWUServer to 0) and restart the Windows Update Service (wuauserv).

# You can use the following PowerShell script:

# Disable WSUS local policy
$currentWU = Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "UseWUServer" | select -ExpandProperty UseWUServer
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "UseWUServer" -Value 0
# Restart Service
Restart-Service wuauserv
# Install all RSAT tools
Get-WindowsCapability -Name RSAT* -Online | Add-WindowsCapability –Online
# Restore local policy
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "UseWUServer" -Value $currentWU
# Restart Service
Restart-Service wuauserv
