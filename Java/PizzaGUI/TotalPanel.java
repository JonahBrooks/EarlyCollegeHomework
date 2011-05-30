//**************************************************************
//********************** TotalPanel.java ***********************
//**************************************************************
import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;
	// left panel, holds the total order details, including total cost
class TotalPanel extends JPanel
{	JPanel pizzaTotal = new JPanel();
	JLabel pizzaType = new JLabel();

	JPanel drinkTotal = new JPanel();
	JLabel drinkType = new JLabel();
	JLabel drinkCont = new JLabel();
	JLabel drinkSize = new JLabel();

	JPanel extraTotal = new JPanel();

	JPanel orderTotal = new JPanel();
	JLabel orderCost = new JLabel("$0");

	DataHolder data = new DataHolder();	// used to interact with data and other panels

	public TotalPanel()
	{
		setLayout(new BoxLayout (this, BoxLayout.Y_AXIS));
		Border inner = BorderFactory.createRaisedBevelBorder();
		Border outter = BorderFactory.createMatteBorder(22,5,0,3, Color.gray);
		Border combo = BorderFactory.createCompoundBorder(outter, inner);
		setBorder(combo);
		pizzaTotal.setLayout(new BoxLayout(pizzaTotal,BoxLayout.Y_AXIS));
		extraTotal.setLayout(new BoxLayout(extraTotal,BoxLayout.Y_AXIS));
		drinkTotal.setLayout(new BoxLayout(drinkTotal,BoxLayout.Y_AXIS));
		orderTotal.setLayout(new BoxLayout(orderTotal,BoxLayout.Y_AXIS));
		pizzaTotal.add(new JLabel("-Pizza:                             "));
		pizzaTotal.add(pizzaType);			// extra spaces on Pizza to set size of panel
		add(pizzaTotal);
		add(Box.createVerticalGlue());
		drinkTotal.add(new JLabel("-Drink:"));
		drinkTotal.add(drinkSize);
		drinkTotal.add(drinkCont);
		drinkTotal.add(drinkType);
		add(drinkTotal);
		add(Box.createVerticalGlue());
		extraTotal.add(new JLabel("-Extras:"));
		add(extraTotal);
		add(Box.createVerticalGlue());
		orderTotal.add(new JLabel("Total cost:"));
		orderTotal.add(orderCost);
		add(orderTotal);
	} // end constructor
	//************************************************************************
	//* update: Refreshes the panels to show current order status		     *
	//************************************************************************
	public void update()
	{  		// update total cost
		orderCost.setText(data.getCost());
			// update size/crust of pizza
		pizzaType.setText(data.getPType());
			// update toppings
		for(int i = 0; i < data.getAllToppings().length; i++)
		{	if( data.getToppingFlags()[i] )	// if this topping is on the pizza
				pizzaTotal.add(data.getAllToppings()[i]);
			else
				pizzaTotal.remove(data.getAllToppings()[i]);
		}
			// update drink
		drinkSize.setText(data.getDSize());
		drinkCont.setText(data.getDCont());
		drinkType.setText(data.getDType());
			// update extras
			// update toppings
		for(int i = 0; i < data.getAllExtras().length; i++)
		{	if( data.getExtraFlags()[i] )	// if this extra has been selected
				extraTotal.add(data.getAllExtras()[i]);
			else
				extraTotal.remove(data.getAllExtras()[i]);
		}
	} // end update()
} // end TotalPanel class
