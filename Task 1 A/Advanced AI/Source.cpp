#include <iostream>
#include <string>
#include <map>
#include <vector>

float RareDisease(float PD, float PTD, float PNTND);
float GetValue();

int main()
{
	std::cout << "|			Advanced AI			|" << std::endl;
	std::cout << "P(d|t): " << RareDisease(float(1.0f / 10000.0f), 0.99f, 0.95f) << std::endl;
	std::cout << "P(d|t): " << RareDisease(GetValue(), GetValue(), GetValue()) << std::endl;
	
	return 0;
}

//P( d ) : prior probability of having a disease
//P( t | d ) : probability that the test is positive given the person has the disease
//P( ¬t | ¬d) : probability that the test is negative given the person does not have the disease

//d: the person has the disease
//t: the test is positive 
float RareDisease(float PD, float PTD, float PNTND)
{
	//P(d|t)
	//P(t|¬d) = 1 - P(¬t|¬d)
	float PTND = 1 - PNTND;
	//P(t)
	float PT = (PTD * PD) + (PTND * 1 - PD);
	//P(d|t)
	float PDT = (PTD * PD) / PT;

	return PDT;
}

float GetValue()
{
	std::cout << "Please Enter Your Value: ";
	float Return;
	std::cin >> Return;
	return Return;
}