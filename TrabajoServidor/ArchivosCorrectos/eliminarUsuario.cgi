#!/usr/bin/perl

#Darse de baja en un servicio implica varios aspectos
    # Eliminar de la base de datos mariadb  --> es una consulta
    # Eliminar como usuario
    

use strict;
use warnings;
use POSIX;
use Linux::usermod;
use File::Path qw(rmtree);



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

    my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'upsauniversidaddevalladolid@gmail.com',
                                                 -pass=>'paol ulvc mcbo gxkx');


 
    $mail->send(-to=>$email, -subject=>'Usuario Eliminado', -body=>'Usted se ha dado de baja en el servicio Conde Y bermejo Soluciones',
            -attachments=>'full_path_to_file');
 
    $mail->bye;


}
