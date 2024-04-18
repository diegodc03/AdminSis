#!/usr/bin/perl

use strict;
use warnings;

# Ejecutar el comando 'sa -cd' y capturar la salida en una variable
my $output = `sa -cd`;

# Dividir la salida en líneas y procesar cada línea
my @lines = split /\n/, $output;


foreach my $line (@lines) {
    # Hacer algo con cada línea, por ejemplo, imprimir
    print $line . "\n";
}


