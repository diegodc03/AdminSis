#!/usr/bin/perl

use strict;
use warnings;
use DBI;

my $username = "usuario";
my $passwd = "contraseña";
my $name = "Nombre";
my $secondname = "Apellido";
my $email = "correo\@gmail.com";
my $postcode = "12345";


#Probar Base de Datos
 #Declaramos las variables de la base de datos
    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "na";

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
        #No existe el usuario
        print "Usuario enconntrado"

    } else {
        
        #Usuario no existe, podemos crear el usuario

        my $var = $db->prepare("INSERT INTO usuarios(username,password, name, secondname, email, postcode) VALUES (?,?,?,?,?,?)");

        $var->execute($username,$passwd,$name,$secondname, $email, $postcode);

        $db->disconnect;

        print "Usuario correcto"

    }
