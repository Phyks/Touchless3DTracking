/* Touchless tracking
 * ==================
 * This code takes as many measurements as it can at approximately
 * 10Hz = 60 Hz / (2 full cycles * 3 sensors).
 *
 * The code takes as many measurements as possible on the period of two
 * cycles of the main power frequency, in order to cancel out any potential
 * coupling.
 *
 * Original code was found on instructables :
 * http://www.instructables.com/id/DIY-3D-Controller/
 *
 * Code slightly modified and commented by Phyks for HackENS
 *
 * As I found the code on Instructables and I don't give a damn to the 
 * modifications I made, you may reuse it freely by writing where you 
 * found it.
 */

#define resolution 8
// Frequency of main power to avoid coupling
#define mains 50
// Time between measures
#define refresh 2 * 1000000 / mains

// Pins to use
// Must be between 8 and 13 to use this code without 
// modifications (PORTB is for pins 8 to 13)
//
// Note : If you change pin numbers, you *must* change the mask.
//        See arduino doc for more info.
#define PIN_R 8
#define MASK_R B00000001
#define PIN_G 9
#define MASK_G B00000010
#define PIN_B 10
#define MASK_B B00000100

// Counter for the timer
extern volatile unsigned long timer0_overflow_count;

void startTimer() {
    timer0_overflow_count = 0;
    TCNT0 = 0; // Initialize counter value to 0
}

unsigned long checkTimer() {
    return ((timer0_overflow_count << 8) + TCNT0) << 2;
}

long time(int pin, byte mask) {
    unsigned long count = 0, total = 0;

    while(checkTimer() < refresh) {
        // Note : pinMode is about 6 times slower than assigning
        // DDRB directly, but that pause is important

        // Set pin as output and LOW, see arduino doc for info on PORTB
        pinMode(pin, OUTPUT);
        PORTB = 0;

        // Set it as INPUT to take measure
        pinMode(pin, INPUT);

        // While PINB is low, increment counter
        while((PINB & mask) == 0)
            count++;

        total++;
    }
    // Restart timer for next measurement
    startTimer();
    // Return the measurement result
    return (count << resolution) / total;
}

void setup() {
    // Initialize serial communication
    Serial.begin(115200);

    // INPUT on pins
    pinMode(PIN_R, INPUT);
    pinMode(PIN_G, INPUT);
    pinMode(PIN_B, INPUT);

    // Start timer
    startTimer();
}

void loop() {
    // Print output to serial in decimal
    Serial.print(time(PIN_R, MASK_R), DEC);
    Serial.print(" ");

    Serial.print(time(PIN_G, MASK_G), DEC);
    Serial.print(" ");

    Serial.print(time(PIN_B, MASK_B), DEC);
    Serial.print("\n");
}
