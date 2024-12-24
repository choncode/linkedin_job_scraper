# LinkedIn Job Scraper

There are two python scripts in this repo:

### job_scraper.py

This is just a python script that scrapes linkedin jobs based on your search url and filters, outputing to a JSON file with the following key value pairs for each job found:

```json
[
    {
        "title": "Example Job Title",
        "company": "Example",
        "location": "London, England, United Kingdom",
        "link": "https://uk.linkedin.com/jobs/view/sample_url1234",
        "description": "This is a made up job description that you would get from a linkedin job listing"
    }
]
```

### new_job_filter.py

This is a python script that filters the scraped jobs to remove any jobs that contain key words (skills) that you dont want to include, as well as checking against the existing_jobs.json to prevent duplication of job listings.


## Instructions

### Configuration

- Set up and activate your venv
- Run the following command `pip install -r requirements.txt`
- Open a linkedin page on your browser of choice
- Login with your usual details (this script does not require your credentials in any way)
- Go to the jobs page on linkedin
- Make a generic search as you would normally do, making sure to put the job title, location (at the mininum you need to put England, UK)
- Ideally add the preferred filters e.g. full-time, location, hybrid/remote, from past week etc
- Once the filters are saved and applied, grab the linkedin url of that search page

### Running job_scraper.py

- Locate the `search_url` variable and replace the url with the one you have copied
- Locate the `for i in range(2)` line, leave this as `2` to start with, but you can customise this range to be higher if you want to scrape more jobs which adds significant more run time
- Execute this python file with `python src/job_scraper.py`
*** Warnings, this should open a new Chrome browser page which 1 of the below will happen:
1. Stuck on a blank linkedin page
2. Opens the linkedin job search page but shows a login to see more jobs prompt
3. Opens the linkedin job search page and begins automatically loading more jobs before eventually expanding each job card

You may have to try a few times, but if `1` or `2` occurs, just close the browser and execute the Python file again. If `3`, then just sit back and relax.

When the script is finished (in scenario `3`), the browser should automatically close and you should get a new updated file in `./output/scraped_jobs.json`. In this json file, I recommend right clicking to Format Document and also word UNwrapping (yes the opposite of word wrapping), just so you're able to see the jobs in a readable way except for the trailing job description.

### Running new_job_filter.py

- Open and view the new_job_filter.py
- Locate the `job_filter` function
- Locate the `denied_skills` list, here you will input key words that you don't want to show in the job listings e.g. Place `Azure` if you dont want any matching jobs that have the word `Azure` in the job description
- Execute this python file with `python src/new_job_filter.py`
- This should now update/overwrite the `new_jobs.json`

### Manual Steps

- Now you can freely click on each job link in the scraped and filtered jobs from `new_jobs.json`
- Once you have viewed all jobs, you will need to manually copy and paste all of the jobs (the json objects) into the `existing_jobs.json` so that it keeps track of your viewed jobs for each future job scrape.
- And that's it! Just repeat the steps above for each new job search
