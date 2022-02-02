#include <iostream>
#include <algorithm>
#include <string>

void func() {
	int a = 1;
}

float get_number_divided_by_two(float a) {
	return a / 2;
}

int main() {
	func();
	int a = 15;
	a = get_number_divided_by_two(a);
	std::cout << a;
	
	return 0;
}
