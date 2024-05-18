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
use CGI::Session;

my $cgi = CGI->new();

my $session = new CGI::Session();
$session->load();

#Creamos un array para guardar los datos de la sesión --> Con esto tenemos los parámetros del usuario
my @auth = $session->param;



# Si no existen datos se saldrá ya que el usuario no tiene sesión
if (@auth eq 0){

    $session->delete();
    $session->flush();
    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
    print "<h3 style='color: red;'> Tiene que iniciar Sesión, redireccionando";



}elsif($session->is_expired){

    $session->delete();
    $session->flush();
    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
    print "<h3 style='color: red;'> Su sesión ha caducado, volverá...";



}else{ #Perfecto todo


     # Añadir Usuario a cola_eliminar_usuario

    my $username = $session->param("username");
    my $password = $session->param("password");		
 
    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "servidor";
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

	
    my $consulta = $db->prepare("INSERT INTO cola_eliminar_usuarios (username, password) VALUES (?, ?)");
    $consulta->execute($username,$password);
    
	
    $consulta = $db->prepare("SELECT email from usuarios where username=?");
    $consulta->execute($username);

    # Obtener el valor de la columna "email"
    my ($email) = $consulta->fetchrow_array;


    $consulta = $db->prepare("DELETE FROM usuarios where username=?");
    $consulta->execute($username);


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
    $session->flush();


    
    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../index.html'>";
    print "<h3 style='color: red;'> Esperemos que vuelva";


}
