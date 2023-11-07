int joyX, joyY;

void setup() {
  Serial.begin(9600);
}

void loop() {
  joyX = analogRead(A0);
  joyY = analogRead(A1);

  Serial.print(joyX);
  Serial.print(",");
  Serial.print(joyY);
  Serial.println();

  delay(100); // Adjust as needed
}
