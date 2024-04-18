#!/usr/bin/perl
 
use strict;
use warnings;
use Excel::Writer::XLSX;
print "Content-type: text/html\n\n";
my $workbook  = Excel::Writer::XLSX->new( 'pieStadistics.xlsx' );
my $worksheet = $workbook->add_worksheet();
 
my $chart     = $workbook->add_chart( type => 'pie' );
 
# Configure the chart.
$chart->add_series(
    categories => '=Sheet1!$A$2:$A$7',
    values     => '=Sheet1!$B$2:$B$7',
);
 
# Add the worksheet data the chart refers to.
my $data = [
    [ 'Category', 2, 3, 4, 5, 6, 7 ],
    [ 'Value',    1, 4, 5, 2, 1, 5 ],
];
 
$worksheet->write( 'A1', $data );
 
__END__

