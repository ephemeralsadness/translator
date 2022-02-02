#include <iostream>
#include <algorithm>
#include <string>

int main() {
	int a = 21;
	a %= 5;
	float b = 3;
	float c = a / b;
	c -= 0.1;
	c = std::min(c, a);
	std::cout << c;
	
	return 0;
}
