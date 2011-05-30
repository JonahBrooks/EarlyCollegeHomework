//**************************************************************
//******************* OrderButton.java *************************
//**************************************************************
import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;
		// RadioButtons that store their own listener and item's price
public class OrderButton extends JRadioButton
{	private double cost = 0.0;
	static OrderListener listener = new OrderListener();
	public OrderButton(String text, double price)
	{ 	super(text);
		cost = price;
		addItemListener(listener);
	}
	public double getCost()
	{	return cost;	}

}
