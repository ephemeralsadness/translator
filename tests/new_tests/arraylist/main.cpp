#include <iostream>
#include <algorithm>
#include <string>
#include <vector>

int main() {
	std::vector<int> v;
	for (int i = 0; i < 10; i += 1) {
		v.push_back(i);
	}
	
	for (int i = 0; i < 5; i += 1) {
		v.erase(v.begin() + (0));
	}
	
	std::cout << v.empty() << std::endl;
	std::cout << v.size() << std::endl;
	for (int i = 0; i < 5; i += 1) {
		std::cout << v[i];
	}
	
	std::cout << (v.end() != std::find(v.begin(), v.end(), 8)) << std::endl;
	
	return 0;
}
