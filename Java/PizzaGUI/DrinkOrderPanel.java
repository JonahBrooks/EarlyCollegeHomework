//**************************************************************
//***************** DrinkOrderPanel.java ***********************
//**************************************************************
import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;

public class DrinkOrderPanel extends JPanel
{	OrderButton sizeLarge = new OrderButton("Large",4.25);
	OrderButton sizeMedium = new OrderButton("Medium",3.75);
	OrderButton sizeSmall = new OrderButton("Small",1.50);

	OrderButton contGlass = new OrderButton("Glass",0.0);
	OrderButton contBottle = new OrderButton("Bottle",0.5);
	OrderButton contPitcher = new OrderButton("Pitcher",1.0);

	OrderButton DrPepper = new OrderButton("Dr. Pepper", 0.0);
	OrderButton coke = new OrderButton("Coke", 0.0);
	OrderButton rootbeer = new OrderButton("Rootbeer", 0.0);
	OrderButton sevUp = new OrderButton("7-Up",0.0);
	OrderButton juice = new OrderButton("Juice",0.0);

	public DrinkOrderPanel()
	{	setName("Drinks");	// used to ID this panel in the listener
		setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
		add(Box.createVerticalGlue());

				// add the GUI elements for the size selection
 		add(new JLabel("Size:"));
		JPanel Size = new JPanel();
		Size.setName("Size");	// used to ID this sub-panel in the listener
			Size.setLayout(new BoxLayout(Size, BoxLayout.X_AXIS));
			Size.add(sizeLarge);
			Size.add(sizeMedium);
			Size.add(sizeSmall);
		ButtonGroup sizeGroup = new ButtonGroup();
		sizeGroup.add(sizeLarge);
		sizeGroup.add(sizeMedium);
		sizeGroup.add(sizeSmall);
		add(Size);
		add(Box.createVerticalGlue());

				// add the GUI elements for selecting the container for the drink
		add(new JLabel("Container:"));
		JPanel Cont = new JPanel();
		Cont.setName("Cont");	// used to ID this sub-panel in the listener
			Cont.setLayout(new BoxLayout(Cont, BoxLayout.X_AXIS));
			Cont.add(contGlass);
			Cont.add(contBottle);
			Cont.add(contPitcher);
		ButtonGroup contGroup = new ButtonGroup();
		contGroup.add(contGlass);
		contGroup.add(contBottle);
		contGroup.add(contPitcher);
		add(Cont);
		add(Box.createVerticalGlue());

				// add the GUI elements for the drink selection
		add(new JLabel("Type of drink:"));
		JPanel Type = new JPanel();
		Type.setName("Type");	// used to ID this sub-panel in the listener
			Type.add(DrPepper);
			Type.add(coke);
			Type.add(rootbeer);
			Type.add(sevUp);
			Type.add(juice);
		ButtonGroup typeGroup = new ButtonGroup();
		typeGroup.add(DrPepper);
		typeGroup.add(coke);
		typeGroup.add(rootbeer);
		typeGroup.add(sevUp);
		typeGroup.add(juice);
		add(Type);
		add(Box.createVerticalGlue());
	} // end constructor
} // end DrinkOrderPanel class
