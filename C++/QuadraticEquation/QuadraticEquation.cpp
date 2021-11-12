// QuadraticEquation.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <cmath>
using namespace std;

int main()
{
	float a = NULL;
	float b = NULL;
	float c = NULL;
    while (true)
    {
		try
		{
			if (a == NULL)
			{
				cout << "a: ";
				cin >> a;
				/*if (typeid(a) != typeid(float))
				{
					throw a;
				}*/
			}
			if (b == NULL)
			{
				cout << "b: ";
				cin >> b;
			}
			if (c == NULL)
			{
				cout << "c: ";
				cin >> c;
			}
			break;
		}
		catch (...)
		{
			cout << "Illegal action, input has to be a valid number..." << endl;
			if (b == NULL)
			{
				cout << "a: " << a << endl;
			}
			else if (c == NULL)
			{
				cout << "a: " << a << endl;
				cout << "b: " << b << endl;
			}
		}
    }
	float d = pow(b, 2) - 4 * a * c;
	//cout << d << endl;
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
	else
	{
		cout << "This quadratic formula has 0 answers:" << endl;
	}
	while (true)
	{
		string command;
		cout << "try again? [y/n]: ";
		cin >> command;
		if (command == "y")
		{
			break;
		}
		else if (command == "n")
		{
			return 0;
		}
		else
		{
			cout << "Illegal action, input has to be a valid key..." << endl;
		}
	}
	main();
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file