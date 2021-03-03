# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  
   config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
  # TODO: Install pyenv prerequisites
  # TODO: Install pyenv
   sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

  git clone https://github.com/pyenv/pyenv.git ~/.pyenv

  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
  echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
  source ~/.bash_profile
  pyenv install 3.8.5
  pyenv global 3.8.5
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

   SHELL

   
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
    # Install dependencies and launch
    cd /vagrant/todo_app
    poetry install
    poetry run flask run --host '0.0.0.0' 
    "}
    
   end

end
