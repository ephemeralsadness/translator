#include <iostream>
#include <algorithm>
#include <string>

int main() {
	int a = 10;
	int b = 2;
	float c = 1;
	for (int i = a; i < b; i -= 1) {
		c += 2;
	}
	
	std::cout << c;
	
	return 0;
}
