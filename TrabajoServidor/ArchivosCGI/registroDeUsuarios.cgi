#!/usr/bin/perl

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
use Crypt::Simple;


my $cgi = new CGI;


#Declaramos las variables de la base de datos
	my $root = "adminBase";
	my $pass = "123456";
	my $host = "localhost";
	my $db_name = "servidor";

	# Nos conectamos a la base de datos
	my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });


#Aqui es cuando se Registra, es decir, cogeremos y validamos los datos
if ($cgi->param('submit')) {

		
	my $username = $cgi->param('username');
	my $passwd = $cgi->param('password');
	my $name = $cgi->param('name');
	my $secondname = $cgi->param('secondname');
	my $email = $cgi->param('email');
	my $postcode = $cgi->param('postcode');
	my $user_type = $cgi->param('user_type'); # Tipo de usuario (profesor o alumno)

	if(length($passwd) < 8){
		print $cgi->header(-type => "text/html");
		print "La contraseña es menor de 8";
		print "<meta http-equiv='refresh' content='3; ../register.html'>";
		exit;
	}elsif(length($username) == 0){
		print $cgi->header(-type => "text/html");
		print "Rellene la contraseña";
		print "<meta http-equiv='refresh' content='3; ../register.html'>";
		exit;
	}elsif(length($name) == 0){
		print $cgi->header(-type => "text/html");
		print "Rellene el nombre";
		print "<meta http-equiv='refresh' content='3; ../register.html'>";
		exit;
	}elsif(length($secondname) == 0){
		print $cgi->header(-type => "text/html");
		print "Rellene el apellido";
		print "<meta http-equiv='refresh' content='3; ../register.html'>";
		exit;
	}elsif(length($postcode) == 0){
		print $cgi->header(-type => "text/html");
		print "El codigo postal esta vacío";
		print "<meta http-equiv='refresh' content='3; ../register.html'>";
		exit;
	}
	else{
		my $mayus = 0;
		my $minus = 0;
    		my $num = 0;
 		my $comprobante = 0;	

		#Recorremos el caracter con la contraseña
 		foreach my $caracter (split //, $passwd){
 			if ($caracter =~ /[A-Z]/){
 				$mayus = 1;
 			}
 			elsif($caracter =~ /[a-z]/){
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
 
 
 	}


	#Comprobamos el postcode
	if($postcode !~ /^\d+$/){
		print $cgi->header(-type => "text/html");
		print "El codigo postal es tiene que ser unicamente numérico";
		print "<meta http-equiv='refresh' content='3; ../register.html'>";
	}
 
 	my $token = generate_token();


	#Comprobar que no existe el correo
	my $consulta = $db->prepare("SELECT COUNT(*) from usuarios where email=?");
	$consulta->execute($email);
	my ($num_filas) = $consulta->fetchrow_array;

	if($num_filas > 0){
		print $cgi->header(-type => "text/html");
		print "El correo ya existe, vuelva a introducirlo";
		print "<meta http-equiv='refresh' content='3; ../register.html'>";
		exit;
	}

	
	#Encriptamos la cotnraseña
	my $cryptPass = encrypt($passwd);
 	########################################################################################################

 	$consulta = $db->prepare("INSERT INTO cola_registro(username,password, token, name, secondname, email, postcode, user_type) VALUES (?,?,?,?,?,?,?,?)");
 	$consulta->execute($username, $cryptPass, $token, $name, $secondname, $email, $postcode, $user_type);
 
 	########################################################################################################
 
 	my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                   -login=>'servicioscondeydiego@gmail.com',
                                                   -pass=>'gyjn owfz lqlq htzv');
  
   	 my $message = "Haz clic en el siguiente enlace para crear el usuario: ";
  	   $message .= "http://170.253.8.68/cgi-bin/registroDeUsuarios.cgi?token=$token";
 
    	 $mail->send(-to=>$email, -subject=>'Creacion de usuario', -body=>$message,
             -attachments=>'full_path_to_file');
 
     	$mail->bye;

	print $cgi->header(-type => "text/html");
    print "Se te ha enviado un correo.";
	print "<meta http-equiv='refresh' content='3; ../login.html'>";

	

}
else{	#En este else, es cuando vuelven del gmail que han pulsado el link, sabemos que son ellos por lo que los registramos

	my $token = $cgi->param("token");

	my $consulta = $db->prepare("SELECT * FROM cola_registro where token = ?");

	$consulta->execute($token);
	
	my ($username, $cryptPass, $name, $secondname, $email, $postcode, $user_type);
	if (my $row = $consulta->fetchrow_hashref) {
		$username = $row->{username};
		$cryptPass = $row->{password};
		$token = $row->{token};
		$name = $row->{name};
		$secondname = $row->{secondname};
		$email = $row->{email};
		$postcode = $row->{postcode};
		$user_type = $row->{user_type};
	}

	
	$consulta = $db->prepare("SELECT COUNT(*) FROM usuarios WHERE username=?");
	$consulta->execute($username);

	my ($num_filas) = $consulta->fetchrow_array;
	if ($num_filas > 0) {
		#El usuario existe, redireccionamos al registro
		
		print $cgi->header(-type => "text/html");
		print "<h3>El usuario ya existe</h3>";
		print "<meta http-equiv='refresh' content='3; ../register.html'>";
		$db->disconnect;

	}else {
		#Usuario no existe, podemos crear el usuario

		$consulta = $db->prepare("INSERT INTO cola_registros_usuarios(username,password, name, secondname, email, postcode, user_type) VALUES (?,?,?,?,?,?,?)");
		$consulta->execute($username, $cryptPass, $name, $secondname, $email, $postcode, $user_type);

		$consulta = $db->prepare("DELETE FROM cola_registro where token = ?");
		$consulta->execute($token);		
		

		print $cgi->header(-type => "text/html");

	        print "Se ha creado el usuario correctamente";
		print "Redirigimos a la pantalla principal en 3 segundos, para poderse loguear es en el apartado loggin";
		print "<meta http-equiv='refresh' content='3; ../login.html'>";


	}
	$db->disconnect;
}





# Función para generar un token único
sub generate_token {
    my @chars = ('A'..'Z', 'a'..'z', 0..9);
    my $token = '';
    $token .= $chars[rand @chars] for 1..32;
    return $token;
}






