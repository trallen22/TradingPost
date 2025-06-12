#!/usr/bin/perl

use Getopt::Long;
use File::Basename;
use strict;
use warnings;

my $componentToBuild = ''; # this determines which component to build (frontend/backend)
my $curFileName = basename($0);
GetOptions('component=s' => \$componentToBuild);
if (($componentToBuild ne 'backend') && ($componentToBuild ne 'frontend')) {
    print("ERROR: usage: $curFileName [--c <backend/frontend>]\n");
    exit 1;
}

my $curDirPath = dirname($0);
my $DockerFilePath = "$curDirPath/$componentToBuild/";
# build with 'docker build'
`docker build -t tradingpost-$componentToBuild $DockerFilePath`;
if ($?) {
    print("ERROR: docker build failed");
}
