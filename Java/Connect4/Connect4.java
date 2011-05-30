//************************************************************************************
//  Name: Jonah Brooks         	Filename: BrooksJ_L3\Connect4.java
//  CS162  Spring 2010          Lab #: 3
//  Tues, Thurs 1:00 PM
//  Date:  Saturday April 10th, 2010
//
// 	Program Name: Connect4.java
//	Program Description:
//		A text based, two player version of Connect 4.
//		Wins are checked horizontally, vertically, and diagonally.
//		Up to 25 games can be played with the results recorded for each
//	Pseudocode:
//		Algorithms and pseudo code included in comments above applicable sections of code
//************************************************************************************


import java.io.*;
import java.util.Scanner;

class Connect4 {
	public final static int NOPLAYER = 0;
	public final static int PLAYER1 = 1;
	public final static int PLAYER2 = 2;

	//--------------------------------------------------------------------------------
	//	Main driver for the game
	//--------------------------------------------------------------------------------

	public static void main (String[] args) throws Exception
	{
		char again = 'Y';
		int player = PLAYER2;
		int winner = NOPLAYER;
		int games = 0;
		int moves = 0;
		boolean valid = false;
		Scanner scan = new Scanner(System.in);
		Board Myboard;
		Record[] records = new Record[25];

		while (again == 'Y')
		{	Myboard = new Board();
			winner = NOPLAYER;
			games++;
			moves = 0;
			Myboard.print();	// print board to the screen

			while (winner == NOPLAYER && moves < 64)	// 64 = number of moves in a Cat's Game
			{	player = (player == PLAYER1) ? PLAYER2 : PLAYER1;
					// prompt for, validate, and execute a move from the player
				System.out.print("Player "+player+" please select a column to make your move (0-7): ");
				valid = Myboard.move(player, scan.nextInt());
				while(!valid)	// if input was invalid
				{	System.out.print("That move is not allowed, please select a non-full column between 0 and 7: ");
					valid = Myboard.move(player, scan.nextInt());
				}
				Myboard.print();	// print new board to update the screen
				winner = Myboard.check_win();
				moves++;
			} // end while
			System.out.println ( (winner == 0) ? "Cat's Game!" : "Congratulations Player " + winner + "!!!");
			records[games-1] = new Record(winner, moves);	// store the record for this game

			if (games == 25)
				again = 'N';	// exit if the games played equals 25
			else	// otherwise prompt user
			{	System.out.print ("Do you want to play another game? (y/n): ");
				String word = scan.next();
				word = word.toUpperCase();
				again = word.charAt(0);
			} // end if
		} // end out while

		System.out.println("\n\n Thank you for playing!\nThe record of the games played is:");
		for(int i = 0; i < games; i++)
		{	System.out.print("(Game "+(i+1)+")\t\t");
			records[i].print();
		}
	} // end method main
} // end class Connect 4

//======================================================================================
//	Represents one player piece.
//======================================================================================
class Piece {
	private int owner;

	//----------------------------------------------------------------------------------
	//	Sets up a new piece, owned by neither player
	//----------------------------------------------------------------------------------
	public Piece()
	{	owner = Connect4.NOPLAYER;
	} // end constructor Piece

	public void print()
	{	char toPrint = ' ';	// to represent a piece owned by neither player
		if (owner == 2)
			toPrint = 'O';
		else if (owner == 1)
			toPrint = 'X';
		System.out.print(toPrint);
	} // end method print

	public void set_player(int player)
	{	owner = player;
	}

	public int get_player()
	{	return owner;
	}

	public boolean is_used()
	{	return (owner > 0);	// return whether or not a player owns the piece
	}

} // end class Piece

//======================================================================================
//	Represents the game board.
//======================================================================================
class Board {
	private Piece[][] pieces;
	private int last_row;	// store the row of the last move made
	private int last_col;	// store the column of the last move
	public Board()
	{	pieces = new Piece[8][8];
		for(int row = 0; row < 8; row++)
			for(int col = 0; col < 8; col++)
				pieces[row][col] = new Piece();	// instantiate each piece of the array
	} // end constructor Board

	//----------------------------------------------------------------------------------
	//	Validates and executes moves
	//----------------------------------------------------------------------------------
	public boolean move(int player, int col)
	{	boolean is_valid = true;
		int row = 7;	// start checks with the 'top' row
			// if the column is not within the bounds of the board, or the first slot is full
		if (col > 7 || col < 0 || pieces[row][col].is_used())
		{	is_valid = false;
		}
		else	// while the next slot down is "open"...
		{	while (row >= 0 && !pieces[row][col].is_used())
			{	row--;
			} // decrement row until it is just below the last valid slot
			pieces[row+1][col].set_player(player);	// can't get here at row == 7
		} // end else-if
		last_row = row+1;
		last_col = col;
		return is_valid;
	} // end method move

	//----------------------------------------------------------------------------------
	//	Prints the board to the screen.
	//----------------------------------------------------------------------------------
	public void print()
	{	for(int row = 8; row >= 0; row--)	// start with row 9 (index 8) to label columns
		{	for(int col = 0; col < 8; col++)
			{	if(row == 8)
					System.out.print(" "+col);
				else
				{	System.out.print("|");
					pieces[row][col].print();	// print each piece one at a time
				} // end if-else
			} // end inner for
			System.out.println( (row == 8) ? ' ' : '|');	// print the closing | then start a new line
		} // end outter for
		System.out.println("\n");	// print a couple blank lines to add space between frames
	} // end method print

	//----------------------------------------------------------------------------------
	//	Checks to see if a given player has any winning combination on the board
	//----------------------------------------------------------------------------------
	public boolean is_winner(int player)
	{	boolean won = false;
		int count = 0;
		Piece[] possible_win = new Piece[4];	// store an array of pieces that might be a winning combo
			//--------------------------------------------------------
			// Pseudo code:
			//	if it's possible to win vertically:
			//		check to see if the three pieces directly bellow the last one played are owned
			//			by the current player
			//	if player hasn't already won:
			//		parse through the current row counting up when a piece is owned by current player
			//		reset count if piece isn't owned by the current player
			//		if at any time count reaches 4, the player has won
			//  if player hasn't already won:
			// 		loop while temporary variables storing row and col are within bounds
			//			loop through this with tRow-- and tCol--
			// 			this will land the variables on whatever lower-left edge is in the diagonal
			// 			then loop through again going the other way and count each piece to check for a win
			//		reset variables and do the above step only mirror the row parts
			//			this will check for wins in upper-left to lower right diagonal
			//			  in other words, find the lower left to upper right diagonal which contains the piece
			//			  then check to see if that diagonal contains a win. Repeat for upper left - lower right
			//	return true if any of these checks came up as a win
			//----------------------------------------------------------

			// ------------ check for a vertical win ----------------------
		if(last_row >= 3) // if there are enough pieces in the column for a possible win
		{	won = true;	// be optimistic!
			for(int row = 3; row >= 0; row--)
				if (pieces[last_row-row][last_col].get_player() != player)
					won = false;
		}// end if, checking the 3 pieces directly beneath the last one placed

			// ------------ check for horizontal win -----------------
		if(won == false)
		{	for(int col = 0; col < 8; col++)	// parse the row of interest
			{	if(pieces[last_row][col].get_player() == player)
					count++;
				else
					count = 0;
				if(count == 4)
					won = true;
			} // end parsing for loop
		} // end the check for horizontal win

			// ------------ check for diagonal win -----------------
		if(won == false)
		{
			int tRow = last_row;
			int tCol = last_col;	// temp variables for current row and column for use in loops
			count = 0;
				// ------------- check for a \ type diagonal win ---------------------
			while (tRow<7 && tCol>0)
			{	// while the indices are within the bounds of the board
				tRow++;
				tCol--;
			} // this loop will trace the diagonal up and to the left, to whatever edge it hits first
			while (tRow>=0 && tCol<=7)
			{	// again while the indecies are within the bounds of the board
				if(pieces[tRow][tCol].get_player() == player)
					count++;
				else
					count = 0;
				if(count == 4)
				{	won = true;
				}
				tRow--;
				tCol++;
			} // this loop traces the diagonal back down and to the right, checking for a win combo

				// now to reset the temp variables and run this again
				// ----------- this time mirrored to check for / wins -----------------
			tRow = last_row;
			tCol = last_col;
			count = 0;
				// check for a / type diagonal win
			while (tRow>0 && tCol>0)
			{	// while the indices are within the bounds of the board
				tRow--;
				tCol--;
			} // this loop will trace the diagonal down and to the left, to whatever edge it hits first
			while (tRow<=7 && tCol<=7)
			{	// again while the indecies are within the bounds of the board
				if(pieces[tRow][tCol].get_player() == player)
					count++;
				else
					count = 0;
				if(count == 4)
				{	won = true;
				}
				tRow++;
				tCol++;
			} // this loop traces the diagonal back up and to the right, checking for a win combo
		} // end if, checking for a diagonal win

		return won;
	}

	//----------------------------------------------------------------------------------
	//	Checks if there are any winners at this point.
	//----------------------------------------------------------------------------------
	public int check_win()
	{	int result = Connect4.NOPLAYER;
		if(is_winner(Connect4.PLAYER1))
			result = Connect4.PLAYER1;
		else if (is_winner(Connect4.PLAYER2))
			result = Connect4.PLAYER2;
		return result;
	} // end method check_win
} // end class Board

//======================================================================================
//	Stores and displays the winning player and the number of moves taken in one game
//======================================================================================
class Record {
	private int player, moves;
	public Record(int argPlayer, int argMoves)
	{	player = argPlayer;
		moves = argMoves;
	}
	public void print()
	{	if(player == 0)
			System.out.println("Cat's Game~\t No winner, 64 moves");
		else
			System.out.println("Winner: Player "+player+"\t Total Moves: "+moves);
	}
} // end class Record