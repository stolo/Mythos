#!/usr/bin/perl

use Lingua::LinkParser;
use YAML;
use strict;

my $parser = new Lingua::LinkParser;        # create the parser
my $zeus_text   = "Zeus is the God of thunder";
my $thor_text   = "Thor is the lord of thunder";
          
my $sentence = $parser->create_sentence($zeus_text); # parse the sentence
my $linkage  = $sentence->linkage(1);        # use the first linkage
print $parser->get_diagram($linkage);         # print it out

my $sentence = $parser->create_sentence($thor_text); # parse the sentence
my $linkage  = $sentence->linkage(1);        # use the first linkage
print $parser->get_diagram($linkage);         # print it out

my $greek_gods = YAML::LoadFile('./olympiansHR.yaml');
#foreach (@greek_gods){
#    print $_['name'];
#}

