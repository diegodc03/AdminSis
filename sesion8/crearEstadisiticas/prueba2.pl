#!/usr/bin/perl

use warnings;
use strict;


open my $pipe, '-|', 'sa', '-cd' or die "Can't open pipe: $!";


# In pipe variable, I have all the output of the command 'sa -cd'
# I split all the lines of pipe and I print each line

my @porcentaje;
my @command; 

foreach my $line (<$pipe>) {

    my @cadena = split(' ', $line);

    for(my $c = 0; $c <= $#cadena; $c++) {  # Corrección aquí
    
        #my $cont = 0;
        if($c == 1){
            push @porcentaje, $cadena[$c];
            
        }elsif($c == 8){
            $cadena = substr($cadena, 0, -1);  # Quitar la última letra
        my $numero = int($cadena);  # Convertir la cadena en un número entero
            push @command, $cadena[$c];
            
        }
    }
}


for(my $c = 0; $c <= $#porcentaje; $c++){
    print $porcentaje[$c];
    print "\n"
}

for(my $c = 0; $c <= $#command; $c++){
    print $command[$c];
    print "\n"
}




