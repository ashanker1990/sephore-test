Code explanation:

The code is in sephora_script.py

1. The first part calculates the dependencies of all the sql scripts in the /tmp folder and draws up a graph based on that.I have added in the function to visualize a graph assuming a simple two layer of children and sub children.

The key part in calculating dependencies is to see if the sql script depends on files in the /raw folder or other sql scripts in the /tmp folder.I have written a text scraping function to run this.

2. The second part is to determine the order of script execution.For this I do a two part execution.I iterate through all the scripts which have dependencies on other scripts in the /tmp folder.For each child script I recurse till I reach the base script which ONLY HAS A DEPENDENCY ON A RAW FILES.

In this manner I determine the correct order of scripts in the /tmp folder


3.The this part is to parallelize some scripts.Since all the scripts which have DEPENDENCY ONLY ON RAW FILES can be though of the “base scripts” these can be run parallel initially.
After this the scripts which have dependency on other /tmp scripts are executed.

NOTE: The order of script execution between 2 and 3 changes -this shows how the parallelism affects the order of execution

RUNNING INSTRUCTIONS:
— Pull the repo
— Run the sephora_script.py python code
