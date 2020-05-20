# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bin:$HOME/.local/bin:/snap/bin:$HOME/.local/lib/node_modules/bin:$HOME/.cargo/bin:$HOME/go/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/home/butla/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="bira"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in ~/.oh-my-zsh/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to automatically update without prompting.
# DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS=true

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
HIST_STAMPS="yyyy-mm-dd"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  git
  git-auto-fetch
  # TODO have something like globalias but that expands only after enter
  # and use it only when tutoring or presenting
  virtualenv
  docker
  docker-compose
  timer
)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

export EDITOR='vim'

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

# My stuff
# =======================================

# enable vim mode
bindkey -v

# normal delete and backspace with VIM mode
bindkey "^D" delete-char-or-list
bindkey "^?" backward-delete-char

# fzf for shell history
source ~/.local/share/nvim/plugged/fzf/shell/key-bindings.zsh

# bind cd with fzf to crtl+k in addition to esc+c (described as alt+c)
bindkey '^K' fzf-cd-widget

# TODO show current vim mode indicator

# virtualenvwrapper setup
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/development
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3

if which python3.8 > /dev/null; then
    export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='-p python3.8'
else
    export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='-p python3.7'
fi

# make python scripts use ipdb by default when debugging
export PYTHONBREAKPOINT=ipdb.set_trace

source $(which virtualenvwrapper.sh)

source ~/.config/zsh/aliases.zsh
source ~/.config/zsh/functions.zsh

# https://github.com/rupa/z
source ~/bin/z.sh

# fd configuration, mainly so that FZF works more to my liking
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'

# if less than one screen worth of output, just print it on stdout
# Without this Git on ZSH was trying to put everything through a pager.
export PAGER="less -F -X"

# TODO remove after alacritty fix? https://github.com/jwilm/alacritty/issues/2515
# Needed to make apps start in the foreground
unset DESKTOP_STARTUP_ID
