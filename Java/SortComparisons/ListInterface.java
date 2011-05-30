// *********************************************
//   Interface ListInterface<T>
//  ** An interface for the ADT list.
//   Entries in the list  have positions that begin with 1
// *********************************************

public interface ListInterface<T>
{
	//*****************************************************
   	// Task:  Adds a new entry to the end of the list
   	//        Entries currently in the list are unaffected.
   	//        The list's size is increased by 1.
   	//  @param newEntry: the object to be added as a new entry
   	//  @return true: if the addition is successful, or false if the list is full
   	//****************************************************************
   	public boolean add(T newEntry);

    //***************************************************************
    // Task: Adds a new entry at a specified position within the list.
    //       Entries originally at and above the specified position are at
    //             the next higher position within the list.
    // @param newPosition: an integer that specifies the desired position of new entry
    // @param newEntry: the object to be added as a new entry
    // @ return true:  if the addition is successful
    //          false: if either the list is full, newPosition <1, or
    //                  newPosition > getLength() +1
    //*****************************************************************
    public boolean add(int newPosition, T newEntry);

    // ******************************************************
    // Task: Removes the entry at a given position from the list.
    //       Entries originally at positions higher than the given position are at
    //         the next lower position within the list, and the list size is decreased by 1
    //  @param givenPosition:  an integer tha tindicates the position of the entry to
    //                         be removed.
    //  @return: a reference to the removed entry, or null - if either the list was empty
    //             or givenPosition <1, or givenPosition > getLength()
    //********************************************************
    public T remove(int givenPosition);

    // ******************************************************
	// Task: Removes the first instance of the argument object in the list.
	//		 Collapse the list back down and decrement the length of the list.
	//  @param anObject:  a T object to remove from the list
	//  @return: true if the object was found and removed succesfully
	//			 false if the object was not found in the list
    //********************************************************
    public boolean remove(T anObject);

	// ******************************************************
    // Task: remove all entries from the list.
    // ******************************************************
  	public void clear();

   	//***************************************************
    // Task:  Replaces the entry at a given position in the list.
    // @param givenPosition: an integer that indicates the position of the entry
    //                       to be replaced.
    // @param newEntry: the object that will replace the entry at the position specified
    // @return true: if the replacement occurs
    //         false: if the list is empty, givenPosition <1 or givenPosition > getLength()
    //****************************************************
    public boolean replace(int givenPosition, T newEntry);


    //***************************************************
    // Task:  Replaces the entry at a given position in the list.
    // @param replacePos: an integer that indicates the position of the entry
    //                       to be replaced.
    // @param replaceWith: the object that will replace the entry at the position specified
    // @return the object that was replaced, or null if replacePos is not valid
    //****************************************************
    public T replaceNreturn(int replacePos, T replaceWith);

    // **************************************************
    // Task:  Retrieves the entry at a given position in the list
    // @param givenPosition:  an integer that indicates the position of the desired entry
    // @return: a reference to the indicated entry
    //          or null if the list is empty, givenPosition <1 or givenPosition > getLength()
    // ***************************************************
    public T getEntry(int givenPosition);

    // **************************************************
	// Task:  Finds and returns the position of an object in the list
	// @param anObject:  a T object for which to search the area
	// @return: an integer representing the position of the object in the list
	//          or -1 if the object is not contained in the list
    // ***************************************************
    public int getPosition(T anObject);


    //****************************************************
    //  Task:  Sees whether the list contains a given entry.
    //  @param anEntry:  the object that is the desired entry
    //  @return: true if the list contains anEntry
    //           false if the list does not contain anEntry.
    //******************************************************
    public boolean contains(T anEntry);


    //********************************************************
    //   Task:  Gets the length of the list.
    //   @return: the integer number of entries currently in the list
    //*********************************************************
    public int getLength();

    //********************************************************
    // Task: sees whether the list is empty
    // @return: true if the list is empty
    //           false if the list is not empty
    //****************************************************
    public boolean isEmpty();

    //********************************************************
    // Task: sees whether the list is full
    // @return: true if the list is full
    //           false if the list is not full
    //****************************************************
    public boolean isFull();


    //********************************************************
    // Task: Displays all entries in the list, on per line
    //       in the order in which they occur in the list
    //****************************************************
    public void display();

    //****************************************************
	//  Task:  Checks for equality between two lists
	//  @param argList:  the list with which to compare this one
	//  @return: true if all elements of both lists are the same
	//           false any of the elements of the lists differ
    //******************************************************
    public boolean equals(LList<T> argList);


}  // end ListInterface