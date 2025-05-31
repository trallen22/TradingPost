#!/usr/bin/perl 
use strict;
use Cwd;

my $curTest;
our $passedTests = 0;
our $numTests = 0;
my $nullFile = '/dev/null'; # change to NUL for Windows -> my $nullFile = 'NUL'
my $baseURL = 'http://127.0.0.1:5000';

sub check_test {
    my $curStr = shift;
    my $curTest = shift;
    $numTests = $numTests + 1;
    if ($curStr) {
        $passedTests = $passedTests + 1;
    } else {
        print("Test $curTest failed\n");
    }
}

#######################
# Section 1: News endpoint
#######################
# Test 1.1: this tests signs a user up; should return success 
$curTest = `curl -X GET $baseURL/ticker-news/AAPL -H "Content-Type: application/json" 2>$nullFile | grep success`;
check_test($curTest, 1.1);

END {
    print("Tests passed: $passedTests/$numTests\n");
    if (!$passedTests) { # this is if no tests pass 
        print("Make sure the backend server is running\n");
    }
}