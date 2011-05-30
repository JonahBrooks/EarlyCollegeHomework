import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
public class SortPanel extends JPanel implements ActionListener
{
	private int[] bars = new int[30];
	private int indexStart = 0, indexSmall = 0, indexCheck = 1;
	private Graphics screen;
	private final int AXIS = 175;	// the X axis of the bar graph
	private Timer slowSort;
	private JButton startButton, stopButton, resetButton, brightButton;
	private int barHue = 100;

	public SortPanel()
	{
		slowSort = new Timer(100,this);
		setPreferredSize(new Dimension(800,200));
		Reseed();
		startButton = new JButton("Start");
		stopButton = new JButton("Stop");
		resetButton = new JButton("Reset");
		brightButton = new JButton("Brighten Colors");
		startButton.addActionListener(this);
		stopButton.addActionListener(this);
		resetButton.addActionListener(this);
		brightButton.addActionListener(this);
		add(startButton);
		add(stopButton);
		add(resetButton);
		add(brightButton);
		repaint();
	}

	public void paintComponent(Graphics page)
	{	screen = page;
		Display();
	}

	//************ Reseed: resets the array with new random numbers ***************
	public void Reseed()
	{	for(int i = 0; i < bars.length; i++)
			bars[i] = (int)(Math.random()*91) + 10; // random between 10 and 100 inclusive
	}
	//****************** Display: draws the bars to the screen ********************
	public void Display()
	{
		for(int i = 0; i < bars.length; i++)
		{ 	int x = (i+1)*25 ;
			int y = AXIS - bars[i];
			if(i == indexStart)	// color the current starting bar blue
				screen.setColor(new Color(10,10,barHue));
			else if(i == indexSmall)	// and the current smallest gree
				screen.setColor(new Color(10,barHue,10));
			else if(i == indexCheck)	// and the current possibly smallest red
				screen.setColor(new Color(barHue,10,10));
			screen.clearRect(x,0,20,200);	// clear this bar from the screen
			screen.fillRect(x,y,20,bars[i]); // then redraw the new one
			screen.setColor(Color.black);	// reset to draw all other bars black
			screen.drawString(Integer.toString(bars[i]),x,AXIS+10);	// print value below bar
		}
	}
	//********** SwapStep: takes one step through the sorting proccess. ***********
	public void SwapStep()
	{	int temp;
		if(indexStart < bars.length-1)
		{	if(indexCheck < bars.length)
			{	if(bars[indexSmall] > bars[indexCheck])
					indexSmall = indexCheck;
				indexCheck++;
			}
			else
			{	temp = bars[indexSmall];
				bars[indexSmall] = bars[indexStart];
				bars[indexStart] = temp;
				indexStart++;	// start from next bar next time
				indexSmall = indexStart;	// assume that it is the smallest
				indexCheck = indexSmall + 1;	// check said assumption starting with next next bar
			}
		}
		else
			slowSort.stop();	// stop sorting when indexStart gets to the end
		repaint();
	}
	//********** actionPerformed: the listener for the timer and buttons **********
	public void actionPerformed(ActionEvent e)
	{	Object src = e.getSource();
		if(src.equals(slowSort))
			SwapStep();
		else if(src.equals(startButton))
			slowSort.start();
		else if(src.equals(stopButton))
			slowSort.stop();
		else if(src.equals(resetButton))
		{	slowSort.stop();
			indexSmall = indexStart = indexCheck = 0;
			Reseed();
			repaint();
		}
		else
		{	if(barHue == 100)
			{	barHue = 200;
				brightButton.setText("Darken Colors");
			}
			else
			{	barHue = 100;
				brightButton.setText("Brighten Colors");
			}
			repaint();
		}
	}
} // end class SortPanel