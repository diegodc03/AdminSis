#!/usr/bin/perl

#Aqui tenemos que cambiar los datos del usuario que quiera modificarlos
#Va a venir de un forms, en el cual cogeremos los valores y los añadiremos

use CGI::Session;
use strict;
use warnings;
use CGI;
use DBI;
use Linux::usermod;
use File::Copy;
use Quota;
use Email::Send::SMTP::Gmail;

my $cgi = new CGI;
my $session = new CGI::Session;

$session->load();

my $usuarioInicioSesion = $session->param('username');

if($session->is_expired or !$usuarioInicioSesion){ 
	print $cgi->header("text/html");
        print "<meta http-equiv='refresh' content='3; ../login.html'>";
        print "<h3 style='color: red;'> No hay permisos para estar aqui, redireccionando";

}else{


    #Hacemos una consulta en la base de datos para tener los datos del usuario, por si hay que cambiar algo
    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "servidor";
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });


    my $consulta = $db->prepare("SELECT * FROM usuarios WHERE username=?");
    $consulta->execute($usuarioInicioSesion);
    my @fila = $consulta->fetchrow_array;
    
	my ($namedb, $secondnamedb, $emaildb, $postcodedb, $user_typedb);    
    if(@fila){

        $namedb = $fila[2];
        $secondnamedb = $fila[3];
        $emaildb = $fila[4];
        $postcodedb = $fila[5];
        $user_typedb = $fila[6];


    } else{ 
       #No existe el usuario
        print $cgi->header( -type => "text/html");
        print "<meta http-equiv='refresh' content='3; ../cgi-bin/privado.cgi'>";
        print "<h3>Usuario correcto, no existe en la base de datos</h3>";
    }

    

    #Parametros que pueden haberse elegido en la base de datos
    my $name = $cgi->param('name');
    my $secondname = $cgi->param('secondname');
    my $email = $cgi->param('email');
    my $postcode = $cgi->param('postcode');
    my $user_type = $cgi->param('user_type');

    print $cgi->header( -type => "text/html");
 

    	if(length($name) == 0){
        	$name = $namedb;
   	}
	
	if(length($secondname) == 0){
        	$secondname = $secondnamedb;
    	}
	
	if(length($email) == 0){
        	$email = $emaildb;
    	}
	
	if(length($postcode) == 0){
        $postcode = $postcodedb;
    	
	}if(length($user_type) == 0){
        	$user_type = $user_typedb;
    	}
	#}elsif($user_tpye ne $user_typedb){
		#Tengo que llamar a algo del sistema para cambiar el grupo asociado

	#}
 

	my $consultadb = $db->prepare("UPDATE usuarios SET name = ?, secondname = ?, email = ?, postcode = ?, user_type = ? WHERE username = ?");
	$consultadb->execute($name, $secondname, $email, $postcode, $user_type, $usuarioInicioSesion);
	
	$db->disconnect;

        print $cgi->header(-type => "text/html");
        print "<h3>El usuario se ha modificado</h3>";
        print "<meta http-equiv='refresh' content='3; ../cgi-bin/privado.cgi'>";
	

}
