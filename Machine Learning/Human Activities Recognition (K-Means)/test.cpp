#include <iostream>
#include <fstream>
using namespace std;

int main()
{
	ifstream file("a.txt");
	double val[3], tmp;
	int i = 0;
	while(file >> tmp)
	{
		val[i] = tmp;
		i++;
	}
	for(i = 0; i < 3; i++)
		cout << "val[i]: " << val[i] << " ";
	return 0;
}
