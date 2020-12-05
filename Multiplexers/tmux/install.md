## Install tmux
```bash
sudo apt-get install tmux
```

## Install tpm
```bash
# clone tpm into plugins
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```
## Install tmux configs
```bash
# Fetch tmux config
wget https://raw.githubusercontent.com/tbennett6421/skeletons/master/Multiplexers/tmux/tmux.conf -O ~/.tmux.conf

# Fetch tpm config
wget https://raw.githubusercontent.com/tbennett6421/skeletons/master/Multiplexers/tmux/tmux.pluginmanager -O ~/.tmux.pluginmanager
```

## Initialization of plugins
```bash
# run tmux
tmux 

# reload tmux config, only needed if tmux was not running
tmux source ~/.tmux.conf

# inside the tmux session, install plugins

# prefix + I 
# or
# F11 + shift + i
# or 
# C-a + shift + i
# or 
# C-b + shift + i

```
