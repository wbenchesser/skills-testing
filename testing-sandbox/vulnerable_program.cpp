#include <iostream>
#include <cstring>

// Function with buffer overflow vulnerability
void processInput(const char* userInput) {
    char buffer[10];
    // Buffer overflow - no bounds checking!
    strcpy(buffer, userInput);
    std::cout << "Processed: " << buffer << std::endl;
}

// Function with use-after-free vulnerability
int* createArray() {
    int* arr = new int[5];
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 10;
    }
    delete[] arr;
    // Returning pointer to freed memory!
    return arr;
}

// Function with heap buffer overflow
void heapOverflow() {
    int* array = new int[5];
    // Writing beyond allocated bounds
    for (int i = 0; i <= 10; i++) {
        array[i] = i * 2;
    }
    delete[] array;
}

// Function with stack buffer overflow
void stackOverflow(int index) {
    int stack_array[5];
    // No bounds checking on index
    stack_array[index] = 42;
    std::cout << "Set stack_array[" << index << "] = 42" << std::endl;
}

int main() {
    std::cout << "=== Testing Vulnerable Program ===" << std::endl;

    // Test 1: Buffer overflow
    std::cout << "\n1. Testing buffer overflow..." << std::endl;
    processInput("This is a very long string that will overflow the buffer");

    // Test 2: Use-after-free
    std::cout << "\n2. Testing use-after-free..." << std::endl;
    int* leaked = createArray();
    std::cout << "Accessing freed memory: " << leaked[0] << std::endl;

    // Test 3: Heap buffer overflow
    std::cout << "\n3. Testing heap overflow..." << std::endl;
    heapOverflow();

    // Test 4: Stack buffer overflow
    std::cout << "\n4. Testing stack overflow..." << std::endl;
    stackOverflow(10);  // Out of bounds index

    std::cout << "\n=== Program Complete ===" << std::endl;
    return 0;
}
