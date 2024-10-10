# Content Extractor

This repository contains a collection of tools for extracting and managing text and images from Microsoft PowerPoint slide decks and Word documents.  
These tools were written to automate the process of tracking assets used across multiple slide decks. 

The user simply needs to provide a path to a directory where one or more .pptx and/or .word documents are located. 
The extractor tools will cycle over each file in the given directory and extract text and images. 
For slide decks, text is logged to a json manifest which logs extracted content slide by slide. 
Extracted text is pre-processed to remove stop words and use lamentations to stem words to their root. 
The raw text and pre-processed text are both logged to the json manifest where it can be mined later. 
Images are all given a unique identifier which is tracked in the json manifest. 
Images are resized to fit within the bounds of a maximum dimension given by the user. 
This is done to reduce the amount to data storage needed when extracting large amounts of large images. 
The extracted images are then processed to calculate color moments for indexing and similarity measurements, which are used to cull duplicate images. 
Culled duplicate images are still tracked in the manifest so even if the image is removed, it can be traced back to the slide where it was extracted.
