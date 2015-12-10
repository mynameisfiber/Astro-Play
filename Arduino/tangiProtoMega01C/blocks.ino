void readBlocks(){
  j=0;
  k=0;
  for(int i = 0; i<48; i++){ //cycle through all blocks

    if(i < 16){
      j = i;
      k = 1;
    }
    if(i >= 16 && i < 32){
      j = i - 16;
      k = 2;
    }
    if(i >= 32){
      j = i - 32;
      k = 3;
    }
    //set mux
    setMux(k, j);
    //read block & store in variable
    if(i < 16){
      currentBlock = analogRead(A0);
    }
    if(i >= 16 && i< 32){
      currentBlock = analogRead(A1);
    }
    if(i >= 32){
      currentBlock = analogRead(A7);
    }
    //sample(i);//do sampling math to stabilize
    //send values to makeString()
    makeString(i);
  }
}

