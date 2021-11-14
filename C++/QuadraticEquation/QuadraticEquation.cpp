#include <iostream>
#include <string>
#include <math.h>
using namespace std;

#pragma region FunctionDeclarations
void CheckIfFloat(string input, size_t length);
float dValue(float a, float b, float c);
//float GetRoots(float a, float b, float d);
#pragma endregion

int main() {
	string input;
	float a, b, c;
	bool isAssigned[3] = { false, false, false };
	while (true) {
		try {
			if (isAssigned[0] == false)
			{
				cout << "a: ";
				cin >> input;
				size_t length = 0;
				a = stof(input, &length);
				CheckIfFloat(input, length);
				//a = atof(inputA.c_str());
				//cout << a << " " << typeid(a).name() << endl;
				isAssigned[0] = true;
			}
			if (isAssigned[1] == false)
			{
				cout << "b: ";
				cin >> input;
				size_t length = 0;
				b = stof(input, &length);
				CheckIfFloat(input, length);
				isAssigned[1] = true;
			}
			if (isAssigned[2] == false)
			{
				cout << "c: ";
				cin >> input;
				size_t length = 0;
				c = stof(input, &length);
				CheckIfFloat(input, length);
				isAssigned[2] = true;
			}
			break;
		}
		catch (...)
		{
			cout << "Illegal action, input has to be a valid number..." << endl;
			if (isAssigned[1] == false && isAssigned[0] == true)
			{
				cout << "a: " << a << endl;
			}
			else if (isAssigned[2] == false && isAssigned[1] == true)
			{
				cout << "a: " << a << endl;
				cout << "b: " << b << endl;
			}
		}
	}
	float d = dValue(a, b, c);
	//cout << d << endl;

	/*float ans[] = GetRoots(a, b, d);

	if () {
		cout << "This quadratic formula has 2 answers:" << endl << "1: " << ans[0] << endl << "2: " << ans[1] << endl;
	}
	else if () {
		cout << "This quadratic formula has 1 answer: " << ans[0] << endl;
	}
	else { cout << "This quadratic formula has 0 answers:" << endl; }*/

	if (d > 0)
	{
		float ans1 = (-b + sqrt(d)) / 2 * a;
		float ans2 = (-b - sqrt(d)) / 2 * a;
		//printf("This quadratic formula has 2 answers:\n1: %f\n2: %f", ans1, ans2);
		cout << "This quadratic formula has 2 answers:" << endl << "1: " << ans1 << endl << "2: " << ans2 << endl;
	}
	else if (d == 0)
	{
		float ans = (-b + sqrt(d)) / 2 * a;
		cout << "This quadratic formula has 1 answer: " << ans << endl;
	}
	else { cout << "This quadratic formula has 0 answers:" << endl; }
	while (true)
	{
		string command;
		cout << "try again? [y/n]: ";
		cin >> command;
		if (command == "y") { break; }
		else if (command == "n") { return 0; }
		else { cout << "Illegal action, input has to be a valid key..." << endl; }
	}
	main();
}


void CheckIfFloat(string input, size_t length) {
	if (input.size() != length) { throw; }
}


float dValue(float a, float b, float c) {
	return (pow(b, 2) - 4 * a * c);
}


//float GetRoots(float a, float b, float d) {
//	if (d>0) {
//		return ((-b + sqrt(d)) / 2 * a), ((-b - sqrt(d)) / 2 * a);
//	}
//	else if (d == 0) {
//		return (-b + sqrt(d)) / 2 * a;
//	}
//}


// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
