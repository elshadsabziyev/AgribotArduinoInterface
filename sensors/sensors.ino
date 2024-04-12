#include <DHT.h>
#include <DHT_U.h>
#define DHTPin 2
#define DHTTYPE DHT11
#define soilMoistureSensorPin A0
#define waterLevelSensorPin A1
#define relayPin 8

DHT dht(DHTPin, DHTTYPE);

void setup()
{
    Serial.begin(9600);
    pinMode(relayPin, OUTPUT);
    pinMode(soilMoistureSensorPin, INPUT);
    dht.begin();
    Serial.println("Reading From the Sensor ...");
    delay(2000);
}

void loop()
{
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    int soilMoisture = analogRead(soilMoistureSensorPin);
    soilMoisture = map(soilMoisture, 1023, 0, 0, 100);
    int waterLevel = analogRead(waterLevelSensorPin);
    waterLevel = map(waterLevel, 1023, 0, 0, 100);
    String pumpState = (digitalRead(relayPin) == HIGH) ? "OFF" : "ON";

    if (soilMoisture < 25)
    {
        digitalWrite(relayPin, LOW);
    }
    else
    {
        digitalWrite(relayPin, HIGH);
    }

    // Write the data to the serial port
    Serial.print("<");
    Serial.print(humidity);
    Serial.print(",");
    Serial.print(temperature);
    Serial.print(",");
    Serial.print(soilMoisture);
    Serial.print(",");
    Serial.print(waterLevel);
    Serial.print(",");
    Serial.print(pumpState);
    Serial.println(">");

    delay(100); // Wait for 100 milliseconds
}
