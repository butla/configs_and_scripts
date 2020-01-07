alias vim='PYTHONPATH=$(pwd) vim'
alias r='ranger'
alias t='tmux -2'

alias gs='git status'
alias gl='git log -3 --graph'
alias gdf='git difftool --dir-diff'
alias gd='git diff'
alias gc='git checkout'
alias gco='git commit -a'
alias gm='git mergetool'
alias gp='git push'
alias gpl='git pull'

alias dk='docker-compose'

# thorough finding
alias fdd='fd --hidden --follow --exclude .git'
#
# find everything
alias fde='fd --hidden --follow --exclude .git --no-ignore'

alias my_ip='http ipinfo.io'
alias ag='ag --hidden --ignore .git -f'

alias pudbtest='pudb3 $(which pytest) -s'
alias pudbtest2='pudb $(which pytest) -s'

alias dockerclean='docker ps -aq | xargs docker rm'
alias dockercomposeup='docker-compose up --build; docker-compose down -v'
alias dockerports='docker ps --format "{{.Image}} >>> {{.Ports}}\n"'

alias plasmarestart='killall plasmashell && kstart plasmashell'
# restart bluetooth (and WiFi?) on bl laptop. Maybe should change the tlp setup?
alias bluetooth_restart_bl='sudo usb_modeswitch -R -v 8087 -p 0a2b'

alias subs='subliminal download -l en .'
alias subspl='subliminal download -l pl .'
