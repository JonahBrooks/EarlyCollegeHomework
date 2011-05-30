//**************************************************************
//********************** DataHolder.java ***********************
//**************************************************************
import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;
import java.text.NumberFormat;

//***********************************************************
//*	DataHolder Class: Designed to make the program work...  *
//***********************************************************
public class DataHolder
{
	static private double totalCost;
	static private int numToppings;
	static private String pCrust, pSize, dType, dSize, dCont, eSize;
	static private JLabel[] toppings = {	new JLabel("Green Peppers"),
								new JLabel("Black Olives"),
								new JLabel("Pepperoni"),
								new JLabel("Ham"),
								new JLabel("Pineapple"),
								new JLabel("Red Onions")	};
	static private boolean[] toppingFlags= {false, false, false, false, false, false };
				// ** these arrays are for storing and managing the check box data **
	static private JLabel[] extras = {	new JLabel("Bread Sticks"),
								new JLabel("Cheese Sticks"),
								new JLabel("Stuffed Cheese Sticks"),
								new JLabel("Cinnamon Sticks"),
								new JLabel("Dessert Pizza"),
								new JLabel("Side Salad"),
								new JLabel("Marinara Sauce"),
								new JLabel("Garlic Dip"),
								new JLabel("Ranch Dressing") };
	static private boolean[] extraFlags = {false,false,false,false,false,false,false,false,false};

	//****************************************************
	//* methods used during all event handeling          *
	//****************************************************
	public DataHolder()
	{ 	totalCost = 0.0;

		numToppings = 0;

		pCrust = "";
		pSize = "";
		dType = "";
		dSize = "";
	}
		// modCost: changes the cost by the amount sent in
	public void modCost(double arg)
	{	totalCost += arg;	}

		// getCost: returns a string with the total cost of the order
	public String getCost()
	{	return NumberFormat.getCurrencyInstance().format(totalCost);	}

	//****************************************************
	//* methods used for handeling the PizzaPanel events *
	//****************************************************

		// modType: takes the size or crust type as an argument and updates it here
	public void modType(String arg)
	{		// if the input is a crust type, based on second letter of name
		if( arg.charAt(1) == 't' || arg.charAt(1) == 'h')
			pCrust = arg + " crust";
		else
			pSize = arg;
	}

		// modTopping: adds or takes off a topping on the pizza
	public void modTopping(String arg)
	{	for(int i = 0; i < toppings.length; i++)
		{	if (toppings[i].getText().equals(arg))	// if this index is a match to the arg
				if (toppingFlags[i])	// if this topping is already on the pizza
				{ 	totalCost -= 1;	// take away a dollar for removing an 'extra' topping
					toppingFlags[i] = false;
				}
				else
				{	totalCost += 1;	// add a dollar for adding an 'extra' topping
					toppingFlags[i] = true;
				}
		} // end for
	} // end modTopping

		// getPType: returns a string in the format of "[size] [crust]"
	public String getPType()
	{	return pSize + " " + pCrust;	}

		// getAllTopping: returns the array of toppings
	public JLabel[] getAllToppings()
	{	return toppings;	}
		// getToppingFlags: returns the array of topping flags
	public boolean[] getToppingFlags()
	{	return toppingFlags;	}

	//*****************************************************
	//* methods used for handeling DrinkPanel events      *
	//*****************************************************

		// accepts the name of the container of the button,
		//	and the name of the button. Sets drink stats.
	public void modDrink(String origin, String arg)
	{	if(origin.equals("Size"))
			dSize = arg;
		else if (origin.equals("Cont"))
			dCont = arg;
		else
			dType = arg;
	}

	public String getDSize()
	{	return dSize;	}

	public String getDCont()
	{	return dCont;	}

	public String getDType()
	{	return dType;	}

	//****************************************************
	//* methods used for handeling the ExtrasPanel events*
	//****************************************************

		// modExtras: adds or takes off an extra from the order
	public void modExtras(String arg, double price)
	{	for(int i = 0; i < extras.length; i++)
		{	if (extras[i].getText().equals(arg))	// if this index is a match to the arg
				if (extraFlags[i])	// if this topping is already on the pizza
				{ 	totalCost -= price;	// subtract the cost of this extra from the order cost
					extraFlags[i] = false;
				}
				else
				{	totalCost += price;	// add the cost of this extra to the order cost
					extraFlags[i] = true;
				}
		} // end for
	} // end modExtras

		// getAllExtras: returns the array of extras
	public JLabel[] getAllExtras()
	{	return extras;	}
		// getExtraFlags: returns the array of extras flags
	public boolean[] getExtraFlags()
	{	return extraFlags;	}
} // end DataHolder class