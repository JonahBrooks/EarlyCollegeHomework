//**************************************************************
//***************** PizzaOrderPanel.java ***********************
//**************************************************************
import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;

public class PizzaOrderPanel extends JPanel
{	OrderButton sizeLarge = new OrderButton("Large",12.95);
	OrderButton sizeMedium = new OrderButton("Medium",10.95);
	OrderButton sizeSmall = new OrderButton("Small",8.95);

	OrderButton crustThick = new OrderButton("Thick",0.0);
	OrderButton crustThin = new OrderButton("Thin",0.0);
	OrderButton crustStuffed = new OrderButton("Stuffed",1.0);

	OrderBox peppers = new OrderBox("Green Peppers");
	OrderBox olives = new OrderBox("Black Olives");
	OrderBox pepperoni = new OrderBox("Pepperoni");
	OrderBox ham = new OrderBox("Ham");
	OrderBox pineapple = new OrderBox("Pineapple");
	OrderBox onion = new OrderBox("Red Onions");

	public PizzaOrderPanel()
	{	setName("Pizza");	// used to ID this panel in the listener
		setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
		add(Box.createVerticalGlue());

				// add the GUI elements for the size selection
 		add(new JLabel("Size:"));
		JPanel Size = new JPanel();
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

				// add the GUI elements for the crust selection
		add(new JLabel("Crust:"));
		JPanel Crust = new JPanel();
			Crust.setLayout(new BoxLayout(Crust, BoxLayout.X_AXIS));
			Crust.add(crustThick);
			Crust.add(crustThin);
			Crust.add(crustStuffed);
		ButtonGroup crustGroup = new ButtonGroup();
		crustGroup.add(crustThick);
		crustGroup.add(crustThin);
		crustGroup.add(crustStuffed);
		add(Crust);
		add(Box.createVerticalGlue());

				// add the GUI elements for the topping selection
		add(new JLabel("Toppings:"));
		JPanel Toppings = new JPanel();
			Toppings.add(peppers);
			Toppings.add(olives);
			Toppings.add(pepperoni);
			Toppings.add(ham);
			Toppings.add(pineapple);
			Toppings.add(onion);
		add(Toppings);
		add(Box.createVerticalGlue());
	} // end constructor
} // end PizzaOrderPanel class
