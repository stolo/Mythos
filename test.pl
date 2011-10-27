#!/usr/bin/perl

use Lingua::LinkParser;
use Lingua::LinkParser::Definitions;
use JSON;
use strict;

my $parser = new Lingua::LinkParser;        # create the parser
my @texts = ( "Hera is the goddess of birth", "Thor is the lord of thunder");
          

foreach my $text (@texts){
    print $text . "\n";
    my $linkage = get_linkage($text);
    my @words = $linkage->words();
    foreach my $word (@words){
        print $word->{'_text'};
        print "\n";
        print get_word_link_codes($word);
        print "\n";
    }
}

sub get_linkage(){
    my $text = shift;
    my $sentence = $parser->create_sentence($text); # parse the sentence
    my $linkage  = $sentence->linkage(1);        # use the first linkage
    return $linkage;
}

sub get_word_link_codes(){
    my $word = shift;
    my @links = $word->links;
    my @link_codes;
    foreach my $link (@links){
        push (@link_codes, $link->{'linklabel'});
    }
    return @link_codes;
}

sub get_word_link_words(){
    my $word = shift;
    my @links = $word->links;
    my @link_words;
    foreach my $link (@links){
        push (@link_words, $link->{'linkword'});
    }
    return @link_words;
}


#foreach my $word (@words){
#    foreach my $key (keys %$word){
#        print $key . " : ";
#        print $word->{$key} . "\n";
#    }
#    my @links = $word->{"_links"};
#    foreach my $link (@links){
#        foreach my $l (@$link){
#            foreach my $k (keys %$l){
#                print $k . " : " . $l->{$k} . "\n";
#            }
#        }
#    }
#    print "***\n";
#}
#print $parser->get_diagram($linkage);         # print it out

#my $sentence = $parser->create_sentence($thor_text); # parse the sentence
#my $linkage  = $sentence->linkage(1);        # use the first linkage
#print $parser->get_diagram($linkage);         # print it out

#open( my $fh, '<', 'olympians.json' );
#my $json_text   = <$fh>;
#my $gods = decode_json( $json_text );
#foreach (@$gods){
#    my @description = split(/[\.\,\;\:]/, $_->{'description'});
#    my $domains = $_->{'domains'};
#    #print $domains; 
#    my $rep;
#    foreach my $desc(@description){
#        foreach my $domain(@$domains){
#            if ($desc =~ m/$domain/){
#                my $sentence = $parser->create_sentence("$desc"); # parse the sentence
#                my @linkages = $sentence->linkages;        # use the first linkage
#                #print length(@linkages);
#                my $rep;
#                foreach my $linkage (@linkages) {
#                    #print $parser->get_diagram($linkage);         # print it out
#                    print define($linkage);
#                    #print $parser->print_constituent_tree($linkage, 2);
#                    #print $linkage->linklabel . "&&&&\n";
#                    #my @words = $linkage->words;
#                    #foreach my $word (@words){
#                    #    print "$word->linkword\n";
#                    #    foreach my $link ($word->links){
#                    #        $rep .= $link->linklabel;
#                    #    }
#                    #}
#                }
#                if ($rep){
#                    print "$desc\n";
#                    print "$rep\n\n";
#                }
#            }
#        }
#    }
#}
#
#my $sentence = $parser->create_sentence($text); # parse the sentence
#my $linkage  = $sentence->linkage(1);        # use the first linkage
#print $parser->get_diagram($linkage);         # print it out
