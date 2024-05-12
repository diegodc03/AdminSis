#!/usr/bin/perl

#Modificación de la contraseña estando detro de la sesión



use strict;
use warnings;
use CGI;
use CGI::Session;
use DBI;
use Linux::usermod;
use File::Copy;
use Quota;
use Email::Send::SMTP::Gmail;


my $cgi = new CGI;
my $session = new CGI::Session();

#Tenemos los datos de la sesión actual
$session->load();

my $contrasenia1 = $session->param('contrasenia1');

my $contrasenia2 = $session->param('contrasenia2');

my $username = $session->param('username');
my $email = $session->param('email');

if($contrasenia1 ne $contrasenia2){
    print $cgi->header("text/html");
    print "<h3>Contraseñas mal escritas, será redireccionado en tres segundos</h3>"; 
    print "<meta http-equiv='refresh' content='3; ../recuperacionContraseniasSesion.html'>";
    
}else{

    #Contraseñas iguales, podemos cambiar la contraseña del usuario
    #Añadir a la base de datos

    #Declaramos las variables de la base de datos
    my $root = "root";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "usuarios";

    # Nos conectamos a la base de datos
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

    #Hacemos la consulta
    my $consulta = $db->prepare("SELECT COUNT(*) FROM usuarios WHERE username=?");

    # Ejecutamos la consulta
    $consulta->execute($username);

    # Obtenemos el número de filas coincidentes
    my ($num_filas) = $consulta->fetchrow_array;

    # Verificamos si el usuario ya existe
    if ($num_filas > 0) {
        #El usuario existe, redireccionamos al registro
        
        print $cgi->header(-type => "text/html");
        print "<h3>El usuario ya existe</h3>";
        print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
        $db->disconnect;

    } else {
        

        # Preparar y ejecutar la consulta SQL para actualizar la contraseña
        my $sql = "UPDATE usuarios SET password = ? where username = ? and email = ?";  # Ajusta el nombre del campo si es diferente
        my $sth = $db->prepare($sql);
        $sth->execute($contrasenia1, $username, $email);

        # Desconectar la base de datos
        $db->disconnect();

        if ($sth->err()) {
            print $cgi->header(-type => "text/html");
            print "<h3>Error al actualizar la contraseña: " . $sth->errstr() . "</h3>";
            print "<meta http-equiv='refresh' content='3; ../privado.html'>";
        } else {
            print $cgi->header(-type => "text/html");
            print "<h3>Contraseña actualizada</h3>";
            print "<meta http-equiv='refresh' content='3; ../privado.html'>";
        }
    }
}




