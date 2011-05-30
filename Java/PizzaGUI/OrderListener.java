//**************************************************************
//********************* OrderListener.java *********************
//**************************************************************
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
public class OrderListener implements ItemListener, ActionListener
{
	DataHolder data = new DataHolder();	// used to interact with data and other panels
	public void itemStateChanged(ItemEvent event)
	{
		OrderButton button = (OrderButton) event.getItem();

			// ******** Begin pizzaPanel event handeling **********
		if (button.getParent().getParent().getName().equals("Pizza"))
		{		// must use getParent twice to get to the main panel instead of the sub panel

			if(button.isSelected())	// if this event is selecting an item
			{	data.modCost(button.getCost());
				data.modType(button.getText());
			}
			else	// if this even is deselecting an item
			{	data.modCost(-button.getCost());	// send a negative to reduce total cost
			}

		} // end pizzaPanel event handeling

			// ******** Begin drinkPanel event handeling ***********
		else if (button.getParent().getParent().getName().equals("Drinks"))
		{	if(button.isSelected())
				data.modCost(button.getCost());
			else
				data.modCost(-button.getCost());

				// changes the type, container, and size of the drink
			data.modDrink(button.getParent().getName(), button.getText());

		} // end drinkPanel even handeling

			// update the screen with the new information
		JFrame parent = (JFrame)button.getTopLevelAncestor();
		PizzaPanel panel = (PizzaPanel)parent.getContentPane().getComponent(0);
		panel.update();
	} // end itemStateChanged()

	public void actionPerformed(ActionEvent event)
	{	OrderBox box = (OrderBox) event.getSource();

			// ******** Begin pizzaPanel event handeling **********
		if (box.getParent().getParent().getName().equals("Pizza"))
		{		// must use getParent twice to get to the main panel instead of the sub panel
			data.modTopping(box.getText());
		}
			// ******** Begin extraPanel event handeling **********
		else if (box.getParent().getParent().getName().equals("Extras"))
		{
			if(box.isSelected())
				data.modExtras(box.getText(), box.getCost());
			else		// add or subtract an extra and its corrisponding cost from the order
				data.modExtras(box.getText(), box.getCost());
		}
				// update the screen with the new information
		JFrame parent = (JFrame)box.getTopLevelAncestor();
		PizzaPanel panel = (PizzaPanel)parent.getContentPane().getComponent(0);
		panel.update();
	} // end actionPerformed()
} // end OrderListener class
