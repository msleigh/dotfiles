##################################################################
#  File: /usr/local/share/ecmwf/share/.bash_profile
#
# The following is intended to set ENVIRONMENT to BATCH when running
# a script from an interactive session - the intention is to
# stop the "rm -i" alias (& other aliases) from being set when
# running scripts

case $- in
	*i*) ENVIRONMENT=INTERACTIVE ;;
	*) ENVIRONMENT=BATCH ;;
esac

# Make sure we go through the shared bash/ksh setings
. ~/.profile

# Define use function if necessary
if [ -z "`typeset -f module`" ] && [ -f "/usr/local/share/use_dir/use_fn" ] 
then
. /usr/local/share/usbash_e_dir/use_fn
fi

# Define SHELL
SHELL=/bin/bash; export SHELL

# Define ECFS environment if it is not already set
if [ -z "`typeset -f ecd`" ]; then
	if [ -f /usr/local/ecfs/prodn/.ecfs_bash_env ]; then
		. /usr/local/ecfs/prodn/.ecfs_bash_env
	elif [ -f /usr/local/apps/ecfs/prodn/.ecfs_bash_env ]; then 
		. /usr/local/apps/ecfs/prodn/.ecfs_bash_env
	elif [ -f /usr/local/apps/ecfs/current/.ecfs_bash_env ]; then 
		. /usr/local/apps/ecfs/current/.ecfs_bash_env
	fi	
fi

# Aliases
if [ "$ENVIRONMENT" = "INTERACTIVE" ]
then
   alias l='ls -l'
   alias la='ls -al'
   alias rm='rm -i'
   export PS1="\u@\h:\w> "
fi

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# PATH is modified in .user_profile, which sources .path
for file in ~/.{path,bash_prompt,exports,aliases,functions,extra}; do
    [ -r "$file" ] && [ -f "$file" ] && source "$file";
done;
unset file;

# append to the history file, don't overwrite it
shopt -s histappend

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar
#
# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"
#
# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
#    alias ls='ls --color=auto'
#    #alias dir='dir --color=auto'
#    #alias vdir='vdir --color=auto'
#
#    alias grep='grep --color=auto'
#    alias fgrep='fgrep --color=auto'
#    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

# Set Python startup file location in PYTHONSTARTUP environment variable
#export PYTHONSTARTUP="${HOME}/.pythonrc.py"

# Over-ride default version of IFS Git tools with local checked-out development
# branch
#export PATH=${HOME}/ifs-git-tools/bin:${PATH}
#export MANPATH=${HOME}/ifs-git-tools/man:${MANPATH}

source ~rdx/git/ifs-git-tools-bash-completion
#source ~/ifs-git-tools/bin/ifs-git-tools-bash-completion

unset CDPATH

# Include timestamp in .bash_history and history command
export HISTTIMEFORMAT='%Y%m%d%H%M%S'

