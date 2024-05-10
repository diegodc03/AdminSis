#!/usr/bin/perl

#Aqui tenemos que cambiar los datos del usuario que quiera modificarlos

use strict;
use warnings;
use CGI;
use DBI;
use Linux::usermod;
use File::Copy;
use Quota;
use Email::Send::SMTP::Gmail;




#Declaramos las variables de la base de datos
my $root = "root";
my $pass = "";
my $host = "localhost";
my $db_name = "usuarios";

# Nos conectamos a la base de datos
my $db = DBI->connect("DBI:mysql:$db_name;host=$host", $root, $pass, { RaiseError => 1 });

#Hacemos la consulta
my $consulta = $db->prepare("SELECT COUNT(*) FROM usuarios WHERE username=?");

# Ejecutamos la consulta
$consulta->execute($username);

# Obtenemos el número de filas coincidentes
my ($num_filas) = $consulta->fetchrow_array;

# Verificamos si el usuario ya existe
if ($num_filas > 0) {
    print $q->header(-type => "text/html");
    print "<h3>El usuario ya existe</h3>";
} else {
    print $q->header(-type => "text/html");
    print "<h3>Usuario correcto, no existe en la base de datos</h3>";
}

$db->disconnect;