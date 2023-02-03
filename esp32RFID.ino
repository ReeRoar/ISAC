#ifdef ESP32 //specify which libraries to pick if using either an esp32 or esp8266  
  #include <WiFi.h>
  #include <HTTPClient.h>
#else
  #include <ESP8266WiFi.h>
  #include <ESP8266HTTPClient.h>
  #include <WiFiClient.h>
#endif
#define RST_PIN         22         
#define SS_PIN          5         
#include <SPI.h>
#include <MFRC522.h>
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
//MFRC522::MIFARE_Key key; // Will hold the card information

//Network credentials
const char* ssid     = "Frontier3200"; //change if connecting to another network
const char* password = "8352347965";   //change if connecting to another network

const char* serverName = "http://192.168.254.156/post-esp-data.php"; //change IP address if connected to another network
String apiKeyValue = "tPmAT5Ab3j7F9";

void setup() {
  Serial.begin(5000);
 //Serial.println("http://192.168.254.156/post-esp-data.php");
  SPI.begin();     
  rfid.PCD_Init();   

 //for(byte i=0;i<6;i++)
 // {
 //   key.keyByte[i]=0xFF; // Prepare the security key for the read and write functions.
 // }
  
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.println(".....");
  }
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
    
  if ( ! rfid.PICC_ReadCardSerial())
    return;
  
  if(WiFi.status()== WL_CONNECTED){
    WiFiClient client;
    HTTPClient http;
    
    http.begin(client, serverName);
    
    // Specify content-type header
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
  String CardID ="";
  for (byte i = 0; i < rfid.uid.size; i++) {
    CardID += rfid.uid.uidByte[i];
  }
   Serial.println("");
   Serial.println("Scanned ID number: " + CardID + "\n");
   
    // Preparing HTTP POST request data
    String httpRequestData = "api_key=" + apiKeyValue + "&id=" + CardID + "";
    Serial.print("httpRequestData: ");  //This is only for testing when connected to a computer.
    Serial.println(httpRequestData);
    
    // Send HTTP POST request
    int httpResponseCode = http.POST(httpRequestData);
        
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode); // A 200 code means that the request succeeded. 
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Close connection
    http.end();
  }
  else {
    Serial.println("WiFi Disconnected");
  }
  // Sends the scanned card HTTP POST request every second
  delay(1000);  
}
