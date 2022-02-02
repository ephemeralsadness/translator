#include <iostream>
#include <algorithm>
#include <string>

int main() {
	int a = 10;
	int b = 2;
	float c = 1;
	do {
		a -= 1;
		c += 2;
	} while (a > b);
	
	std::cout << c;
	
	return 0;
}
