void makeString(char val){ //adds block values to string

if(val < 10){
trayVals = trayVals + (char)(val+48); //add position
}
else if(val >9){
  int val2;
  val2 = val/10;
  val = val- val2*10;
  trayVals = trayVals + (char)(val2+48); //add position
    trayVals = trayVals + (char)(val+48); //add position
}
trayVals = trayVals + ':';

//split current block into values
int cBlock1;
int cBlock2;
int cBlock3;
int cBlock4;
if(currentBlock >= 1000){ //thousands
  cBlock1 = currentBlock /1000; //get first two values
  currentBlock = currentBlock - (cBlock1 * 1000);
}
else{
  (cBlock1 = 0);
}
if(currentBlock >= 100){//hundreds
  cBlock2 = currentBlock /100; //get first two values
  currentBlock = currentBlock - (cBlock2 * 100);
}
else{
  (cBlock2 = 0);
}
if(currentBlock >= 10){//tens
  cBlock3 = currentBlock /10; //get first two values
  currentBlock = currentBlock - (cBlock3 * 10);
}
else{
  (cBlock3 = 0);
}
cBlock4 = currentBlock; //ones

trayVals = trayVals + char(cBlock1 + 48);
trayVals = trayVals + char(cBlock2 + 48);
trayVals = trayVals + char(cBlock3 + 48);
trayVals = trayVals + char(cBlock4 + 48);
trayVals = trayVals + ',';

}


void endTrayString(){
  trayVals = trayVals  + (char)(4+48) +(char)(8+48) + ':' + (char)(mode+48);
    trayVals = trayVals + ',';
    trayVals = trayVals + (char)(4+48) +(char)(9+48) + ':'+ (char)(sendCode+48);
        trayVals = trayVals + ',';
        trayVals = trayVals + (char)(5+48) +(char)(0+48) + ':'+ (char)(runPause+48);
                //trayVals = trayVals + '}';
}
