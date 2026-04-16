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

### Searches

You can search any eukaryotic organism you want on this search engine. Be it rice, a species
of seaweed, or even a potato. For maximum results, I highly suggest you use the scientific name of the organism you want to look up. <br>

If you get no results, don't worry: just search again. <br>

![OrganelleResults.png](https://i.ibb.co/4nGDNNWv/Organelle-Results.png) <br>

When you're done looking at the results, click the `New Search` button again
to go back to the home page. <br>

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


## Getting Started

### Installing

This program was made using Python 3.13.11.
 
### Dependencies
 
The requirements.txt file has all the dependencies needed.
The next section will tell you how to install it.
 
### Executing the Program
 
First and foremost, you need to download the entire GenBank <br>

First, download the `organellebaseflask.zip` and extract the `organellebaseflask`
directory from it. *This will be the working directory you will execute Python from.*

* From the directory, get all your dependencies by executing this line on Python:
```
pip install -r requirements.txt
```
* Afterwards, you must make the tables Organelle Search uses to display results and keep track of users. Execute this:
```
flask --app organellebaseflask init-db
```
* Finally, execute this line:
```
flask --app organellebaseflask 
```
If all goes well, you should see an output of:
```
* Serving Flask app 'organellebaseflask'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
```
Visit the address and the page should look like the first screenshot. You have
successfully deployed Organelle Search on your own device!

## Help

* **Why do I have to make an account to search?**

Because the API (Entrez in this case) requires an email in order to conduct a search. The email
you use to make your account is the one that is used for said search to be executed.

* **Why is the program so slow?**

Once again, it's because of API limits. Without an API key, the maximum amount of requests you
can make is 3 per second. Same reason the maximum amount of results shown is 500.
This has already been accounted for in the script and a limit was placed so even if
you misspell your email, you shouldn't be blocked. However, please try to put a valid email.

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
