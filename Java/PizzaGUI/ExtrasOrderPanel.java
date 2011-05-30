//**************************************************************
//***************** ExtrasOrderPanel.java **********************
//**************************************************************
import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;

public class ExtrasOrderPanel extends JPanel
{	OrderBox stickBread = new OrderBox("Bread Sticks",3.25);
	OrderBox stickCheese = new OrderBox("Cheese Sticks",4.75);
	OrderBox stickStuffed = new OrderBox("Stuffed Cheese Sticks",6.50);

	OrderBox desCin = new OrderBox("Cinnamon Sticks",4.15);
	OrderBox desPizza = new OrderBox("Dessert Pizza",9.85);

	OrderBox sideSalad = new OrderBox("Side Salad", 4.75);
	OrderBox sideMari = new OrderBox("Marinara Sauce", 0.5);
	OrderBox sideGarlic = new OrderBox("Garlic Dip", 0.5);
	OrderBox sideRanch = new OrderBox("Ranch Dressing",0.5);

	public ExtrasOrderPanel()
	{	setName("Extras");	// used to ID this panel in the listener
		setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
		add(Box.createVerticalGlue());

				// add the GUI elements for the stick selection
 		add(new JLabel("Sticks:"));
		JPanel Sticks = new JPanel();
		Sticks.setName("Sticks");	// used to ID this sub-panel in the listener
			Sticks.setLayout(new BoxLayout(Sticks, BoxLayout.X_AXIS));
			Sticks.add(stickBread);
			Sticks.add(stickCheese);
			Sticks.add(stickStuffed);
		add(Sticks);
		add(Box.createVerticalGlue());

				// add the GUI elements for the dessert selection
		add(new JLabel("Desserts:"));
		JPanel Des = new JPanel();
		Des.setName("Desserts");	// used to ID this sub-panel in the listener
			Des.setLayout(new BoxLayout(Des, BoxLayout.X_AXIS));
			Des.add(desCin);
			Des.add(desPizza);
		add(Des);
		add(Box.createVerticalGlue());

				// add the GUI elements for the selection of side orders
		add(new JLabel("Sides:"));
		JPanel Sides = new JPanel();
		Sides.setName("Sides");	// used to ID this sub-panel in the listener
			Sides.add(sideSalad);
			Sides.add(sideMari);
			Sides.add(sideGarlic);
			Sides.add(sideRanch);
		add(Sides);
		add(Box.createVerticalGlue());
	} // end constructor
} // end ExtrasOrderPanel class
