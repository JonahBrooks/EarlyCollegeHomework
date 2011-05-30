//******************************************************************************
//  Name: Jonah Brooks          Filename: BrooksJ_L9/BrooksJL9.cpp
//  CS133u Spring 2010          Lab #: 9
//  Mon, Wed 12:30
//  Date:  05/31/2010
//
//  Program Description:
//      Stores a user defined number of test scores, prints them to the screen,
//      and finds and prints the average of all test scores input by the user.
//  Pseudocode:
//      Introduce the program
//      Ask user for a number of scores to be input
//      Create an array of the input size to store the scores
//      Loop through and prompt user for each element of the array, validate
//      Call the Sort function to sort the array with selection sort
//      Print the list of now-sorted scores
//      Call, and print the results from, the Average function
//  Test Oracle:
//      Input: 10 -> 100, 56, 78, 32, 67, 85, 46, 98, 67, 87
//      Output: [one line each] #1: 32      #2: 46      #3: 56      #4: 67
//      #5: 67      #6: 78      #7: 85      #8: 87      #9: 98      #10: 100
//          Average of: 71.6
//******************************************************************************

#include <iostream>
#include <iomanip>
using namespace std;

void Sort(int* array, int size);  // sorts the array with selection sort
double Average(int* array, int size); // returns the average of array values 

int main()
{
    int* scores = 0;
    int numScores = 0;
    double ave = 0.0;
    cout << "Welcome to this program. It sorts and averages test scores.";
    cout << "\n\nHow many test scores would you like to enter?: ";
    cin >> numScores;
    while(numScores <=0)
    {   cout << "Invalid input: Please enter a positive number of scores: ";
        cin >> numScores;
    }
    scores = new int[numScores];    // allocate memory for the array
    
    cout << "\nThank you. Now, please enter each score as prompted";
    for(int i = 0; i < numScores; i++)
    {   cout << "\nScore #" << (i+1) << ": ";
        cin >> *(scores+i); // assign input to next element of the array
        while(*(scores+i) < 0)
        {   cout<<"Invalid input: Negative scores are not allowed. Try again: ";
            cin >> *(scores+i);
        }
    } // end for
    
    Sort(scores, numScores);   // sort scores array
    cout << "\nThank you. Now sorting....";
    for(int i = 0; i < numScores; i++) // print the scores to the screen
    {   cout << "\n#" << (i+1) << ": " << *(scores+i); 
    }
    ave = Average(scores, numScores);
    cout <<"\nAnd the average score for the above list is: " 
          << ave; 
    
    cin.ignore(9999,'\n');
    cin.get();
    return 0;
}
//--------------------------------------------------------------------
//- Sort(): Uses selection sort to sort the argument array           -
//--------------------------------------------------------------------
void Sort(int* array, int size)
{
    int temp = 0;
    int min = 0; // an index for use in the selection sort
    
    for(int base = 0; base < size-1; base++)  // step through each element
    {   min = base;
        for(int check = base+1; check < size; check++)
        {   if(*(array+check) < *(array+min))
                min = check;
        }
        if(base != min) // if a smaller number was found
        {   temp = *(array+base);
            *(array+base) = *(array+min); // switch min and base
            *(array+min) = temp;
        } // end if
    } // end outer for 
} // end Sort()
    
//---------------------------------------------------------------------
//- Average(): Returns the average of all ints in the argument array  -
//---------------------------------------------------------------------
double Average(int* array, int size)
{
    double toReturn = 0.0;
    int total = 0;
    for(int i = 0; i < size; i++)
        total += *(array+i);
    toReturn = static_cast<double>(total)/size;
    return toReturn;
} // end Average()  
