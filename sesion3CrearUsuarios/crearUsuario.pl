#!/usr/bin/perl

# Script to create an user in Linux (debian 12)

#Author:    Diego de Castro Merillas    [diegodecatro@usal.es]

# We are going to use Cpan, USERMOD.

# First, if we have not downloaded the usermod library...
# sudo apt install cpanminus
# cpanm install Linux::usermod


use strict;
use warnings;
use Linux::usermod;
use File::Copy;

# First, we answer the client, the parrameters of the new account
print "Enter the username";
my $username = <STDIN>;
chomp($username);

#we check if the username exists
if(getpwnam($username)){
    print "The username alredy exists";
    exit();
}

####
print "Enter the password";
my $password = <STDIN>;
chomp($password);

#print "the username is $username and the password $password";

#add home route
my $homeRoute = "/home/".$username."/";
#print "The home route is $homeRoute ";


mkdir $homeRoute || print $!;
chmod(0770, $homeRoute) || print $! ;

# Create a new user
Linux::usermod->add($username, $password, '', '', '', $homeRoute, "/bin/bash");
my $user=Linux::usermod->new($username);
my $uid = $user->get('uid');
my $gid = $user->get('gid');

# We change the permissions of the homeroute
chown($uid, $gid, $homeRoute);


#The last one, we copy skel to new user
# Copy contents of /etc/skel to new user's home directory
my $skel_dir = "/etc/skel";
my $new_user_home = "/home/$username";

opendir(my $skel_fh, $skel_dir) || die "Failed to open skel directory: $!";
while (my $entry = readdir($skel_fh)) {
    next if $entry eq '.' || $entry eq '..';  # Skip hidden files
    
        my $source = "$skel_dir/$entry";
        my $destination = "$new_user_home/$entry";
        copy($source, $destination) || warn "Failed to copy $source to $destination: $!";
        chown($uid, $gid, "$homeRoute/$entry");

}
closedir($skel_fh);



print "The user $username has been created successfully\n";







