# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/bionic64"

  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.ssh.forward_agent = true
  config.vm.hostname = "xwordsvm"
  config.vm.define "xwords-vagrant" do |v|
  end

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
    vb.name = "xwords-vagrant"
    vb.memory = 2048 # the default of 512 gives us a OOM during setup.
  end
  config.vm.network :private_network, ip: '192.168.50.50'

  config.vm.synced_folder ".", "/home/vagrant/xwords"

  config.vm.provision "shell", path: "config/vagrant/provision_vagrant.sh"
  config.vm.provision "docker" do |d|
    d.run "redis", image: "redis:5", args: "-p 6379:6379", daemonize: true
  end
  config.ssh.username = "vagrant"

end
