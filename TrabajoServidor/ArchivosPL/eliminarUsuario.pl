#!/usr/bin/perl

# Script to delete an user in Linux (debian 12)

#Author:    Diego de Castro Merillas    [diegodecatro@usal.es]

# We are going to use Cpan, USERMOD.
 
# First, if we have not downloaded the usermod library...
# sudo apt install cpanminus
# cpanm install Linux::usermod

use strict;
use warnings;
use POSIX;
use Linux::usermod;
use File::Path qw(rmtree);
use CGI;
use DBI;

#my $cgi = new CGI;


#Declaramos las variables de la base de datos
	my $root = "adminBase";
	my $pass = "123456";
	my $host = "localhost";
	my $db_name = "servidor";

	# Nos conectamos a la base de datos
	my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

    
	# Recuperar datos de la cola de usuarios
    my $consulta_cola = $db->prepare("SELECT * FROM cola_eliminar_usuarios");
    $consulta_cola->execute;

	my %groups = Linux::usermod->grps();
    #Aqui tendremos una base de datos en la cual sera cola_eliminar_usuarios
    while (my @fila = $consulta_cola->fetchrow_array) {
        
	
	my $username = $fila[0];
        
	
       # Eliminaciómn del usuario Linux
        Linux::usermod->del($username);
        my $dir = "/home/".$username;

        # Eliminación del grupo asociado al usuario
        Linux::usermod->grpdel($username) if exists $groups{$username};
        rmtree($dir) or die "Couldn't delete $dir: $!";

        my $consulta_eliminar =  $db->prepare("DELETE FROM cola_eliminar_usuarios where username = ?");
        $consulta_eliminar->execute($username);

       # print $cgi->header("text/html");
       # print "<h3>Se ha eliminado el usuario</h3>";
       # print "<meta http-equiv='refresh' content='3; ../index.html'>";
}


    
