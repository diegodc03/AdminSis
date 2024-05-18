#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Session();
use DBI;
use CGI::Carp qw(fatalsToBrowser);
use File::Slurp;
use Linux::usermod;

my $cgi = CGI->new();

my $session = new CGI::Session;
$session->load();

#my $session = CGI::Session->load("id:md5", $cgi, {Directory=>"sessions"});
#my $loggedUser = $session->param("loggedUser");


#Creamos un array para guardar los datos de la sesión
my @auth = $session->param;

# Si no existen datos no habra
if (@auth eq 0){

    $session->delete();
    $session->flush();
    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../login.html'>";
    print "<h3 style='color: red;'> No hay permisos para estar aqui, redireccionando";



}elsif($session->is_expired){

    $session->delete();
    $session->flush();
    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../login.html'>";
    print "<h3 style='color: red;'> Su sesión ha caducado, redireccionando";



}else{

    print $cgi->header("text/html");
    print "<h3 style='color: red;'> Bienvenido a la pagina". $session->param("usuario") ."</h3>";
    print "<br><br>";
    print "<a href='eliminarUsuario.cgi'> Eliminar Usuario </a>";
    print "<br><br>";
    print "<a href='/nuevaContrasenia.html'> Cambiar Contraseña </a>";
    print "<br><br>";
    print "<a href='/modificacionDatos.html'> Modificar Valores </a>";
    print "<br><br>";
    print "<a href='salir.cgi'> Salir de la Aplicación </a>";


}



