#include <iostream>
#include <algorithm>
#include <string>

int main() {
	int a = 10;
    int b = 2;
    float c = 1;
    while (a > b) {
     a -= 1;
     c += 2;
    }
    std::cout << c;
	return 0;
}