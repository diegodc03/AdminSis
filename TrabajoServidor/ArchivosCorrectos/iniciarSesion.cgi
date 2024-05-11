#!/usr/bin/perl

use strict;
use CGI;
#instalar este paquete
use CGI::Session;
use DBI;


my $cgi = CGI->new;

my $usuario = $cgi->param("username", $cgi->param("usuario"));
my $password = $cgi->param("password", $cgi->param("password"));

#Filtrar Datos
if($usuario !~ /^[a-zA-Z0-9]+$/ or $password !~ /^[a-zA-Z0-9]+$/){
    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
    print "<h3>Los tipos de datos introducidos no son correctos</h3>";
}
else{
    my $root = "root";
    my $pass = "diegoCarlos123diego123";
    my $host = "localhost";
    my $db = "servidor";

    my $mysql = DBI->connect("DBI:mysql:$db;host=$host",$root, $pass); 

    #Preparamos la consulta
    my $consulta = $mysql->prepare("SELECT * FROM usuario WHERE usuario='$usuario" AND password='$password');

    #Ejecutar la consulta
    $consulta->execute();

    my $encontrar = 0;

    while($consulta->fetch()){
        $encontrar = 1;
    }

    #Usuario Entocontrado
        #Creamos la ssesion
    if($encontrar eq 1){
        my $session = new CGI::Session;

        $session->save_param($cgi);
        $session->expires("10h");
        $session->flush();

        print $session->header(-location => "privado.cgi");
        
    }
    else{

        print $cgi->header("text/html");
        print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
        print "<h3>Los tipos de datos introducidos no son correctos...</h3>";

    }


    $mysql->disconnect();
}
