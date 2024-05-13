#!/usr/bin/perl

#Aqui tenemos que cambiar los datos del usuario que quiera modificarlos
#Va a venir de un forms, en el cual cogeremos los valores y los añadiremos


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
my $session = new CGI::Session();

$session->load();

my $usuarioInicioSesion = $session->param('username');


if($session->is_expired or !$loggedUser){ 
	print $cgi->redirect("/webs/login.html");

}else{

    #Añadimos en cada variable, la modificación de los datos
    my $passwd = $q->param('password');
    my $name = $q->param('name');
    my $secondname = $q->param('secondname');
    my $email = $q->param('email');
    my $postcode = $q->param('postcode');


    if(length($passwd) == 0){
        my $contraseniaInicioSesion = $session->param('password');
        $passwd = $constraseniaInicioSesion;
    }elsif(length($name) == 0){
        my $nameInicioSesion = $session->param('name');
        $name = $nameInicioSesion;
    }elsif(length($secondname) == 0){
        my $secondNameInicioSesion = $session->param('secondname');
        $secondname = $secondNameInicioSesion;
    }elsif(length($email) == 0){
        my $emailInicioSesion = $session->param('email');
        $email = $emailInicioSesion;
    }elsif(length($postcode) == 0){
        my $postCodeInicioSesion = $session->param('postcode');
        $postcode = $postCodeInicioSesion;
    }

    #Comprobamos si son correctos los valores introducidos.
    if($usuario !~ /^[a-zA-Z0-9]+$/ or $password !~ /^[a-zA-Z0-9]+$/){
        print $cgi->header("text/html");
        print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
        print "<h3>Los tipos de datos introducidos no son correctos</h3>";      
    }

    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "usuarios";

    # Nos conectamos a la base de datos
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

    #Hacemos la consulta
    my $consulta = $db->prepare("SELECT COUNT(*) FROM usuarios WHERE username=? and email=?");

    # Ejecutamos la consulta
    $consulta->execute($username, $email);

    # Obtenemos el número de filas coincidentes
    my ($num_filas) = $consulta->fetchrow_array;

    # Verificamos si el usuario ya existe
    if ($num_filas > 0) {
        #Podemos cambiar los datos
        
        my $cosulta = $db->prepare("UPDATE usuario SET passwd = ?, name = ?, secondname = ?, email = ?, postcode = ? WHERE username = ?")

        $consulta->execute($passwd, $name, $secondname, $email, $postcode, $usuarioInicioSesion)
        
        $db->disconnect;

        print $q->header(-type => "text/html");
        print "<h3>El usuario se ha modificado</h3>";



    } else {
        #No existe el usuario
        print $q->header( -type => "text/html");
        print "<meta http-equiv='refresh' content='3; ../ZonaPrivada.html'>";
        print "<h3>Usuario correcto, no existe en la base de datos</h3>";
    }





}


