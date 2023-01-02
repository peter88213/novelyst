[Project homepage](../index) > [Instructions for use](../usage) > Command reference: Tools menu

--- 

# Tools menu 

**Program settings and miscellaneous functions**

--- 

## Program settings

**Project independent settings**

### Coloring mode

**Set criteria according to which normal scenes are colored in the tree**

- **none** - Normal scenes are black on white by default.
- **status** - Normal scenes are colored according to their completion status (*Outline*, *Draft*, *1st Edit*, *2nd Edit*, or *Done*).
- **style** - Normal scenes are colored according to their style (*staged*, *explaining*, *descriptive*, or *summarizing*). 

### Columns

**Change the column order**

- From top to bottom in the list means from left to right in the tree.
- Just drag and drop to change the order.

Click the **Apply** button to apply changes.

---

## Plugin manager

**Display and manage installed plugins**

- Successfully installed plugins are displayed black on white by default.
- Outdated plugins are grayed out.
- Plugins that cannot run are displayed in red, with an error message.

### About version compatibility

On the window frame, you see the *novelyst* version, consisting of three numbers that are separated by points.

`<major version number>.<minor version number>.<patch level>`

In the **novelyst API**, you see the plugin's compatibility information, consisting of two numbers that are separated by points.

`<major version number>.<minor version number>`

#### The rule for compatibility 

- The plugin's *novelyst API* major version number must be the same as *novelyst's* major version number. 
- The plugin's *novelyst API* minor version number must be less than or equal to *novelyst's* minor version number.

#### Fix incompatibilities

- If the plugin's *novelyst API* major version number is greater than *novelyst's* major version number, *novelyst* needs to be updated.
- If the plugin's *novelyst API* major version number is less than *novelyst's* major version number, the plugin needs to be updated.
- If the plugin's *novelyst API* minor version number is greater than *novelyst's* minor version number, *novelyst* needs to be updated.

#### Update plugins

Select the plugin you want to update. If the "Home page" button is activated, you can click on it, and your system browser opens the plugin home page. Otherwise, you have to know the source of the plugin yourself. 

Go to the plugin home page and download the latest release. Install it according to the instructions. 

If the plugin is a *novelyst* add-on, reinstall it from your latest *novelyst* release files.

### Uninstall a plugin

Select the plugin, and click on the **Delete** button. 

---

[<< Previous](export_menu) -- [First >>](file_menu)