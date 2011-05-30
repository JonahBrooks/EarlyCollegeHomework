//************************************************************************************
//  Name: Jonah Brooks         	Filename: BrooksJ_L7\Lab7.java
//  CS162  Spring 2010          Lab #: 7
//  Tues, Thurs 1:00 PM
//  Date:  Monday May 17th, 2010
//
// 	Program Name: Lab7.java	and	SortPanel.java
//	Program Description:
//		Sorts a bar graph in slow motion using a selection sort algorithm and a timer
//	Pseudocode:
//		set AXIS to the "bottom" of the bar graph
//		Use a timer to call SwapStep() once every tenth second
//		SwapStep():
//			declare a temp integer for use in swaping values later
//			if not done sorting (if "start" is not at the end):
//				check the next bar in the array to find the smallest
//				once all unsorted bars have been checked, use temp as a pivot to swap
//				the values of the smallest with the current "start"
//				then increment "start" and reset the other variables to start at start
//			else if done: stop timer to stop sorting
//			either way, redraw the screen using the (possibly) new data
//			formula for drawng the screen: loop through array drawing a rect with:
//				height = value, width = 20, x = index of loop * 25, y = AXIS - value of element
//			the bar that is currently "start" is colored blue, current smallest is green
//			and the current one being checked s red. All other bars are black.
//			So, set the color as such just before printing whichever bar is being printed
//************************************************************************************
import javax.swing.JFrame;

public class Lab7
{
	public static void main(String[] args)
	{
		JFrame frame = new JFrame("Selection Sort");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		SortPanel sort = new SortPanel();

		frame.getContentPane().add(sort);
		frame.pack();
		frame.setVisible(true);
	}
}