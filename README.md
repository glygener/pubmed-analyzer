# PubMed Analyzer
## EDirect Installation Instructions
* Open a terminal window and run one of the following commands to download and install the software:

    * sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
    * sh -c "$(wget -q https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"

This will prompt a number of script downloads that will be compiled into an "edirect" folder in the user's home directory

You may update the PATH environment variable in the user's configuration file:
* echo "export PATH=\$HOME/edirect:\$PATH" >> $HOME/.bash_profile

Answer "y" and press the Return key if you want to run the PATH update command 

* If the PATH is already set or want to make editing changes manually, press Return
* Once installation is complete, run line below to set the PATH for the current terminal session
    * export PATH=${HOME}/edirect:${PATH}



