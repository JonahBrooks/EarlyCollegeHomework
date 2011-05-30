//***************************************************************************************
//* Name: Jonah Brooks         	Filename: BrooksJ_L4\Hydra.java						    *
//*												 ...\LList.java							*
//*												 ...\ListInterface.java					*
//* CS260  Spring 2011          Lab #: 4												*
//* Date:  Tuesday April 26th, 2011														*
//*																						*
//*	Program Name: Hydra.java															*
//* Program Description:																*
//*		This program uses an LList of Strings to simulate a hydra. It accepts a String	*
//*		from the user and then systematically "kills" the hydra by removing a letter	*
//*		from the String and creating two copies of the new String.						*
//*																						*
//*		LList.java was modified to store the address of the last element of the list	*
//*		in order to optimize adding elements to the end of the list.					*
//*																						*
//*	Pseudocode:																			*
//*		Create two LList<String> objects (one for each strategy) and a Scanner object	*
//*		Prompt the user for a String, accept it, then place it in both LLists			*
//*		Loop for Strategy 1 (processing the first LList):								*
//*			Remove the element at position 1 of the LList								*
//*			Get the substring of this element from 1 to length							*
//*			Add this new String to the begging of the LList two times					*
//*			Repeat, since the first String in the list will always be the smallest		*
//*		Loop for Strategy 2 (processing the second LList):								*
//*			Remove the element at position 1 of the LList								*
//*			Get the substring of this element from 1 to length							*
//*			Add this new String to the end of the LList two times						*
//*			Repeat, since the first Stringin the list will always be the largest		*
//***************************************************************************************
import java.util.Scanner;
public class Hydra
{
	public static void main(String[] args)
	{
		Scanner sysIn = new Scanner(System.in);
		String hydraString;
		LList<String> Hydra = new LList<String>();
		long startTime;

		System.out.print("Enter a String to slay like a Hydra: ");
		hydraString = sysIn.nextLine();

			// Only adding/removing from the first position of the LList gives us an O(2^n) operation
		Hydra.add(hydraString);
		startTime = System.currentTimeMillis();
		while(!Hydra.isEmpty())
		{
			String currentHead = Hydra.remove(1);
			if(currentHead.length() > 1)
			{	String newHead = currentHead.substring(1,currentHead.length());
				Hydra.add(1,newHead);
				Hydra.add(1,newHead);
			}
			//Hydra.display();
		}
		System.out.println("Method 1 took: " + (System.currentTimeMillis() - startTime) +
							" milliseconds to complete\n");

		// Given the changes I made to LList that let us quickly access the last element
		// we now still have an O(2^n) operation
		Hydra.add(hydraString);
		startTime = System.currentTimeMillis();
		while(!Hydra.isEmpty())
		{
			String currentHead = Hydra.remove(1);
			if(currentHead.length() > 1)
			{	String newHead = currentHead.substring(1,currentHead.length());
				Hydra.add(newHead);
				Hydra.add(newHead);
			}
			//Hydra.display();
		}
		System.out.println("Method 2 took: " + (System.currentTimeMillis() - startTime) +
							" milliseconds to complete");
	}
}