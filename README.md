

<img src="https://github.com/jackpay/cascadePy/blob/master/markdown/images/CASM_LOGO_COLOUR.png" width=300/>

# cascadePy
cascadePy (CaPy) is a corpus expansion toolkit written in Python.

cascadePy is a Python toolkit developed by [Centre for the Analysis of Social Media (CASM) Technology LLP](https://www.casmtechnology.com/) in collaboration with the [Global Initiative against Transnational Organised Crime (GITOC)](https://globalinitiative.net/).

cascadePy is combines a number of NLP, information-extraction and web-collection methods to provide a set of tools primarily for use in open-source intelligence (OSINT) efforts against the illicit online wildlife trade.

The intended use of cascadePy is to discover, chracterise and expand the vernacular used by those in the trade of illegal wildlife and identify the places they are use on the web.

This work is an expansion on the original work that can be found [here](http://sro.sussex.ac.uk/id/eprint/93062/).

The installation instructions for the toolkit can be found below and a brief summary of each module can be found in the accompanying Wiki. 

# Citing this work
If you intend to use this toolit, please use the following citation:

> Pay, Jack Frederick, 2020. The Corpus Expansion Toolkit: finding what we want on the web (Doctoral thesis, University of Sussex).

In bibtex:
```
@phdthesis{pay2020corpusexpansion,
           title = {The Corpus Expansion Toolkit: finding what we want on the web},
          author = {Jack Frederick Pay},
            year = {2020},
          school = {University of Sussex},
             url = {http://sro.sussex.ac.uk/id/eprint/93062/},
}
```


# Installation instructions

## Prerequisites
1) It is recommended that your Python environment is >=3.8
2) Is is also recommended to use a data-science focused Python environment, such as [Anaconda](https://www.anaconda.com/).

## Installation
1) Clone the repository to your local machine
2) run ```python setup.py install```
3) Install any relevant spaCy models you require. For example, for English run the following command:
```python -m spacy download en```
3) Follow the below instructions to install the Surprising Phrase Detector (SFPD)

## Installing the SFPD
> Robertson, Andrew David, 2019. Characterising semantically coherent classes of text through feature discovery (Doctoral thesis, University of Sussex).
> 
1) Clone the repository found [here](https://github.com/andehr/sfpd) (citing where necessary).
2) Follow the necessary installation instructions.

## Usage
The toolkit is primarily a library or programming API for others to develop their own corpus expansion pipelines and methodologies. However, a brief breakdown of each module can be found in the accompanying Wiki. 

## How to contribute
Please feel free to raise any issues found when using this toolkit, create pull requests or create discussion threads.






