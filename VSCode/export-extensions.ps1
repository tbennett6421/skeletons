## Run the following in the vscode integrated console
$file = "extensions.txt"
New-Item -Path . -Name $file -ItemType "file" -Force
code --list-extensions | ForEach-Object { "code --install-extension $_" } >> $file
exit(0)
