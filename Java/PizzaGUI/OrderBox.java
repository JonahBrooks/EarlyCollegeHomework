//**************************************************************
//********************* OrderBox.java **************************
//**************************************************************
import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;
			// JCheckBox that stores their own listener and item cost
public class OrderBox extends JCheckBox
{	private double cost = 0.0;
	static OrderListener listener = new OrderListener();
	public OrderBox(String text)
	{ 	super(text);
		addActionListener(listener);
	}
		//overloaded constructor for single item purchases
	public OrderBox(String text, double price)
	{	this(text);
		cost = price;
	}
	public double getCost()
	{	return cost;	}

}
