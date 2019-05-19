#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

my @tasks = ("power", "reset", "weakness", "avltree");
my $path = "./src/tests";

print "-" x 40 . "\n";

foreach my $task (@tasks) {

	opendir(my $dh, "$path/$task") or die "Cant' open $path/$task";
	my @input = grep(/\.in$/, readdir($dh));
	closedir($dh);

	foreach my $input (@input) {
		print "Test file: $path/$task/$input\n";

		if ($input =~ /(.+)\.in/) {

			open(my $fh, '<', "$path/$task/$1.out") or die "Can't open $path/$task/$1.out";
			chomp(my @output = <$fh>);
			close $fh;

			my $output = join("\n", @output) . "\n";

			my $program_out = `./$task < $path/$task/$input`;
			my $exit_code = $?;

			my $out_eq = $program_out eq $output;

			if ($out_eq) {
				print "OK\n";
			} else {
				print "Expected:\n$output";
				print "Program:\n$program_out";
			}
            print "\n";

		} else {
			next;
		}
	}
}
