int R1 = 2;
int R2 = 3;
int R3 = 4;
int R4 = 5;
int R5 = 6;
int R6 = 7;
int R7 = 8;
int R8 = 9;
int sW1 = 12;
int volt;

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);
  pinMode(R3, OUTPUT);
  pinMode(R4, OUTPUT);
  pinMode(R5, OUTPUT);
  pinMode(R6, OUTPUT);
  pinMode(R7, OUTPUT);
  pinMode(R8, OUTPUT);
  pinMode(sW1, INPUT_PULLUP);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming data as a String until a newline character is received
    String commandData = Serial.readStringUntil('\n');
    // Remove the first '<' and the last '>' for easier parsing
    if (commandData.startsWith("<") && commandData.endsWith(">")) {
      commandData = commandData.substring(1, commandData.length() - 1);
      processCommand(commandData);
    }
  }
}

void processCommand(String command) {
  // Split the command into its parts using a tokenizer
  int relayStates[8];  // Array to hold the state of each relay
  int i = 0;
  int fromIndex = 0;
  int commaIndex = command.indexOf(',', fromIndex);

  while (commaIndex != -1 && i < 8) {
    relayStates[i++] = command.substring(fromIndex, commaIndex).toInt();
    fromIndex = commaIndex + 1;
    commaIndex = command.indexOf(',', fromIndex);
  }

  // Get the last value after the last comma
  if (i < 8) {
    relayStates[i] = command.substring(fromIndex).toInt();
  }

  // Activate relays according to the parsed command
  activateRelays(relayStates);
}

void activateRelays(int relayStates[8]) {
  int pins[8] = {R1, R2, R3, R4, R5, R6, R7, R8};
  String pinNames[8] = {"R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"};

  // First set to 255 if state is 1
  for (int i = 0; i < 8; i++) {
    if (relayStates[i] == 1) {
      analogWrite(pins[i], 255);
      }
    else {
      analogWrite(pins[i], 0); // Ensure pins are set to 0 if state is 0
    }
  }

  delay(500); // Wait for 500ms

  // Then set to 125 if state is 1
  for (int i = 0; i < 8; i++) {
    if (relayStates[i] == 1) {
      analogWrite(pins[i], 125);
      if (pins[i] == R3){
        volt = digitalRead(sW1);
        while (volt == 0){
          delay(10);
          volt = digitalRead(sW1);
          if (volt == 1){
            analogWrite(pins[i],0);
            break;
          }
        }
      }
    } else {
      analogWrite(pins[i], 0); // Ensure pins remain at 0 if state is 0
    }
  }
  Serial.println(volt);
  Serial.println("OK");
}
