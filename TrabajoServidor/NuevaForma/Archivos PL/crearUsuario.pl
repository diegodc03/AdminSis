#!/usr/bin/perl

# Script to create an user in Linux (debian 12)

#Author:    Diego de Castro Merillas    [diegodecatro@usal.es]

# We are going to use Cpan, USERMOD.

# First, if we have not downloaded the usermod library...
# sudo apt install cpanminus
# cpanm install Linux::usermod



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

    
	# Recuperar datos de la cola de usuarios
my $consulta_cola = $db->prepare("SELECT * FROM cola_registros_usuarios");
$consulta_cola->execute;

while (my $fila = $consulta_cola->fetchrow_hashref) {
    my $username = $fila->{username};
    my $password = $fila->{password};
    my $token = $fila->{token};
    my $name = $fila->{name};
    my $secondname = $fila->{secondname};
    my $email = $fila->{email};
    my $postcode = $fila->{postcode};

    # Verificar si el usuario ya existe en el sistema
    if (getpwnam($username)) {
        print $cgi->header("text/html");
        print "El usuario ya existe en el servidor Linux: $username\n";
        print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
        next;
    }

    # Directorio de inicio del usuario
    my $homeRoute = "/home/$username";

    # Crear el usuario en el sistema
    Linux::usermod->add($username, $password, undef, undef, undef, $homeRoute, "/bin/bash");
    my $user = Linux::usermod->new($username);
    Linux::usermod->grpadd($username, $user->get('gid'));

    # Copiar archivos de configuración predeterminados al directorio de inicio del usuario
    make_path($homeRoute);
    dircopy("/etc/skel", $homeRoute);

    # Establecer cuotas de disco para el usuario
    my $uid = $user->get('uid');
    my $quotadev = Quota::getqcarg("/");
    Quota::setqlim($quotadev, $uid, 61440, 81920, 0, 0);

    # Añadir el usuario a la base de datos si no existe
    my $consulta= $db->prepare("SELECT COUNT(*) FROM usuarios WHERE username = ?");
    $consulta->execute($username);
    my ($num_filas) = $consulta->fetchrow_array;

    if ($num_filas == 0) {
        $consulta = $db->prepare('INSERT INTO usuarios (username, password, name, secondname, email, postcode) VALUES (?, ?, ?, ?, ?, ?)');
        $consulta->execute($username, $password, $name, $secondname, $email, $postcode);
        

        # Enviar correo electrónico de confirmación
        my $mailer = Email::Send::SMTP::Gmail->new(
            -smtp  => 'smtp.gmail.com',
            -login => 'servicioscondeydiego@gmail.com',
            -pass  => 'gyjn owfz lqlq htzv'
        );

        my $mensaje = "Usuario creado correctamente. Puedes iniciar sesión en el sistema.";
        $mailer->send(
            -to      => $email,
            -subject => 'Acceso Creado',
            -body    => $mensaje
        );

        $mailer->bye;

        #Eliminar usuario de la cola
        # Añadir el usuario a la base de datos si no existe
        $consulta = $db->prepare("DELETE cola_registros_usuarios.* FROM cola_registros_usuarios WHERE username = ? and email= ?");
        $consulta->execute($username, $email);



    } else {
        print $cgi->header("text/html");
        print "El usuario ya existe en la base de datos: $username\n";
        print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
    }
}

# Desconectar de la base de datos
$db->disconnect;




