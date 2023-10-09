#include <Servo.h>

Servo myservo1;
Servo myservo2;

void setup() {
  myservo1.attach(9);
  myservo2.attach(10);
  Serial.begin(2400);
  Serial.setTimeout(500); // Set a timeout of 5000 milliseconds
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); // This will now timeout after 5 seconds
    int separatorIndex = data.indexOf(',');

    if(separatorIndex != -1) {
      int pos1 = data.substring(0, separatorIndex).toInt();
      int pos2 = data.substring(separatorIndex + 1).toInt();

      // Validation checks for the positions
      if (isValidMicroseconds(pos1) && isValidMicroseconds(pos2)) {
        myservo1.writeMicroseconds(pos1);
        myservo2.writeMicroseconds(pos2);
      } else {
        Serial.println("Invalid values received");
      }
    }
  }
}

bool isValidMicroseconds(int pos) {
  return (pos >= 700 && pos <= 2000); // validate that the position is within an acceptable range
}
