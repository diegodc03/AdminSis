#!/usr/bin/perl

#Darse de baja en un servicio implica varios aspectos
    # Eliminar de la base de datos mariadb  --> es una consulta
    # Eliminar como usuario
    


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



use Passwd::Unix;

use MIME::Lite;

#Creamos un objeto CGI
my $cgi = new CGI;

my $session = new CGI::Session();

#Creamos un array para guardar los datos de la sesión
my @auth = $session->param;


# Si no existen datos se saldrá ya que el usuario no tiene sesión
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
    print "<h3 style='color: red;'> Su sesión ha caducado, volverá...";



}else{ #Perfecto todo


    # Añadir Usuario a cola_eliminar_usuario

    my $username = $session->param('username');
    my $email = $session->param('email');
    

    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "usuarios";

    # Nos conectamos a la base de datos
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });


    #Hacemos la consulta para añadir a la cola de eliminaciones
    my $consulta = $db->prepare("INSERT INTO cola_eliminar_usuarios (username, email) VALUES (?, ?)");
    $consulta->execute($username, $email);
    
    my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'servicioscondeydiego@gmail.com',
                                                 -pass=>'gyjn owfz lqlq htzv');

    my $message = "El usuario ha sido eliminado del servidor, esperemos que vuelva. Un saludo, los admins :) ";
 
    $mail->send(-to=>$email, -subject=>'Creacion de usuario', -body=>$message,
            -attachments=>'full_path_to_file');
 
    $mail->bye;


    $db->disconnect();


    $session->load();
    $session->delete();
    $session->fflush();
    

    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../index.html'>";
    


}






