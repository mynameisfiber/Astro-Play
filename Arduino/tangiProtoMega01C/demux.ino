void setMux(int muxNum, int y){
  int s0;
  int s1;
  int s2;
  int s3;
      int muxs0;
    int muxs1;
    int muxs2;
    int muxs3;
  if(muxNum == 1){

    muxs0 = 8;
    muxs1 = 9;
    muxs2 = 10;
    muxs3 = 11;
  }
  else if(muxNum == 2){

    muxs0 = 12;
    muxs1 = 5;
    muxs2 = 6;
    muxs3 = 7;
  }
  else if(muxNum == 3){
    muxs0 = 13;
    muxs1 = A3;
    muxs2 = A4;
    muxs3 = A5;
  }
  switch(y){ //this could be done a lot prettier but it's late and I don't care
  case 0:
    s0 = 0;
    s1 = 0;
    s2 = 0;
    s3 = 0;
    break;
  case 1:
    s0 = 255;
    s1 = 0;
    s2 = 0;
    s3 = 0;
    break;
  case 2:
    s0 = 0;
    s1 = 255;
    s2 = 0;
    s3 = 0;
    break;
  case 3:
    s0 = 255;
    s1 = 255;
    s2 = 0;
    s3 = 0;
    break;
  case 4:
    s0 = 0;
    s1 = 0;
    s2 = 255;
    s3 = 0;
    break;
  case 5:
    s0 = 255;
    s1 = 0;
    s2 = 255;
    s3 = 0;
    break;
  case 6:
    s0 = 0;
    s1 = 255;
    s2 = 255;
    s3 = 0;
    break;
  case 7:
    s0 = 255;
    s1 = 255;
    s2 = 255;
    s3 = 0;
    break;
  case 8:
    s0 = 0;
    s1 = 0;
    s2 = 0;
    s3 = 255;
    break;
  case 9:
    s0 = 255;
    s1 = 0;
    s2 = 0;
    s3 = 255;
    break;
  case 10:
    s0 = 0;
    s1 = 255;
    s2 = 0;
    s3 = 255;
    break;
  case 11:
    s0 = 255;
    s1 = 255;
    s2 = 0;
    s3 = 255;
    break;
  case 12:
    s0 = 0;
    s1 = 0;
    s2 = 255;
    s3 = 255;
    break;
  case 13:
    s0 = 255;
    s1 = 0;
    s2 = 255;
    s3 = 255;
    break;
  case 14:
    s0 = 0;
    s1 = 255;
    s2 = 255;
    s3 = 255;
    break;
  case 15:
    s0 = 255;
    s1 = 255;
    s2 = 255;
    s3 = 255;
    break;
  default:
    break;

  }
  //set mux address
  digitalWrite(muxs0, s0);
  digitalWrite(muxs1, s1);
  digitalWrite(muxs2, s2);
  digitalWrite(muxs3, s3);
}

