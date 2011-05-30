//******************************************************************************
//  Name: Jonah Brooks          Filename: BrooksJ_L4/BrooksJL4.cpp
//  CS133u Spring 2010          Lab #: 4
//  Mon, Wed 12:30
//  Date:  04/24/2010
//
//  Program Description:
//      Asks for the width, depth, and starting height of a box, then produces
//      a table of values detailing the area and volume of a box of those
//      dimensions, as well as boxes of similar dimensions but varying heights.
//  Pseudocode:
//      Declare int variables for height, depth, and width.
//      Call intro() to introduce the program to the user.
//      Call promptStats() to get the height, depth, and width from the user.
//          (use cin to assign input to pass by reference variables)
//      Send that input to makeTable()
//        which will then call volume() and surfaceArea() to get remaining data
//          (volume returns: height * depth * width   as an int)
//          (surfaceArea returns: 2(height*width + height*depth + depth*width) )
//        then it will print the table to the screen using cout and setw
//      Finally, call volume and surfaceArea from main just for the fun of it~
//  Test Oracle:
//   (input: height = 5, depth = 10, width = 4)
//      Depth:      Width:      Height:      Area:      Volume:
//        10          4           5          220          200    
//        10          4           7          276          280
//        10          4           9          332          360
//        10          4          11          388          440
//                      (etc, etc)
//      Also, if all the dimensions of the box were doubled:
//      The area would be   : 880
//      The volume would be : 1600       
//******************************************************************************
#import <iostream>
#import <iomanip>
using namespace std;

// function protoypes
void intro();
void promptStats(int& height, int& depth, int& width);
void verify(int& input);
void makeTable(int height, int depth, int width);
int volume(int height, int depth, int width);
int surfaceArea(int height, int depth, int width);

//*****************************************************************************
//*  main function. Calls the other functions to print a table containing the *
//*  volume and surface area of various boxes based on use input.             *
//*****************************************************************************
int main()
{   int height = 0, depth = 0, width = 0;
    
    intro();    // introduce the program to the user
    promptStats(height, depth, width);  // prompt user to input starting stats
    makeTable(height, depth, width);    // generate output table
    
    cout << "Also, if all the dimensions of this box were doubled: \n";
    cout << "The area would be   : " << surfaceArea(height*2,depth*2,width*2);
    cout << endl;
    cout << "The volume would be : " << (8*volume(height,depth,width));
        
    cin.ignore(9999, '\n');
    cin.get();
    return 0;
} // end main()

//*****************************************************************************
//* intro function. Prints a program introduction to the screen               *
//*****************************************************************************
void intro()
{   cout << "Welcome to the volumes and areas of boxes with differing heights "
         << "Program!\n";
    cout << "This program will calculate the area and volume of a given box.\n";
    cout << "It will then calculate the same for other boxes of "
         << "various heights.\n\n";
}

//*****************************************************************************
//* promtStats function. Prompts user for the box's starting dimensions, then *
//* stores this input back in the int reference variables sent as parameters  *
//*****************************************************************************
void promptStats(int& height, int& depth, int& width)
{   cout << "Please enter the starting dimension of the box to be calculated.";
    cout << "\nInitial Height: ";
    cin >> height;
    verify(height);
    cout << "Depth (length): ";
    cin >> depth;
    verify(depth);
    cout << "Lastly, width : ";
    cin >> width;
    verify(width);
} // end promptStats()

//*****************************************************************************
//* verify function. Verifies the validity of user input. Reassigns reference *
//* arguments when valid input has been gathered.                             *
//*****************************************************************************
void verify(int& input)
{   while(input <=0 || input > 1200)   // prevent negative, zero, and overflow
    {   cout << ((input>1200) ? ("No boxes bigger than my appartment please."):
                                ("... that's not even possible."));
        cout << "\nPlease input a number between 1 and 1200: ";
        cin >> input;   // pass by reference = reasigning original variable
    } // end while
} // end verify()

//*****************************************************************************
//* makeTable function. Accepts ints for the dimensions of the box, passes    *
//* those variables on to the volume and surfaceArea functions, then uses     *
//* all these values to print the final output table for the user             *
//***************************************************************************** 
void makeTable(int height, int depth, int width)
{   cout << "\nDepth:\tWidth:\tHeight:\tArea:\tVolume:\n";
    for(int i = 0; i < 7; i++)
    {   cout << setw(4) << depth << "\t" << setw(4) << width << "\t" 
             << setw(4) << height << "\t"
             << setw(4) << surfaceArea(depth,width,height) << "\t" 
             << setw(4) << volume(depth,width,height) << endl;
        height += 2;
    } // end for
    cout << endl;
} // end makeTable()

//*****************************************************************************
//* volume function. Accepts ints for dimensions of the box, then calculates  *
//* the volume of the box. Returns this calculated volume.                    *
//*****************************************************************************
int volume(int height, int depth, int width)
{       // calculate volume, then return it
    return height*width*depth;
} 

//*****************************************************************************
//* surfaceArea function. Accepts ints for dimensions of the box, then        *
//* calculates the total surface area of the box. Returns this calculated area*
//*****************************************************************************
int surfaceArea(int height, int depth, int width)
{      // calculate total surface area, then return it
    return 2*(height*width + height*depth + depth*width);
} 
