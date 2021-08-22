# Getting Started with TMUX

Many of the options simply use (prefix), by default this is `Ctrl+b` (C-b). I tend to remap prefix to match the prefix in GNU screen to be `Ctrl+a` (C-a). 

Any keybinds marked with `[!]` are used specifically in my configuration and are not standard options

tmux uses the concepts of sessions, windows, and panes.
 * Sessions are a instance of tmux that contains windows/panes. An example of a session would be a terminal that is being used to run a backup job.
 * Windows are sub-units of management within tmux. Windows can be used to divide up different "screens". An example might be a window for performance monitoring
 * Panes are sub units of management within a tmux window. Panes can be split horizontal and vertically and allow you to see multiple terminals side-by-side in one window.

## Session Management
```bash
# Create a new session
tmux new -s session_name

# attaches to an existing named tmux session
tmux attach -t session_name

# attach to an existing session, creating if needed
tmux attach -t HTB || tmux new -s HTB

# detach the currently attached session
tmux detach (prefix + d)

# list existing tmux sessions
tmux list-sessions

# switch to an existing named session
tmux switch -t session_name

# rename session
tmux rename-session new-name ( prefix + $ )
```

## Working with Windows
Windows are displayed on the bottom bar. Your active window is marked with a asterisk. Each windows is also identified with a number and a name. `0:VPN`

```bash
# create a new window
tmux new-window ( prefix + c )

# renaming a window
tmux rename-window new-name ( prefix + , )

# move to the window based on index number
(prefix + 0-9)

# move to the next window
( prefix + n )

# move to the previous window
( prefix + p )
```


## Working with Panes
```
# vertical split
tmux split-window ( prefix + " )
[!] tmux split-window -h ( prefix + v )

# horizontal split
tmux split-window -h ( prefix + % ) ~~~ Remember to use shift ~~~
[!] tmux split-window -h ( prefix + s )

# Chaging active panes
(prefix) + <arrows>
[!] ALT + <arrows>

# resize windows
(prefix) hold control + <arrows>
[!] Control + <arrows>

# Move pane to left
( prefix + { )

# Move pane to right
( prefix + } )

# Convert pane to a window
( prefix + ! )

# Toggle zoom in/out
( prefix + z )
```

# Using Edit/Copy Mode
```bash
# Enter Edit mode
( prefix + [ )

# Enter Copy/Selection mode
<Space>

# Cancel Selection
<Esc>

# Yank to Buffer
<Enter>

# Paste from buffer
( prefix + ] )
```

# Getting Help
```
( prefix + ? )
```
