//***************************************************************************************
//* Name: Jonah Brooks         	Filename: BrooksJ_L6\PostfixParse.java					*
//*																						*
//* CS260  Spring 2011          Lab #: 6												*
//* Date:  Sunday May 22nd, 2011														*
//*																						*
//*	Program Name: PostfixParser.java													*
//* Program Description:																*
//*		Accepts an infix notation equation from the user and formats it into postfix	*
//*		notation and evaluates that new postfix equation.								*
//*																						*
//*	Pseudocode:																			*
//*		Prompt the user for an equation in infix notation.								*
//*		Use a for-loop and a switch statement to parse the infix equation				*
//*			If the next character is a number, add it to the new string					*
//*			If the next character is an operator, peek at the top of the operator stack	*
//*			If the top of the stack is of lower precedence, push the new operator		*
//*			Otherwise pop the operators to the string until the above check passes		*
//*			Repeat until the entire input expression has been parsed to the new string	*
//*		Now use a loop to parse the new postfix expression								*
//*			Scan the expression adding each new integer to a stack						*
//*			When an operator is found, perform the operation on the last two operands	*
//*			Push the result of that operation onto the stack as a new operand			*
//*			Repeat until all operators and operands have been processed					*
//*		Pop the last operand (result) off of the stack and print it out to the screen	*
//*																						*
//***************************************************************************************
import java.util.Scanner;
import java.util.Stack;

public class PostfixParser
{
	public static void main(String[] args)
	{
		Scanner scan = new Scanner(System.in);
		boolean anotherExpression = true;

		System.out.println("Input an infix expression of integers (or enter to quit): ");
		String infix =  scan.nextLine();
		if(infix.trim().length() == 0)
			anotherExpression = false;
		while(anotherExpression)
		{
			String postfix = "";

			Stack<Character> operatorStack = new Stack<Character>();

				// Parse into postfix
			char lastChar = '~';
			for(int i = 0; i < infix.length(); i++)
			{
				char curChar = infix.charAt(i);

				switch(curChar)
				{
					case '0': case '1': case '2': case '3': case '4':
					case '5': case '6': case '7': case '8': case '9':
						if(!(lastChar >= '0' && lastChar <= '9'))
							postfix += ' ';
						postfix += curChar;
						lastChar = curChar;
						break;

					case '(': case '[': case '{':
					case '*': case '/': case '%':
					case '+': case '-':
						lastChar = curChar;
						while((!operatorStack.isEmpty()) &&
							(getPrecedence(curChar) <= getPrecedence(operatorStack.peek()))
							&& getPrecedence(operatorStack.peek()) != 4 )
						{
							postfix += " "+ operatorStack.pop();
						}
						operatorStack.push((Character)curChar);
						break;
					case ')': case ']': case '}':
						while(!operatorStack.isEmpty()
							 &&(curChar == ')' && operatorStack.peek() != '(')
							 ||(curChar == ']' && operatorStack.peek() != '[')
							 ||(curChar == '}' && operatorStack.peek() != '{') )
						{ postfix += " "+ operatorStack.pop(); }
						if(!operatorStack.isEmpty())
							operatorStack.pop();	// get rid of the opening brace
						break;
					default:
						break;
				}
			}
			while(!operatorStack.isEmpty())
			{ postfix += " " + operatorStack.pop();
			}

			System.out.println("Infix: " + infix);
			System.out.println("Postfix:" + postfix);

			Stack<Integer> operandStack = new Stack<Integer>();
			Scanner parser = new Scanner(postfix);
			String operator;
			while(parser.hasNext())
			{	if(parser.hasNextInt())
					operandStack.push((Integer)parser.nextInt());
				else
				{	operator = parser.next();
					int second = operandStack.pop();
					int first = operandStack.pop();
					switch(operator.charAt(0))
					{
						case '+':
							operandStack.push((Integer)(first + second));
							break;
						case '-':
							operandStack.push((Integer)(first - second));
							break;
						case '*':
							operandStack.push((Integer)(first * second));
							break;
						case '/':
							operandStack.push((Integer)(first / second));
							break;
						case '%':
							operandStack.push((Integer)(first % second));
							break;
						default:
							break;
					}
				}
			}
			int total = operandStack.pop();
			System.out.println("Evaluates to: " + total + "\n");

			System.out.println("Input an infix expression of integers (or enter to quit): ");
			infix =  scan.nextLine();
			if(infix.trim().length() == 0)
				anotherExpression = false;
		}
	}

	private static int getPrecedence(char arg)
	{	int toReturn = -1;
		switch(arg)
		{	case '(': case '[': case '{':
				toReturn = 4;
				break;
			case '*': case '/': case '%':
				toReturn = 3;
				break;
			case '+': case '-':
				toReturn = 2;
				break;
			default:
				break;
		}
		return toReturn;
	}
}