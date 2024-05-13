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

    # Eliminaciómn del usuario Linux
    Linux::usermod->del($username);

    my $dir = "/home/".$username;

    # Eliminación del grupo asociado al usuario
    Linux::usermod->grpdel($username) if exists $groups{$username};

    rmtree($dir) or die "Couldn't delete $dir: $!";



    # Eliminacion del usuario de la base de datos

    my $username = $session->param('username');
    my $email = $session->param('email');
    

    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "usuarios";

    # Nos conectamos a la base de datos
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

    #Hacemos la consulta
    #my $consulta = $db->prepare("SELECT COUNT(*) FROM usuarios WHERE username=?");
    my $consulta = $db->prepare("DELETE FROM usuarios where username=? and email=?");

    # Ejecutamos la consulta
    $consulta->execute($username, $email);
    $db->disconnect();

    

    #Enviar un email comunicando que el usuario ha sido correctamente dado de baja
    my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'upsauniversidaddevalladolid@gmail.com',
                                                 -pass=>'paol ulvc mcbo gxkx');


 
    $mail->send(-to=>$email, -subject=>'Usuario Eliminado', -body=>'Usted se ha dado de baja en el servicio Conde Y bermejo Soluciones',
            -attachments=>'full_path_to_file');
 
    $mail->bye;

   

    print $cgi->header("text/html");
    print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
    print "<h3>Se ha eliminado el usuario</h3>";


}










#En este punto habrá que tener una consulta de la base de datos

while (1) {

    print "This is the users list\n";
    
    setpwent();
    # Iterate over each entry in the passwd file
    while (my ($username, undef, $uid, $gid) = getpwent()) {
    # Check if the GID is greater than 1000
        if ($gid >= 1000 && $uid >= 1000 && $gid < 60000 && $uid < 60000) {
            print "$username $gid\n";
        }
    }
    endpwent();


    my $username;
    
    
    print "Enter the username to delete: ";
    
    $username = <STDIN>;
    chomp($username);

    if ($username eq "exit" ){
        exit();

    }else{
        Linux::usermod->del($username);
        
        my $dir = "/home/".$username;
        rmtree($dir) or die "Couldn't delete $dir: $!";
        #rmdir $dir or die "Couldn't delete $dir: $!";

    }

    print "User $username deleted\n";



    #Llamamos a la base de datos para que así pueda responder correctamente

    #LLamada a la base de dats
    



    #Aqui pon el correo que sea

    


}
