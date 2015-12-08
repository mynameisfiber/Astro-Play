/*
void setLEDs(){
  //this could be seriously optimized, who cares, get it done for now
  switch(mode){
  case 0: //mode- all off
    //setMux1( 0);
    digitalWrite(led1, LOW);
    //setMux1( 1);
    digitalWrite(led2, LOW);
    //setMux1( 2);
    digitalWrite(led3, LOW);
    break;
  case 1: //mode 1
    //setMux1( 0);
    if(sendCode == 0){ //if we are not sending code
      digitalWrite(led1, HIGH); //solid
    }
    else{
      digitalWrite(led1, HIGH); //solid
      delay(blinkT);
      digitalWrite(led1, LOW); //blink
      delay(blinkT);
      digitalWrite(led1, HIGH); //blink
      delay(blinkT);
      digitalWrite(led1, LOW); //blink
      delay(blinkT);
      digitalWrite(led1, HIGH); //blink
      delay(blinkT);
      digitalWrite(led1, LOW); //blink
      delay(blinkT);
      digitalWrite(led1, HIGH); //blink
      delay(blinkT);
    }
    digitalWrite(led2, LOW);
    //setMux1( 1);
    digitalWrite(led3, LOW);
    //setMux1( 2);

    break;
  case 2: //mode 2
    //setMux1( 1);
    if(sendCode == 0){ //if we are not sending code
      digitalWrite(led2, HIGH); //solid
    }
    else{
      digitalWrite(led2, HIGH); //solid
      delay(blinkT);
      digitalWrite(led2, LOW); //blink
      delay(blinkT);
      digitalWrite(led2, HIGH); //blink
      delay(blinkT);
      digitalWrite(led2, LOW); //blink
      delay(blinkT);
      digitalWrite(led2, HIGH); //blink
      delay(blinkT);
      digitalWrite(led2, LOW); //blink
      delay(blinkT);
      digitalWrite(led2, HIGH); //blink
      delay(blinkT);
    }

    digitalWrite(led1, LOW);

    digitalWrite(led3, LOW);


    break;
  case 3: //mode 3
   // setMux1( 2);
    if(sendCode == 0){ //if we are not sending code
      digitalWrite(led3, HIGH); //solid
    }
    else{
      digitalWrite(led3, HIGH); //solid
      delay(blinkT);
      digitalWrite(led3, LOW); //blink
      delay(blinkT);
      digitalWrite(led3, HIGH); //blink
      delay(blinkT);
      digitalWrite(led3, LOW); //blink
      delay(blinkT);
      digitalWrite(led3, HIGH); //blink
      delay(blinkT);
      digitalWrite(led3, LOW); //blink
      delay(blinkT);
      digitalWrite(led3, HIGH); //blink
      delay(blinkT);
    }
    digitalWrite(led1, LOW);
   // setMux1( 1);
    digitalWrite(led2, LOW);
   // setMux1( 0);

    break;
  }
}
*/

void checkButtons() {
  if ( digitalRead(button1) == LOW) {
    delay (10);
    buttonPress1 = true; //button1 has been pressed
    //Serial.println("button1 pressed");
  }
  else if (digitalRead(button1) == HIGH && buttonPress1) { //button1 has been pressed and released
    buttonPress1 = false;
    if (mode == 1) {
      sendCode = 1; //set flag for send code to output
      //Serial.println("button1 released 2");
    }
    else {
      mode = 1; //entering new mode (mode 1)
      //Serial.println("button1 released 1");
    }
  }


  // check button 2
  if (digitalRead(button2) == LOW) {
    delay (10);
    buttonPress2 = true; //button2 has been pressed
    //Serial.println("button2 pressed");
  }
  else if (digitalRead(button2) == HIGH && buttonPress2) { //button2 has been pressed and released
    buttonPress2 = false;
    if (mode == 2) {
      sendCode = 1; //set flag for send code to output
      //Serial.println("button2 released 2");
    }
    else {
      mode = 2; //entering new mode (mode 2)
      //Serial.println("button2 released 1");
    }
  }




  // check button 3
  if (digitalRead(button3) == LOW) {
    delay (10);
    buttonPress3 = true; //button2 has been pressed
    //Serial.println("button3 pressed");
  }
  else if (digitalRead(button3) == HIGH && buttonPress3) { //button3 has been pressed and released
    buttonPress3 = false;
    if (mode == 3) {
      sendCode = 1; //set flag for send code to output
      //Serial.println("button3 released 2");
    }
    else {
      mode = 3; //entering new mode (mode 2)
      //Serial.println("button3 released 1");
    }
  }

 // check button 4
  if (digitalRead(button4) == LOW) {
    delay (10);
    buttonPress4 = true; //button2 has been pressed
    //Serial.println("button3 pressed");
  }
  else if (digitalRead(button4) == HIGH && buttonPress4) { //button4 has been pressed and released
    buttonPress4 = false;
    runPause = 1; //button was pressed and released
    //newMode = true;
   // mode = 4; //entering new mode (mode 2)
    //Serial.println("button3 released 1");

  }
  
}
