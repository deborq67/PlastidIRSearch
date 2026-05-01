# PlastidSearch
An NCBI-based search engine that detects inverted repeats within plant plastids.

## Description

Organelles are analogous to mini-organs within the cells of multicellular organisms like 
plants, animals, fungi, algae, and just about anything else that is not bacteria or archaea. Some of 
these organelles, such as mitochondria and chloroplasts, are believed to have evolved from 
bacteria that had a symbiotic relationship with an ancient cell lineage. As such, both chloroplasts 
and mitochondria still have their own genomes, or genetic material. These genomes have been 
significantly reduced via billions of years of evolution, but there are completed maps of these 
DNA sequences of organelles for different species in genetic databases.

Plastid IR Search is a search engine for complete *plastid* genome records. Plastids are a type of organelle 
only found in plants, algae, and a few other eukaryotes. Chloroplasts, the organelles responsible for photosynthesis in 
plants, are actually a type of plastid. One of the more unique features of plastid genomes is that 
they mostly consist of what are known as inverted repeats (IRs). Basically, these are two separate 
sections of the genome that are opposites of each other and, when lined up, match. For example, 
Ira (the first inverted repeat) could look like:
```
GCTTATTCTCTATGCGGGG
```
and then Irb would be the same sequence backwards:

```
GGGGCGTATCTCTTATTCG
```
In GenBank, some of these complete plastid genome records do not note, or annotate, whether there is
an inverted repeat present or not. Plastid IR Search tries to locate the presence of these notes in the
records and if they're present, it gives the exact locations according to the notes.

## How to Use

Just like any search engine, make your search by typing whatever plant or alga you want into the
search engine, no registration needed!

![OrganelleSearchHome.png](https://i.ibb.co/hJfzx0qB/Organelle-Register.png) <br>

### About

On the button at the hand-hand corner. This button mainly tells you basic information and *some* FAQS
about the project so you don't have to look at the Github page every time you want to do find something
out. Mainly, it has a legend for the symbols in inverted repeats in case you want to know what each one does.
<br>

### Searches

You can search any eukaryotic organism you want on this search engine. Be it rice, a species
of seaweed, or even a potato. For maximum results, I highly suggest you use the scientific family or family of the organism you want to look up.
Be warned though that due to rate-limiting, the results will be slower the more results generated.<br>

If you get no results, don't worry: just search again. <br>

![OrganelleResults.png](https://i.ibb.co/4nGDNNWv/Organelle-Results.png) <br>

Unlike my previous projects, the purpose of Plastid IR Search is to tell you information on whether inverted repeats were *annotated* in the actual
genetic records of these plants and algae which is achieved via the analysis of more than 40000 genetic records. The check mark means both inverted
repeats were annotated, the X means none were annotated, and the grey dash means the file was not found. YOu may have noticed that the `Accession` column is hyperlinked. That's because when you click on it, a different output appears depending on what `IR Reported in Record File?` says. If you click on it when there is an X, the program will simply tell you there was nothing found. If you click on a row with a dash however:

#########################################



When you're done looking at the results, click the logo or
make a new search using the Result search bar. <br>

Need some ideas of what to search for? Try these organisms:
 * *Solanum tuberosum* - Potato

### History

You may have noticed that at the end of the top black bar, there is an option that
says `History`. As the name suggests, this button lets you view your entire
search history including invalid results. It will also show the time stamp
of when said search was executed. <br>

![OrganelleHistory.png](https://i.ibb.co/TqH77P7T/Organelle-History.png) <br>

If you have a Django admin account, you can also visit the Django admin page to view, delete,
and edit the search histories of users, including yours. Specifically, you can edit the amount
of records found and the search term itself if you so choose.

### Accession Finds

On the button at the hand-hand corner. This button mainly tells you basic information and *some* FAQS
about the project so you don't have to look at the Github page every time you want to do find something
out. Mainly, it has a legend for the symbols in inverted repeats in case you want to know what each one does.
<br>


## Getting Started

### Installing

This program was made using Python 3.13.11.
 
### Dependencies
 
The requirements.txt file has all the dependencies needed.
The next section will tell you how to install it.
 
### Executing the Program
 
Given the complexity of this program, you will have several steps before you can use it.

#### Step 1: Get your dependencies installed.

* From the directory, get all your dependencies by executing this line on Python:
```
pip install -r requirements.txt
```

#### Step 2: Download the Genbank folder and put it in the plastid_ir_search folder.

NOT in the `PlastidIRSearch` folder (your root.) Put the folder on the same level as manage.py, you'll see
why later. As you do so, be sure to also  run `cd ./plastid_ir_search` on your terminal (both Windows and Linux).

[Download the needed folder here.](https://drive.google.com/file/d/1D-JlTBUCT_bMl8UBFwnFtCS_qHYZx6ur/view?usp=drive_link)

Fair warning: This folder is around 1.1 GB large and fully decompressed, you're looking at almost 14 GB. It contains over 40000
publicly-available genetic records from [NCBI Genbank.](https://www.ncbi.nlm.nih.gov/genbank/) Don't change the name of the folder.

#### Step 2: Get the models created.

Needed to store important information later on. Just do:

```
python manage.py makemigrations
python manage.py migrate
```

#### Step 3: Execute ir_setup.

This is a custom command that will generate IR values to be associated with each search. It detects that exact `genbank_files` folder on
the manage.py level. This step will take a few minutes since it is computing more than 40000 files. Just do:

```
python manage.py ir_setup
```

OPTIONAL: If you ever want to update your existing files already on tables for any reason, you can do:
```
python manage.py ir_setup -u
```
#### Step 4: Run the server.
Just do:
```
python manage.py runserver
```
After that, the search engine should be up and running and look like the following:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 01, 2026 - 07:58:08
Django version 6.0.4, using settings 'plastid_ir_search.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Visit the address and the page should look like the first screenshot. You have
successfully deployed Organelle Search on your own device!

## Help


* **Why is the program so slow?**

Once again, it's because of API limits. Without an API key, the maximum amount of requests you
can make is 3 per second. Same reason the maximum amount of results shown is 500.
This has already been accounted for in the script and a limit was placed so even if
you misspell your email, you shouldn't be blocked. However, please try to put a valid email.

* **ERROR: Could not find a version that satisfies the requirement package==version_number**

This has happened to me a couple of times. Usually it means that the Python environment you are using has repositories not yet updated. In fact,
the Biopython I was using during this project is the latest version that came one month ago! Try setting up a .venv to remedy that doing:
```
python -m venv .venv
source .venv/bin/activate
```
or depending on what type of Python you have:
```
python3 -m venv .venv
source .venv/bin/activate
```
Alternatively, you could try taking out the version number and stick with the latest package in your Python repository. I imagine this would most likely work.

## Authors
 
* David Bohorquez
 
## Version History

* Released as organellebaseflask.zip.
 
## License
 
This project is licensed under the GNU General Public License - see the LICENSE.md file for details
 
## Acknowledgments
 
* [Fayette Reynolds for the background image.](https://www.pexels.com/photo/cell-seen-under-microscope-11198505/)
* [Bootstrap Template for Search Bar](https://bootstrapexamples.com/@anonymous/search-bar-with-search-icon-in-bootstrap-5-2)
* [Bootstrap Template for Error Page](https://bootstrapexamples.com/@valeria/404-page-template-2)
* [This Ernst Haeckel drawing for the logo: it's public domain.](https://pdimagearchive.org/images/b46b8d91-a0b4-4134-8268-1660285ab735/)
* [Modified Heroic Template used for base.html](https://github.com/startbootstrap/startbootstrap-heroic-features)
* [Register and Login System](https://learndjango.com/tutorials/django-login-and-logout-tutorial)
* [Bootstrap Navbar Documentation](https://getbootstrap.com/docs/4.0/components/navbar/#text)
