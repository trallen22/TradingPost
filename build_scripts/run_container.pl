#!/usr/bin/perl

use Getopt::Long;
use File::Basename;
use Cwd 'abs_path';
use strict;
use warnings;

# TODO: implement command line options
my $componentToRun = ''; # this determines which component to build (frontend/backend)
my $interactive = 0;
GetOptions(
    'component=s' => \$componentToRun,
    'interactive' => \$interactive
    );
if (($componentToRun ne 'backend') && ($componentToRun ne 'frontend')) {
    print("component must be 'backend' or 'frontend'\n");
    exit 1;
}

my $curDirPath = dirname($0); # this should resolve to 'build_scripts/'
my $absPath = abs_path($curDirPath);
my $topPath = "$absPath/../"; # this should go up to TradingPost
my $imageName = "tradingpost-$componentToRun";
my $hostIP = "127.0.0.1";
my %ports = (
    'backend' => '5000',
    'frontend' => '3000',
);
# TODO: maybe clean this up
# `docker run --rm --volume $topPath:/app --publish 127.0.0.1:5000:5000 $imageName`;
if ($interactive) {
    exec("docker", "run", "--rm", "-it", "--init", "--volume", "$topPath:/app", "--publish", "$hostIP:$ports{$componentToRun}:$ports{$componentToRun}", "$imageName", "/bin/bash");
} else {
    exec("docker", "run", "--rm", "--init", "--volume", "$topPath:/app", "--publish", "$hostIP:$ports{$componentToRun}:$ports{$componentToRun}", "$imageName");
}
