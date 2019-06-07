## Process so far
### Ansible host
1. install python
    * `apt-get install python3 python3-pip ipython3 build-essential python-dev python3-dev`
2. install ansible
    * `apt-get install ansible`
3. install requirements
    * `pip install -r requirements.txt`
4. configure a basic inventory file (see the samples)

### Windows targets
1. Install Windows Server 2012 R2
2. Create firewall rules to allow WinRM inbound.
    * `New-NetFirewallRule -DisplayName "Allow WinRM" -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow`
    * `New-NetFirewallRule -DisplayName "Allow WinRM(S)" -Direction Inbound -Protocol TCP -LocalPort 5986 -Action Allow`
3. Install .NET 4.0+
    * `Install-WindowsFeature -Name AS-NET-Framework`
4. Run the winrm provisioning script
    * `powershell.exe -exec bypass -Command "IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1');`
5. Test the connection
    * `ansible "all" -m win_ping -i win_hosts`
