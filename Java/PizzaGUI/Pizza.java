//************************************************************************************
//  Name: Jonah Brooks         	Filename: BrooksJ_L5\Pizza.java
//  CS162  Spring 2010          Lab #: 5
//  Tues, Thurs 1:00 PM
//  Date:  Monday May 10th, 2010
//
// 	Program Name: Pizza.java  along with: OrderListener.java, OrderButton.java,
//				OrderBox.java, DrinkOrderPanel.java, ExtrasOrderPanel.java,
//				PizzaOrderPanel.java, TotalPanel.java, DataHolder.java
//	Program Description:
//		A GUI for calculating the cost of a pizza order
//************************************************************************************

import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;

public class Pizza
{	public static void main (String[] args)
	{	PizzaFrame frame = new PizzaFrame("Pizza!");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setPreferredSize(new Dimension(1000,700));
		frame.pack();
		frame.setVisible(true);
	}
}
class PizzaFrame extends JFrame
{	private PizzaPanel pPanel = new PizzaPanel();
	public PizzaFrame(String arg)
	{	super(arg);
		getContentPane().add(pPanel);
	}
	public void update()
	{	pPanel.update();
	}
}

// panel that holds all the other panels
class PizzaPanel extends JPanel
{	TotalPanel tPanel = new TotalPanel();
	public PizzaPanel()
	{	setLayout(new BorderLayout());
			// ****leave a gray border around each item
		setBackground (Color.gray);
		add(new TitlePanel(), BorderLayout.NORTH);
		add(tPanel, BorderLayout.WEST);
		add(new OrderPane(), BorderLayout.CENTER);
		add(new JLabel("Pizza!"), BorderLayout.SOUTH);
		setVisible(true);
	}
	public void update()
	{	tPanel.update();
	}
}

// top panel, contains the logo and title
class TitlePanel extends JPanel
{
	public TitlePanel()
	{	JLabel titleLabel = new JLabel("PIZZA!      ", new ImageIcon("banner.jpg"), SwingConstants.CENTER);
		titleLabel.setHorizontalTextPosition(SwingConstants.LEFT);
		titleLabel.setFont(new Font("Dialog", 1, 30));
		add(titleLabel);
		setBackground(new Color(50,120,50));
	}
}

// tabbed pane in the center, holds the order panels
class OrderPane extends JTabbedPane
{
	public OrderPane()
	{
		addTab("Pizza", new PizzaOrderPanel());
		addTab("Drinks", new DrinkOrderPanel());
		addTab("Extras", new ExtrasOrderPanel());

	}
}
