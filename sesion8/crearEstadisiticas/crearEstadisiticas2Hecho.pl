#!/usr/bin/perl

use strict;
use warnings;
use Excel::Writer::XLSX;


# We get a excel file with a pie chart of the most used programs in the system
# We get the data from the database

open my $pipe, '-|', 'sa', '-cd' or die "Can't open pipe: $!";


# In pipe variable, I have all the output of the command 'sa -cd'
# I split all the lines of pipe and I print each line

my @porcentaje;
my @command; 
my $aux = 0;
foreach my $line (<$pipe>) {

    my @cadena = split(' ', $line);
    if($aux != 0){
        for(my $c = 0; $c <= $#cadena; $c++) {  # Corrección aquí
        
            #my $cont = 0;
            if($c == 1){
                my $cadenaC = substr($cadena[$c], 0, -1);  # Quitar la última letra
                my $numero = eval($cadenaC);  # Convertir la cadena en un número entero
                push @porcentaje, $numero;
                print $numero;
                
            }elsif($c == 8){
                
                push @command, $cadena[$c]
                
            }
        }
    }
    $aux = 1;
    
}


#Count number of array
my $numArray = $#command;


my $workbook  = Excel::Writer::XLSX->new( 'chart_pie_command_used1.xlsx' );
my $worksheet = $workbook->add_worksheet();
my $bold      = $workbook->add_format( bold => 1 );

# Add the worksheet data that the charts will refer to.
my $headings = [ 'Commands', 'Porcentajes' ];
my $data = [
    [ @command ],
    [ @porcentaje],
];

$worksheet->write( 'A1', $headings, $bold );
$worksheet->write( 'A2', $data );

# Create a new chart object. In this case an embedded chart.
my $chart = $workbook->add_chart( type => 'pie', embedded => 1 );

# Configure the series.
$chart->add_series(
    name        => 'Pie sales data',
    categories  => [ 'Sheet1', 1, 10, 0, 0 ],
    values      => [ 'Sheet1', 1, 10, 1, 1 ],
    data_labels => { value => 1 },
);

# Add a title.
$chart->set_title( name => 'Popular Pie Types' );

# Set an Excel chart style. Colors with white outline and shadow.
$chart->set_style( 10 );

# Insert the chart into the worksheet (with an offset).
$worksheet->insert_chart( 'C2', $chart, 25, 10 );

__END__
