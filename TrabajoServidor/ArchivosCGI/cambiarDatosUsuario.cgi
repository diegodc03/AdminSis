#!/usr/bin/perl

#Aqui tenemos que cambiar los datos del usuario que quiera modificarlos
#Va a venir de un forms, en el cual cogeremos los valores y los añadiremos


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
my $session = new CGI::Session();

$session->load();


if($session->is_expired or !$loggedUser){ 
	print $cgi->redirect("/webs/login.html");

}else{

 #Añadimos en cada variable, la modificación de los datos
    my $name = $q->param('name');
    my $secondname = $q->param('secondname');
    my $email = $q->param('email');
    my $postcode = $q->param('postcode');


    
    if(length($passwd) >= 8){
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
   
     


    }  




}
