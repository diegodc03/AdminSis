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

		
	my $username = $q->param('username');
	my $passwd = $q->param('password');
	my $name = $q->param('name');
	my $secondname = $q->param('secondname');
	my $email = $q->param('email');
	my $postcode = $q->param('postcode');

	if(length($passwd) < 8){
		print $q->header(-type => "text/html");
		print "La contraseña es menor de 8";
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
				$num = 1
			}
			
			if($mayus == 1 and $minus == 1 and $num == 1){
				#print $q->header(-type => "text/html");
				#print "La contraseña es correcta";
				$comprobante = 1;
				last;
			}	
			
		
		}

		if($comprobante == 0){
			print $q->header(-type => "text/html");
			print "La contraseña tiene que tener minusculas mayusculas y letras";
			
			#exit;
		}


	}

	my $token = generate_token();

	########################################################################################################

	#Hacemos la consulta
	my $consulta = $db->prepare("INSERT INTO cola_registro_usuarios(username,password, token, name, surname, email, postcode) VALUES (?,?,?,?,?,?,?)");

	# Ejecutamos la consulta
	$consulta->execute($username);

	########################################################################################################

	my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'servicioscondeydiego@gmail.com',
                                                 -pass=>'gyjn owfz lqlq htzv');

    my $message = "Haz clic en el siguiente enlace para crear el usuario: ";
    $message .= "http://example.com/reset_password.pl?token=$token";
 
    $mail->send(-to=>$email, -subject=>'Creacion de usuario', -body=>$message,
            -attachments=>'full_path_to_file');
 
    $mail->bye;




}
else{	#En este else, es cuando vuelven del gmail que han pulsado el link, sabemos que son ellos por lo que los registramos

	my $token = $cgi->param("token")
	#Con el token accedemos a la base de datos y asi podemos poner todo en la base de datos de verdad
	#Hacemos la consulta
	my $consulta = $db->prepare("SELECT * FROM cola_registros_usuarios where token = ?");

	# Ejecutamos la consulta
	$consulta->execute($token);

	# Recuperar y almacenar los datos en variables
	my ($username, $password, $token, $name, $secondname, $email, $postcode);
	if (my $row = $sth->fetchrow_hashref) {
		$username = $row->{username};
		$passwd = $row->{password};
		$token = $row->{token};
		$name = $row->{name};
		$secondname = $row->{secondname};
		$email = $row->{email};
		$postcode = $row->{postcode};
	}
		
	#Creamos el usuario
	#we check if the username exists
	if(getpwnam($username)){
		print "Usuario Existente";
	}

	#add home route
	my $homeRoute = "/home/".$username."/";
	#print "The home route is $homeRoute ";


	# Creamos el nuevo usuario
		Linux::usermod->add($username, $password, undef, undef, undef, $homeRoute, "/bin/bash");
		my $user=Linux::usermod->new($username);
		Linux::usermod->grpadd($username, $user->get('gid'));
		my $usergroup = Linux::usermod->new($username, 1);

		my $uid = $user->get('uid');
		my $gid = $user->get('gid');



	#Crear /home y copiar las cosas de /etc/skel
		make_path($homeRoute , { owner => $username, group => $username });
		dircopy("/etc/skel", $homeRoute);
		
		chown($uid, $gid, $homeRoute);  # Cambiar el propietario y grupo del directorio
		chown($uid, -1, "$homeRoute/*");  # Cambiar el propietario de los archivos dentro del directorio    
		chown(-1, $gid, "$homeRoute/*");  # Cambiar el grupo de los archivos dentro del directorio
	

	#Establecer las quotas para ese usuario en /home
		my $quotadev = Quota::getqcarg("/");
		Quota::setqlim($quotadev, $uid, 61440, 81920, 0, 0);


		
	########################################################################################################
	#Añadir a la base de datos


	#Hacemos la consulta
	my $consulta = $db->prepare("SELECT COUNT(*) FROM usuarios WHERE username=?");

	# Ejecutamos la consulta
	$consulta->execute($username);

	# Obtenemos el número de filas coincidentes
	my ($num_filas) = $consulta->fetchrow_array;

	# Verificamos si el usuario ya existe
	if ($num_filas > 0) {
		#El usuario existe, redireccionamos al registro
		
		print $q->header(-type => "text/html");
		print "<h3>El usuario ya existe</h3>";
		print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
		$db->disconnect;

	} else {
		#Usuario no existe, podemos crear el usuario

		my $var = $dbh->prepare('INSERT INTO usuarios(username,password, name, surname, email, postcode) VALUES (?,?,?,?,?,?)');

		$var->execute($username,$passwd,$name,$secondname, $email, $postcode);

		$db->disconnect;

		print $q->header(-type => "text/html");
		print "<h3>Usuario correcto, no existe en la base de datos</h3>";

	}


}





# Función para generar un token único
sub generate_token {
    my @chars = ('A'..'Z', 'a'..'z', 0..9);
    my $token = '';
    $token .= $chars[rand @chars] for 1..32;
    return $token;
}







