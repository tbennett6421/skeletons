function Get-Time { return $(get-date | foreach { $_.ToLongTimeString() } ) }

function prompt
{
	$width = ($Host.UI.RawUI.WindowSize.Width - 2 - $(Get-Location).ToString().Length)
	$hr = New-Object System.String @('-',$width)
	Write-Host -ForegroundColor Red $(Get-Location) $hr
    # Write the time 
    write-host "[" -noNewLine
    write-host $(Get-Time) -foreground yellow -noNewLine
    write-host "] " -noNewLine
    # Write the path
    write-host $($(Get-Location).Path.replace($home,"~").replace("\","/")) -foreground green -noNewLine
    write-host $(if ($nestedpromptlevel -ge 1) { '>>' }) -noNewLine
    return "> "
}

function Get-LastExecutionTime
{
	$command = Get-History -Count 1  
	$command.EndExecutionTime - $command.StartExecutionTime
}

function count
{
    BEGIN { $x = 0 }
    PROCESS { $x += 1 }
    END { $x }
}

function product
{
    BEGIN { $x = 1 }
    PROCESS { $x *= $_ }
    END { $x }
}

function sum
{
    BEGIN { $x = 0 }
    PROCESS { $x += $_ }
    END { $x }
}

function average
{
    BEGIN { $max = 0; $curr = 0 }
    PROCESS { $max += $_; $curr += 1 }
    END { $max / $curr }
}

function ll
{
    param ($dir = ".", $all = $false) 

    $origFg = $host.ui.rawui.foregroundColor 
    if ( $all ) { $toList = ls -force $dir }
    else { $toList = ls $dir }

    foreach ($Item in $toList)  
    { 
        Switch ($Item.Extension)  
        { 
            ".Exe" {$host.ui.rawui.foregroundColor = "Yellow"} 
            ".cmd" {$host.ui.rawui.foregroundColor = "Red"} 
            ".msh" {$host.ui.rawui.foregroundColor = "Red"} 
            ".vbs" {$host.ui.rawui.foregroundColor = "Red"} 
            ".csv" {$host.ui.rawui.foregroundColor = "Cyan"} 
            ".docx" {$host.ui.rawui.foregroundColor = "Cyan"} 
            ".doc" {$host.ui.rawui.foregroundColor = "Cyan"} 			
            ".pdf" {$host.ui.rawui.foregroundColor = "Cyan"} 						
            Default {$host.ui.rawui.foregroundColor = $origFg} 
        } 
        if ($item.Mode.StartsWith("d")) {$host.ui.rawui.foregroundColor = "Green"}
        $item 
    }  
    $host.ui.rawui.foregroundColor = $origFg 
}

function lla
{
    param ( $dir=".")
    ll $dir $true
}

filter grep ( $reg )
{
    if ($_.tostring() -match $reg)
        { $_ }
}

# behave like a grep command
# but work on objects, used
# to be still be allowed to use grep
filter match( $reg )
{
    if ($_.tostring() -match $reg)
        { $_ }
}

# behave like a grep -v command
# but work on objects
filter exclude( $reg )
{
    if (-not ($_.tostring() -match $reg))
        { $_ }
}

# behave like match but use only -like
filter like( $glob )
{
    if ($_.toString() -like $glob)
        { $_ }
}

filter unlike( $glob )
{
    if (-not ($_.tostring() -like $glob))
        { $_ }
}

filter FileSizeBelow($size){if($_.length -le $size){ $_ }}
filter FileSizeAbove($size){if($_.Length -ge $size){$_}}
