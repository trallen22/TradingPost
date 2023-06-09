use strict;

my $commitMsg = shift;
if ($commitMsg eq '') {
	print "ERROR: Usage: missing commit message";
	exit -1;
}

my $add = `git add --all`; 
(print "ERROR: problem adding to git" && exit 1) if $?;

my $commit = `git commit -m \"$commitMsg\"`;
(print "ERROR: problem commiting to git" && exit 2) if $?;

my $push = `git push`;
(print "ERROR: problem pushing to remote" && exit 3) if $?;

exit 0;


