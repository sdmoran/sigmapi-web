# -*- mode: ruby -*-
# vi: set ft=ruby :

["vagrant-vbguest"].each do |plugin|

  if not Vagrant.has_plugin?(plugin)
    raise "#{plugin} is required. Please run `vagrant plugin install #{plugin}`"
  end
end

Vagrant.configure("2") do |config|
  config.vm.box = "bento/centos-7.3"
  config.vm.network :forwarded_port, guest:8000, host:8000
  config.vm.provision :shell, :path => "scripts/install.sh"
end
