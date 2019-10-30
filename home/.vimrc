" Vundle setup
set nocompatible              " required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" code completions
Plugin 'Valloric/YouCompleteMe'
" async linting and syntax checking
Plugin 'w0rp/ale'
" text searching
Plugin 'mileszs/ack.vim'
" auto-close brackets, quotes, code structures, etc.
Plugin 'Raimondi/delimitMate'
Plugin 'tpope/vim-endwise'
" fast jumping around the visible text
Plugin 'easymotion/vim-easymotion'
" fuzzy file search
Plugin 'junegunn/fzf'
Plugin 'junegunn/fzf.vim'
Plugin 'flazz/vim-colorschemes'
Plugin 'junegunn/rainbow_parentheses.vim'
" close HTML tags
Plugin 'alvan/vim-closetag'
" commenting out
Plugin 'tpope/vim-commentary'
Plugin 'tpope/vim-fugitive'

" neovim-only plugins
Plugin 'numirias/semshi'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required


" My settings follow
if &term =~ '^screen'
    " tmux will send xterm-style keys when its xterm-keys option is on
    execute "set <xUp>=\e[1;*A"
    execute "set <xDown>=\e[1;*B"
    execute "set <xRight>=\e[1;*C"
    execute "set <xLeft>=\e[1;*D"
endif

set rtp+=~/bin/fzf

set expandtab
set tabstop=4
set shiftwidth=4

" TODO (doesn't work yet) don't fold anything in files by default
set foldlevelstart=10

" working with the system clipboard (requires vim-gtk3)
set clipboard=unnamedplus

" Markdown syntax highlighting
autocmd BufNewFile,BufFilePre,BufRead *.md set filetype=markdown

" Bash syntax highlighting
autocmd BufNewFile,BufFilePre,BufRead .bash_functions set filetype=sh

" YML editing options
autocmd FileType yaml setlocal tabstop=2 softtabstop=2 shiftwidth=2

" Terraform editing options
autocmd BufNewFile,BufFilePre,BufRead *.tfvars set filetype=tf
autocmd FileType tf setlocal tabstop=2 softtabstop=2 shiftwidth=2

" SQL editing options
autocmd FileType sql setlocal tabstop=2 softtabstop=2 shiftwidth=2

" HTML/CSS editing options
autocmd FileType css,html* setlocal tabstop=2 softtabstop=2 shiftwidth=2
" prevent delimitMate from closing tags by not using <>, so that vim-closetag can do it's job
" TODO not working
autocmd FileType html let b:delimitMate_matchpairs = "(:),[:],{:}"

set ignorecase
set hlsearch
set incsearch
set smartcase
set number
set relativenumber
set nowrap

" showing whitespace
set listchars=trail:¬,tab:>-,extends:>,precedes:<
set list

" buffers are hidden, not closed when switching to a different one; preserves undo history
set hidden

" show commands as they are being typed
set showcmd

" always display the status line
set laststatus=2

colorscheme darcula
syntax enable

" disable background color settings, so it can be transparent
highlight Normal guibg=NONE ctermbg=NONE

" Coloring syntax on long lines was slow in Vim, though it seems to be better in NeoVim.
" This limits the number of columns to be colored.
" set synmaxcol=200

" spell-checking
set spell spelllang=en_us
set spellfile=~/.vim/en.utf-8.add

" Unbind space from doing anything in normal mode, make it the leader key.
noremap <Space> <NOP>
let mapleader = " "

"bind J and K to moving around
nmap J 30j
nmap K 30k
vmap J 30j
vmap K 30k

" TODO bind a shortcut to type :%s:<CURSOR>:gc so that I can search and replace faster

" jumping around method level code blocks with a nicer binding
nmap <leader>[ [m
nmap <leader>] ]m

" code analysis and refactoring
nnoremap <leader>d :YcmCompleter GoToDefinition<CR>
nnoremap <leader>c :YcmCompleter GetDoc<CR>
nnoremap <leader>r :YcmCompleter GoToReferences<CR>
nnoremap <leader>R :Semshi rename<CR>

" jumping around the quickfix list
nnoremap <leader>j :cn<CR>
nnoremap <leader>k :cp<CR>

" jumping around the location list
nnoremap <leader>J :lnext<CR>
nnoremap <leader>K :lprev<CR>

" keybindings for fuzzy file finding
nnoremap <leader>. :FZF<CR>
nnoremap <leader>, :Buffers<CR>
nnoremap ? :Ag<CR>

" useful keybindings for basic operations
nnoremap <leader>q :bd<CR>
nnoremap <leader>s :w<CR>

" easymotion configuration, only explicit mappings
let g:EasyMotion_do_mapping=0
map <leader>w <Plug>(easymotion-w)
map <leader>W <Plug>(easymotion-W)
map <leader>b <Plug>(easymotion-b)
map <leader>B <Plug>(easymotion-B)

" put in the current timestamp with ctrl+t
" TODO make it work! (works only in instert mode right now!)
noremap <leader>t :put=strftime("%c")<CR>

" Useful when you want to paste one thing over a couple of things without Vim
" replacing the default register after the initial replace.
vnoremap <leader>p "0p

" Search for occurrences of a word in code files.
nnoremap <leader>f :execute "Ack " . expand("<cword>")<CR>

" Search for occurrences of a word in python files, don't jump to first found immediately (j), but
" open the quickfix list (cw).
" Should use that when YouCompleteMe fails to find references.
nnoremap <leader>F :execute "vimgrep /" . expand("<cword>") . "/j **/*.py"<Bar>cw<CR>

" making YouCompleteMe work nicely with virtualenv
let g:ycm_python_binary_path = 'python'

" automatically close the doc preview window after completion
let g:ycm_autoclose_preview_window_after_completion = 1

" ack.vim should use silver searcher under the hood
" It will search in hidden files, but will ignore git stuff
let g:ackprg = 'ag --vimgrep --hidden --ignore .git'

" ALE configuration
" TODO if the file is a test file, see if there's .pylintrc-test. Use ale_pattern_options for that?
" Set the linter depending on what's available in the current environment.
for linter in ['pylint', 'flake8', 'pycodestyle']
    if system("python3 -c 'import " . linter . "'") == ""
        let g:ale_linters = { 'python': [linter] }
        break
    endif
endfor

let g:ale_lint_on_text_changed = 'never'

" Rainbow parentheses config
let g:rainbow#pairs = [['(', ')'], ['[', ']']]
au VimEnter * RainbowParentheses
