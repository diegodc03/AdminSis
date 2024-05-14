#!/usr/bin/perl

use strict;
use CGI;
#instalar este paquete
use CGI::Session;
use DBI;


my $cgi = CGI->new;

# Obtenemos el usuario y la contraseña de inicio de sesión
my $usuario = $cgi->param("username");
my $password = $cgi->param("password");


#Filtrar Datos
if($usuario !~ /^[a-zA-Z0-9]+$/ or $password !~ /^[a-zA-Z0-9]+$/){
    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
    print "<h3>Los tipos de datos introducidos no son correctos</h3>";
}
else{
    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "usuarios";

    # Nos conectamos a la base de datos
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

    my $consulta = $mysql->prepare("SELECT * FROM usuario WHERE usuario= ? AND password = ?");
    $consulta->execute($usuario, $password);

    my $encontrar = 0;

    while($consulta->fetch()){
        $encontrar = 1;
    }

    #Usuario Entocontrado
        #Creamos la ssesion
    if($encontrar == 1){
        my $session = new CGI::Session;

        $session->save_param($cgi);
        $session->expires("10h");
        $session->flush();

        print $session->header(-location => "privado.cgi");
        system("logger -p local6.info 'Inicio de sision existoso'");

    }
    else{
        system("logger -p local6.info 'Inicio de sision fallido'");
        print $cgi->header("text/html");
        print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
        print "<h3>Los tipos de datos introducidos no son correctos...</h3>";
    }

    $mysql->disconnect();
}
