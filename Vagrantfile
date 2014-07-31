# -*- mode: ruby -*-
# vi: set ft=ruby :

MOUNT_POINT = '/home/vagrant/whats-fresh'

box_ver = "20140121"
box_url = "http://vagrant.osuosl.org/centos-6-#{box_ver}.box"

Vagrant.configure("2") do |config|
  config.vm.hostname = "project-fish"
  config.vm.box       = "centos-6-#{box_ver}"
  config.vm.box_url   = "#{box_url}"

  config.vm.network :private_network, ip: "33.33.33.50", adapter: 2

  config.berkshelf.berksfile_path = "chef/Berksfile"
  config.berkshelf.enabled = true
  config.omnibus.chef_version = "11.12.4"

  # Symlink our project for development purposes
  config.vm.synced_folder ".", MOUNT_POINT

  config.vm.provision :chef_solo do |chef|
    chef.run_list = [
        "recipe[whats-fresh::default]"
    ]
  end
end
