#!/usr/bib/perl


use strict;
use warnings;
use CGI;
use DBI;
use Linux::usermod;
use Crypt::Simple;

#Declaramos las variables de la base de datos
my $root = "adminBase";
my $pass = "123456";
my $host = "localhost";
my $db_name = "servidor";

# Nos conectamos a la base de datos
my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

#Tenemos que coger el user
my $consulta_cola = $db->prepare("SELECT * FROM cola_modificar_contrasenia");
$consulta_cola->execute;

#Hacemos un while hasta que se termine todo el select
# Recuperar y almacenar los datos en variables
my ($username, $passwd);
while (my @row = $consulta_cola->fetchrow_array) {
	$username = $row[0];
    $passwd = decrypt($row[1]);

    #Devuelve el usuario
#    my $user = Linux::usermod->users($username);
    my $user = Linux::usermod->new($username);
    $user->set('password', $passwd);


    #Eliminamos los valores de la base de datos
    $consulta_cola = $db->prepare("DELETE FROM cola_modificar_contrasenia where username = ?");
    $consulta_cola->execute($username);
}





    
