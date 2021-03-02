alias vim='PYTHONPATH=$(pwd) vim'
alias r='ranger'
alias t='tmux -2'
alias vv='tmux_ide_panel'

# quick adding of untracked or changed files
alias ga='git add $(git ls-files --modified --others --exclude-standard | fzf) && git status'
alias gcf='git checkout -- $(git ls-files --modified --others --exclude-standard | fzf) && git status'
alias gs='git status'
alias gl='git log -3 --graph'
alias gdf='git difftool --dir-diff'
alias gd='git diff'
# can't have the status and needs to be an alias, so that I get completions for branches :(
alias gc='git checkout'
alias gco='git commit -a'
alias gm='git mergetool && echo ----------- && git status'
alias gpl='git pull'
alias gf='git fetch && echo ----------- && git status'
alias gr='git rebase -i'
# rebase the commits on the current branch
alias grb='git rebase -i $(git merge-base HEAD origin/master) && echo ----------- && git status'
# show the changes made on the current branch
alias gdfb='git difftool --dir-diff $(git merge-base HEAD origin/master)'
# show the log of the current branch
alias glb='git log $(git merge-base HEAD origin/master)..HEAD'
alias gclean='git reset --hard && git clean -f && echo ----------- && git status'

alias d='docker'
alias dk='docker-compose'

# get free disk space without the trash output from Snap
alias dff='df -h | grep -v "/snap"'
# get bulk devices without the trash output from Snap
alias lsblkk='lsblk | grep -v "/snap"'

# thorough finding
alias fdd='fd --hidden --follow --exclude .git'
#
# find everything
alias fde='fd --hidden --follow --exclude .git --no-ignore'

# find and edit file
alias fv='vim $(fd --hidden --follow --exclude .git --no-ignore | fzf)'

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

# Create a safe password in Python and copy it into the clipboard.
# Good for fast generation of passwords.
alias getpass='python -c "import secrets; print(secrets.token_urlsafe());" | xclip -selection clipboard'

# Show the JSON from a file in terminal. Does the nice render.
alias jsonv='python -m json.tool'
