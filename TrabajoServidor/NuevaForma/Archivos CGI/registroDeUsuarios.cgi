#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use DBI;
use Linux::usermod;
use File::Copy;
use Quota;
use Email::Send::SMTP::Gmail;


my $q = CGI->new();

my $a = $q->param('username');
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

#Creamos el usuario

#we check if the username exists
if(getpwnam($a)){
    print $q->header(-type => "text/html");
	print "Usuario Existente";
}


#add home route
my $homeRoute = "/home/".$username."/";
#print "The home route is $homeRoute ";

#Añadimos los permisos de home route
mkdir $homeRoute || print $!;
chmod(0770, $homeRoute) || print $! ;


# Creamos el nuevo usuario
Linux::usermod->add($username, $password, '', '', '', $homeRoute, "/bin/bash");
my $user=Linux::usermod->new($username);
my $uid = $user->get('uid');
my $gid = $user->get('gid');


# Le damos los permisos al usuario
chown($uid, $gid, $homeRoute);


#The last one, we copy skel to new user
# Copy contents of /etc/skel to new user's home directory
my $skel_dir = "/etc/skel";
my $new_user_home = "/home/$username";

opendir(my $skel_fh, $skel_dir) || die "Failed to open skel directory: $!";
while (my $entry = readdir($skel_fh)) {
    next if $entry eq '.' || $entry eq '..';  # Skip hidden files
    
        my $source = "$skel_dir/$entry";
        my $destination = "$new_user_home/$entry";
        copy($source, $destination) || warn "Failed to copy $source to $destination: $!";
        chown($uid, $gid, "$homeRoute/$entry");

}
closedir($skel_fh);




#Añadimos la quota de limite fuerte de 80 MB
my $hard = 80000;


#We apply the quota
my ($block_set, $inode_set) = Quota::setqlim($homeRoute, $uid, 0, $hard, 0, 0, 0, 0);


if ($block_set && $inode_set) {
	print $q->header(-type => "text/html");
    print "Cuotas establecidas correctamente para $username .\n";
} else {
	print $q->header(-type => "text/html");
    print "Error al establecer las cuotas para $username: $!\n";
}



#Aqui pon el correo que sea

my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'upsauniversidaddevalladolid@gmail.com',
                                                 -pass=>'paol ulvc mcbo gxkx');


 
$mail->send(-to=>$email, -subject=>'Usuario Creado', -body=>'Usted se ha dado de alta en el servicio Conde Y bermejo Soluciones',
            -attachments=>'full_path_to_file');
 
$mail->bye;


########################################################################################################
#Añadir a la base de datos

#Declaramos las variables de la base de datos
my $root = "root";
my $pass = "";
my $host = "localhost";
my $db_name = "usuarios";

# Nos conectamos a la base de datos
my $db = DBI->connect("DBI:MariaDB:database=$db;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

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

	my $var = $dbh->prepare('INSERT INTO usuarios(username,password, name, surname, email, postcode) VALUES (?,?, ?,?,?,?,1,1,0)');

	$var->execute($username,$passwd,$name,$secondname, $email, $postcode);

	$db->disconnect;

    print $q->header(-type => "text/html");
    print "<h3>Usuario correcto, no existe en la base de datos</h3>";

}







print $q->header(-type => 'text/plain');
print "Creado $a";


