String trayVals = "{";
int mode = 0; // mode 1 is programming, mode 2 is robot, mode 3 is music, mode 4 is printer
int sendCode;
boolean buttonPress1;
boolean buttonPress2;
boolean buttonPress3;
boolean buttonPress4;
int runPause;//for fourth button
int blinkT = 100;
int currentBlock;


int j; //subMux pin#
int k; //subMux#

int blockCount = 0;

void setup() {
  pinMode(2, INPUT); //b1
  pinMode(3, INPUT); //b2
  pinMode(4, INPUT); //b3
  pinMode(A6, INPUT); //b4
  digitalWrite(2, HIGH); //pullup
  digitalWrite(3, HIGH); //pullup
  digitalWrite(4, HIGH); //pullup
  //digitalWrite(A6, HIGH); //pullup for fourth button (nonfunctional with mini circuit)
  // pinMode(5, OUTPUT); //l1
  // pinMode(6, OUTPUT); //l2
  // pinMode(7, OUTPUT); //l3
  pinMode(8, OUTPUT); //m1 s0
  pinMode(9, OUTPUT); //m1 s1
  pinMode(10, OUTPUT); //m1 s2
  pinMode(11, OUTPUT); //m1 s3
  pinMode(A0, INPUT); //m1 z
  pinMode(12, OUTPUT); //m2 s0
  pinMode(5, OUTPUT); //m2 s1
  pinMode(6, OUTPUT); //m2 s2
  pinMode(7, OUTPUT); //m2 s3
  pinMode(A1, INPUT); //m2 z
  pinMode(13, OUTPUT); //m3 s0
  pinMode(A3, OUTPUT); //m3 s1
  pinMode(A4, OUTPUT); //m3 s2
  pinMode(A5, OUTPUT); //m3 s3
  pinMode(A7, INPUT); //m3 z
  pinMode(A2, OUTPUT); //LED

  Serial.begin(57600);


}

int button1 = 2;
int button2 = 3;
int button3 = 4;
int button4 = 20;
int led1 = A2;
//int led2 = 6;
//int led3 = 7;


void loop() {
  checkButtons();
  //pull mux 1 E low

  //setup API string (Not needed)
  readBlocks(); //reads and adds values to API
  //end API string
  //setLEDs();
  //pull mux 1 E high

  endTrayString();
  //send string
  Serial.println(trayVals);
  //clear string and sendCode val
  trayVals = "";
  sendCode = 0;
  runPause = 0; //reset button 4
}
