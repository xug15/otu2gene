open I, "<$ARGV[0]";
open O, ">$ARGV[1]";
while(<I>){
chomp;
@data=split /\t/,$_;
if($data[2]>96){
        print O "$data[0]\t$data[1]\n";
   }
}
close I;
close O;
