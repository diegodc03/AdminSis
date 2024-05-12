#!/usr/bin/perl

# Script to delete an user in Linux (debian 12)

#Author:    Diego de Castro Merillas    [diegodecatro@usal.es]

# We are going to use Cpan, USERMOD.
 
# First, if we have not downloaded the usermod library...
# sudo apt install cpanminus
# cpanm install Linux::usermod

use strict;
use warnings;
use POSIX;
use Linux::usermod;
use File::Path qw(rmtree);

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

}
    
