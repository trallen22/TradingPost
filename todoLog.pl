#!/usr/bin/perl

use strict;


# Gets the todo number for format TODO#
sub get_number {
    my $task = shift; 
    my $logNumber = (my @tmpTask = split(':', $task))[0];
    my $number = substr($logNumber, 5);

    return $number;
}

# Checks each file in directory for TODOs 
sub check_folder {
    my $curPath = shift;
    chomp($curPath);

    my @nextPaths = `ls $curPath`;

    for my $path (@nextPaths) {
        chomp($path);
        my $thisPath = "$curPath\/$path";
        
        if (-d $thisPath) {
            check_folder($thisPath);
        } elsif ($path =~ /.py$/ || $path =~ /.pl$/) {
            my @todoList = `cat $thisPath | grep TODO`;
            foreach (@todoList) {
                $_ =~ s/[\n\r\s]+//g; # removes tab from todos
                my $tmpStr = substr($_, 0, 5);
                if ($tmpStr eq uc('#todo')) {
                    my $logNum = get_number($_);
                    if ($logNum eq '') {
                        print "Lonesome TODO\n";
                    } else {
                        print "$logNum in $path\n";
                    }
                    
                }
            }
        }     
    }
}

# TODO8: Work on script to editing changeLog.txt

my $cwd = `pwd`;
check_folder($cwd);


exit 0;

