#!/usr/bin/perl


use strict;
use warnings;

use CGI;
#instalar este paquete
use CGI::Session;
use DBI;



#Crear un objeto CGI
my $cgi = CGI->new();

#Crear un objeto session
my $session = new::Session();

#Cargamos los datos de la sesión
$session->load();

#Creamos un array para guardar los datos de la sesión
my @auth = $session->param;


# Si no existen datos no habra
if (@auth eq 0){

    $session->delete();
    $session->flush();
    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
    print "<h3 style='color: red;'> No hay permisos para estar aqui, redireccionando";



}elsif($session->is_expired){

    $session->delete();
    $session->flush();
    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
    print "<h3 style='color: red;'> No hay permisos para estar aqui, redireccionando";



}else{

    print $cgi->header("text/html");
    print "<h3 style='color: red;'> Bienvenido a la pagina". $session->param("usuario") ."</h3>";
    print "<br><br>";
    print "<a href='exit.cgi'> Salir de la Aplicación </a>";


}