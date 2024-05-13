#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use DBI;
use Linux::usermod;
use File::Copy;
use Quota;
use Email::Send::SMTP::Gmail;
use File::Path qw(make_path remove_tree);
use File::Copy::Recursive qw(dircopy);
use File::Finder;

my $cgi = new CGI;



my $username = "diego2";
#Creamos el usuario
my $password = "123456";

#we check if the username exists
if(getpwnam($username)){
	print "Usuario Existente";
}


#add home route
my $homeRoute = "/home/".$username."/";
#print "The home route is $homeRoute ";




# Creamos el nuevo usuario
	Linux::usermod->add($username, $password, undef, undef, undef, $homeRoute, "/bin/bash");
	my $user=Linux::usermod->new($username);
	Linux::usermod->grpadd($username, $user->get('gid'));
	my $usergroup = Linux::usermod->new($username, 1);

	my $uid = $user->get('uid');
	my $gid = $user->get('gid');



#Crear /home y copiar las cosas de /etc/skel
	make_path($homeRoute , { owner => $username, group => $username });
	dircopy("/etc/skel", $homeRoute);
    
	chown($uid, $gid, $homeRoute);  # Cambiar el propietario y grupo del directorio
    chown($uid, -1, "$homeRoute/*");  # Cambiar el propietario de los archivos dentro del directorio    
    chown(-1, $gid, "$homeRoute/*");  # Cambiar el grupo de los archivos dentro del directorio
    #chown($usergroup->get('uid'), $usergroup->get('gid'), File::Finder->in($homeRoute));
	#chown($usercreated->get('uid'), $usergroup->get('gid'), "$dirhome/public_html.no");	
	#chown($usercreated->get('uid'), $usergroup->get('gid'), "$dirhome/bienvenido.txt");



#Establecer las quotas para ese usuario en /home
	my $quotadev = Quota::getqcarg("/");
  	Quota::setqlim($quotadev, $uid, 61440, 81920, 0, 0);
