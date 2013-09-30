#define resolution 8
#define mains 50 // 60: north america, japan; 50: most other places

#define refresh 2 * 1000000 / mains

// Counter for the timer
extern volatile unsigned long timer0_overflow_count;

/* === */
/* ??? */
void startTimer() {
    timer0_overflow_count = 0;
    TCNT0 = 0;
}

unsigned long checkTimer() {
    return ((timer0_overflow_count << 8) + TCNT0) << 2;
}

long time(int pin, byte mask) {
    unsigned long count = 0, total = 0;
    
    while(checkTimer() < refresh) {
        // pinMode is about 6 times slower than assigning
        // DDRB directly, but that pause is important
        pinMode(pin, OUTPUT);
        PORTB = 0;
        
        pinMode(pin, INPUT);
        
        while((PINB & mask) == 0)
            count++;
            
        total++;
    }
    startTimer();
    return (count << resolution) / total;
}

/* ??? */
/* === */

void setup() {
    // Initialize serial communication
    Serial.begin(115200);
    
    // INPUT on pin 8
    pinMode(8, INPUT);
    
    // Start timer
    startTimer();
}

void loop() {
    // Print output to serial in decimal
    Serial.print(time(8, B00000001), DEC);
    Serial.print(" ");
}
