#!/usr/bin/perl

use strict;
use CGI;
use CGI::Session; 
use DBI;
use Crypt::Simple;


#Creamos un objeto CGI
my $cgi = CGI->new();

my $username = $cgi->param("username");
my $password = $cgi->param("password");


    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "servidor";
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

    my $consulta = $db->prepare("SELECT * FROM usuarios WHERE username= ?");
    $consulta->execute($username);


    my $fila = fetchrow_array;


    my $passworddb = decrypt($fila[1]);

    my $inicio_ses = 0;
    if($password eq $passworddb){
        $inicio_ses = 1;

    }

    


    #Usuario Entocontrado        #Creamos la ssesion
    if($inicio_ses eq 1){
        my $session = new CGI::Session();
	#my $session = new CGI::Session("id:md5", $cgi, {Directory=>"sessions"});
	
        $session->save_param($cgi);
        $session->expires("10h");
        $session->flush();

	system("logger -p local6.info 'Inicio de sision existoso '");
	
	
	#print $cgi->header("-cookie=>cookie");
        print $session->header(-location => "privado.cgi");
	#print $cgi->redirect("privado.cgi");

	}
   else{
        
	system("logger -p local6.info 'Inicio de sision fallido'");
        print $cgi->redirect("http://170.253.8.68/index.html");
    }


    $db->disconnect();


