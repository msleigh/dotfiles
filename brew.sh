#!/usr/bin/env bash

# Install command-line tools using Homebrew.

# Make sure we’re using the latest Homebrew.
brew update

# Upgrade any already-installed formulae.
brew upgrade

# Save Homebrew’s installed location.
BREW_PREFIX=$(brew --prefix)

# Should be already installed (due to ~/Documents/setup)
brew install gh
brew install stow

# Install GNU core utilities (those that come with macOS are outdated).
# Don’t forget to add `$(brew --prefix coreutils)/libexec/gnubin` to `$PATH`.
brew install coreutils
#ln -s "${BREW_PREFIX}/bin/gsha256sum" "${BREW_PREFIX}/bin/sha256sum"

# Install some other useful utilities like `sponge`.
#brew install moreutils
# Install GNU `find`, `locate`, `updatedb`, and `xargs`, `g`-prefixed.
brew install findutils
# Install GNU `sed`, overwriting the built-in `sed`.
#brew install gnu-sed --with-default-names
# Install a modern version of Bash.
brew install bash
brew install bash-completion@2

# Switch to using brew-installed bash as default shell
if ! fgrep -q "${BREW_PREFIX}/bin/bash" /etc/shells; then
  echo "${BREW_PREFIX}/bin/bash" | sudo tee -a /etc/shells;
  chsh -s "${BREW_PREFIX}/bin/bash";
fi;

brew install ack
brew install actionlint
brew install borgbackup
brew install cloc
brew install fzf
brew install gcc
brew install git
brew install git-gui
brew install gitleaks
brew install gnu-sed
brew install graphviz
brew install grep
brew install gs
brew install jq
brew install lua
brew install node
brew install opencode
brew install pandoc
brew install parallel
brew install ripgrep
brew install shellcheck
brew install tmux
brew install tree
brew install uv
brew install vim
brew install xz
brew install zoom

brew install --cask anki
brew install --cask bitwarden
brew install --cask claude-code
brew install --cask codex
brew install --cask firefox
brew install --cask iterm2
brew install --cask jellyfin-media-player
brew install --cask musescore
brew install --cask obsidian
brew install --cask proton-drive
brew install --cask protonvpn
brew install --cask signal
brew install --cask spotify
brew install --cask vlc
brew install --cask zotero

# Remove outdated versions from the cellar.
brew cleanup
