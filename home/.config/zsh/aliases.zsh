alias vim='PYTHONPATH=$(pwd) vim'
alias r='ranger'
alias t='tmux -2'
alias vv='tmux_ide_panel'

alias gs='git status'
alias gl='git log -3 --graph'
alias gdf='git difftool --dir-diff'
alias gd='git diff'
alias gc='git checkout'
alias gco='git commit -a'
alias gm='git mergetool'
alias gp='git push'
alias gpl='git pull'
alias gf='git fetch'
alias gr='git rebase -i'
# rebase the commits on the current branch
alias grb='git rebase -i $(git merge-base HEAD origin/master)'
# show the changes made on the current branch
alias gdfb='git difftool --dir-diff $(git merge-base HEAD origin/master)'
# show the log of the current branch
alias glb='git log $(git merge-base HEAD origin/master)..HEAD'

alias d='docker'
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
# Restart bluetooth devices on my machines.
# Looks like they are being put to sleep and not waking.
# Should maybe change the tlp setup, so they aren't put to sleep.
alias bluetooth_restart_bl='sudo usb_modeswitch -R -v 8087 -p 0a2b'
alias bluetooth_restart_b3='sudo usb_modeswitch -R -v 0cf3 -p e300'

alias subs='subliminal download -l en .'
alias subspl='subliminal download -l pl .'

# I like this as the default font
alias toilet='toilet -f mono9'
