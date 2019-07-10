use devops;
CREATE TABLE `servers` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `ip` varchar(50) NOT NULL,
  `port` int(11) NOT NULL,
  `user` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert into servers (name, ip, port, user) values( 'nginx', '127.0.0.1', 22, 'root' );

CREATE TABLE `user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert into user (username,password) values ('shijiange', md5('shijiangepwd'));


CREATE TABLE `deploy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `hosts_path` varchar(100) NOT NULL,
  `hosts_pattern` varchar(100) NOT NULL,
  `module` varchar(100) NOT NULL,
  `args` varchar(1000) NOT NULL,
  `forks` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert into deploy (name, hosts_path, hosts_pattern, module, args, forks) values ('deploy_nginx', '/etc/ansible/hosts', 'all', 'shell', 'ifconfig | grep eth0', 1);


CREATE TABLE `playbook` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `hosts_path` varchar(100) NOT NULL,
  `playbook_path` varchar(100) NOT NULL,
  `forks` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert into playbook (name, hosts_path, playbook_path, forks) values('deploy_nginx', '/etc/ansible/hosts', '/tmp/test.yml', 1);