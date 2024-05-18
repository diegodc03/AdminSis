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

my @auth = $session->param;
my $username = $session->param('username');

my $contrasenia1 = $cgi->param('contrasenia1');
my $contrasenia2 = $cgi->param('contrasenia2');


if($contrasenia1 ne $contrasenia2){
    print $cgi->header("text/html");
    print "<h3>Contraseñas mal escritas, será redireccionado en tres segundos</h3>";
    print "<meta http-equiv='refresh' content='3; ../index.html'>";

}elsif( length($contrasenia1) >= 8){
    print $cgi->header("text/html");
    print "<h3>Contraseña con menos de 8 caracteres</h3>";
    print "<meta http-equiv='refresh' content='3; ../index.html'>";

}else{
 
     my $mayus = 0;
     my $minus = 0;
     my $num = 0;
     my $comprobante = 0;

     #Recorremos el caracter con la contraseña
     foreach my $caracter (split //, $contrasenia1){
     if ($caracter =~ /[A-Z]/){
     	$mayus = 1;
     }elsif($caracter =~ /[a-z]/){
 	$minus = 1;
     }elsif($caracter =~ /\d/){
        $num = 1;
     }
}

                        # Verificar si se cumple al menos un requisito de cada tipo
                        if ($mayus != 1 or $minus != 1 or $num != 1) {
                        print $cgi->header(-type => "text/html");
                        print "La contraseña debe contener al menos una letra mayúscula, una letra minúscula y un número.";
                        print "<meta http-equiv='refresh' content='3; ../register.html'>";
                        exit;
                }

    




    #Contraseñas iguales, podemos cambiar la contraseña del usuario
    #Añadir a la base de datos

    #Declaramos las variables de la base de datos
    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "servidor";
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

    my $consulta;
    my $email;	
    
    #Comprubo en que estado estamos, si proviene de contraseña sin sesion o con sesion
    #Si proviene sin sesion se busca a partir del correo el username
    if(@auth eq 0){
	$email = $cgi->param('email');
	$consulta = $db->prepare("SELECT username FROM usuarios WHERE email=?");
    	$consulta->execute($email);

    	# Obtenemos el número de filas coincidentes
    	$username = $consulta->fetchrow_array;
	    
     }
	 
	$consulta = $db->prepare("SELECT COUNT(*) FROM usuarios WHERE username=?");
    	$consulta->execute($username);


    	# Obtenemos el número de filas coincidentes
    	my ($num_filas) = $consulta->fetchrow_array;


     

    
    
    # Verificamos si el usuario ya existe
    if ($num_filas ==  0) {
        #El usuario no existe, redireccionamos al registro

        print $cgi->header(-type => "text/html");
        print "<h3>El usuario no existe</h3>";
        print "<meta http-equiv='refresh' content='3; ../login.html'>";
        $db->disconnect;

     } else {
	

        # Preparar y ejecutar la consulta SQL para actualizar la contraseña en usuarios
        my $consulta= $db->prepare("UPDATE usuarios SET password = ? where username = ?");
        $consulta->execute($contrasenia1, $username);

        #Añado a la cola de modificacion en Linux
        $consulta = $db->prepare("INSERT INTO cola_modificar_contrasenia (username, password) values (?,?)");
        $consulta->execute($username, $contrasenia1);


        if ($consulta->err()) {
            print $cgi->header(-type => "text/html");
            print "<h3>Error al actualizar la contraseña: " . $consulta->errstr() . "</h3>";
            print "<meta http-equiv='refresh' content='3; ../login.html'>";
        } else {
            print $cgi->header(-type => "text/html");
            print "<h3>Contraseña actualizada</h3>";
	    
	    #Añado a la cola de modificacion en Linux
            $consulta = $db->prepare("SELECT email FROM usuarios where username = ?");
            $consulta->execute($username);
 	    my ($email) = $consulta->fetchrow_array;


	    my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'servicioscondeydiego@gmail.com',
                                                 -pass=>'gyjn owfz lqlq htzv');

      	    my $message = "Se ha cambiado la contraseña correctamente ";
 
    	    $mail->send(-to=>$email, -subject=>'Cambio de Contraseña', -body=>$message,
           	 -attachments=>'full_path_to_file');
 
    	    $mail->bye;
	    


            print "<meta http-equiv='refresh' content='3;URL= /cgi-bin/privado.cgi'> ";
        }
       $db->disconnect();
       }

}
