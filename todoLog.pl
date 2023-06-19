#!/usr/bin/perl

use strict;


# Gets the todo number for format TODO#
sub get_number { 
    my $task = shift; 
    my $logNumber = (my @tmpTask = split(':', $task))[0];
    my $number = substr($logNumber, 5);

    return $number;
}


sub get_todos {
    my $curTodo = shift;
    my $path = shift;
    
    $curTodo =~ s/[\n\r\s]+//g; # removes tab from todos
    my $tmpStr = substr($curTodo, 0, 5);

    if ($tmpStr eq uc('#todo')) {
        my $logNum = get_number($curTodo);
        if ($logNum eq '') {
            return "Lonesome TODO";
        } else {
            return "$logNum in $path";
        }
    }
}

# Checks each file in directory for TODOs 
sub check_path {
    my $curPath = shift;
    chomp($curPath);
    my @listTodos = shift;
    my @nextPaths = `ls $curPath`;

    for my $path (@nextPaths) {
        chomp($path);
        my $thisPath = "$curPath\/$path";
        if (-d $thisPath) {
            my @todoArray = check_path($thisPath, @listTodos); # recursively checks directories 
            push (@listTodos, @todoArray);
        } elsif ($path =~ /.py$/ || $path =~ /.pl$/) {
            my @todoList = `cat $thisPath | grep TODO`;
            foreach (@todoList) {
                my $strTodo = get_todos($_, $path);
                push (@listTodos, $strTodo);
            }
        }   
    }
    return @listTodos;  
}

# TODO8: Work on script to editing changeLog.txt

my $cwd = `pwd`;
my @listTodo = ();
@listTodo = check_path($cwd, @listTodo);
my $i = 0;
foreach (@listTodo) {
    chomp($_);
    print "$_\n" if $_ ne '';
}

exit 0;

