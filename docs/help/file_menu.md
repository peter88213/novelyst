[Project homepage](../index) > [Instructions for use](../usage) > [Online help](help) > Command reference: File menu

--- 

# File menu 

**File operation**

--- 

## New 

**Create a new novel project**

- You can create a new project with **File > New** or **Ctrl-N**. This will close the current project
  and open a file dialog asking for the location and file name of the project to create.
- Once you specified a valid file path, a blank project appears. Be aware, it's not saved on disk yet.

--- 

## Open... 

**Open a novel project**

- If no novel project is specified by dragging and dropping on the program icon,
  the latest project selected is preset. You can change it with **File > Open** or **Ctrl-O**.

--- 

## Reload

**Reload the novel project**

- You can reload the project with **File > Reload** or **Ctrl-R**.
- If the project has changed on disk since last opened, you will get a warning.

--- 

## Refresh tree

**Update the project structure after making changes**

Hit the **F5** key to synchronize the tree with the project structure. This ensures for instance, 
that scenes within a "Notes", "Unused", or "To do" chapter are of the same type after moving them there.
- Refreshing the tree may trigger the "Modified" flag.
- When refreshing the tree, "Normal type" chapters in the *Research* tree are moved to the *Narrative* tree.
- When refreshing the tree, parts and chapters are renumbered according to the settings. 

--- 

## Lock 

**Protect the project while edited outsides**

You can lock the project, so that no changes can be made with *novelyst* while parts of the project are
edited "outsides", e.g. with OpenOffice. In locked status, the window footer displaying the project path
is displayed in reversed colors. 
 
- You can lock the project with **File > Lock** or **Ctrl-L**. The project is saved when modified.

The project lock status is persistent. This is achieved by automatically creating a lock file 
named `.LOCK.<project name>.yw7#`. If you delete this file while *novelyst* is not running, the project 
will be unlocked upon next start.  

This locking mechanism must not be confused with that of yWriter. When the project is opened in yWriter, 
yWriter creates its own lock file. If *novelyst* finds this, it will neither load nor save the project. 

--- 

## Unlock

**Make the project editable**

- You can unlock the project with **File > Unlock** or **Ctrl-U**. 

--- 

## Open Project folder

**Launch the file manager**

- You can launch the file manager with the current project folder with **File > Open Project folder** or **Ctrl-P**. This might be helpful, if you wish to delete export files, open your project with another application, and so on. In case you edit the project "outsides", consider locking it before.

--- 

## Save

**Save the project**

- You can save the project with **File > Save** or **Ctrl-S**.
- If the project is open in yWriter, you will be asked to exit yWriter first.
- If the project has changed on disk since last opened, you will get a warning.
- It is recommended to refresh the tree (see above) before saving. So you can see how 
  it will look after reloading. 

--- 

## Save as...

**Save the project with another file name/at another place**

- You can save the project with another file name/at another place with **File > Save as...** or **Ctrl-Shift-S**. Then a file select dialog opens.
- Your current project remains as saved the last time. Changes since then go to the new project.

--- 

## Close

**Close the novel project**

- You can close the project without exiting the program with **File > Close**.
- When closing the project, you will be asked for saving the project, if it has changed.
- If you open another project, the current project is automatically closed.

--- 

## Exit

**Exit the program**

- You can exit with **File > Exit** of **Ctrl-Q**.
- When exiting the program, you will be asked for saving the project, if it has changed.

--- 

[<< Last](tree_context_menu) -- [Next >>](view_menu)